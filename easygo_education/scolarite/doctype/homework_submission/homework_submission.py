"""Homework Submission DocType."""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, get_time, flt, now_datetime


class HomeworkSubmission(Document):
    """Homework Submission management."""
    
    def validate(self):
        """Validate homework submission data."""
        self.validate_submission_date()
        self.validate_grade()
        self.check_late_submission()
        self.calculate_percentage()
        self.set_defaults()
    
    def validate_submission_date(self):
        """Validate submission date against homework due date."""
        if self.homework:
            homework_doc = frappe.get_doc("Homework", self.homework)
            
            if homework_doc.due_date and self.submission_date:
                if getdate(self.submission_date) > getdate(homework_doc.due_date):
                    if not self.extension_granted:
                        self.is_late = 1
                        frappe.msgprint(_("Warning: This is a late submission"), alert=True)
    
    def validate_grade(self):
        """Validate grade against max grade."""
        if self.grade and self.max_grade:
            if flt(self.grade) > flt(self.max_grade):
                frappe.throw(_("Grade cannot exceed maximum grade"))
            
            if flt(self.grade) < 0:
                frappe.throw(_("Grade cannot be negative"))
    
    def check_late_submission(self):
        """Check if submission is late."""
        if not self.homework:
            return
        
        homework_doc = frappe.get_doc("Homework", self.homework)
        
        if homework_doc.due_date and self.submission_date:
            due_date = getdate(homework_doc.due_date)
            submission_date = getdate(self.submission_date)
            
            if submission_date > due_date and not self.extension_granted:
                self.is_late = 1
            elif self.extension_granted and self.extension_date:
                if submission_date > getdate(self.extension_date):
                    self.is_late = 1
                else:
                    self.is_late = 0
    
    def calculate_percentage(self):
        """Calculate percentage score."""
        if self.grade and self.max_grade and flt(self.max_grade) > 0:
            self.percentage = (flt(self.grade) / flt(self.max_grade)) * 100
    
    def set_defaults(self):
        """Set default values."""
        if not self.submission_date:
            self.submission_date = getdate()
        
        if not self.submission_time:
            self.submission_time = get_time()
        
        if not self.status:
            self.status = "Submitted"
        
        # Get max grade from homework
        if self.homework and not self.max_grade:
            homework_doc = frappe.get_doc("Homework", self.homework)
            self.max_grade = homework_doc.max_grade
    
    def on_update(self):
        """Actions after update."""
        if self.status == "Graded" and self.grade:
            self.update_homework_statistics()
            self.notify_student()
    
    def update_homework_statistics(self):
        """Update homework completion statistics."""
        if self.homework:
            homework_doc = frappe.get_doc("Homework", self.homework)
            
            # Count submissions
            total_submissions = frappe.db.count("Homework Submission", {
                "homework": self.homework,
                "status": ["in", ["Submitted", "Graded", "Returned", "Resubmitted"]]
            })
            
            graded_submissions = frappe.db.count("Homework Submission", {
                "homework": self.homework,
                "status": "Graded"
            })
            
            # Calculate average grade
            avg_grade = frappe.db.sql("""
                SELECT AVG(grade)
                FROM `tabHomework Submission`
                WHERE homework = %s AND status = 'Graded' AND grade IS NOT NULL
            """, [self.homework], as_list=True)
            
            homework_doc.total_submissions = total_submissions
            homework_doc.graded_submissions = graded_submissions
            homework_doc.average_grade = avg_grade[0][0] if avg_grade and avg_grade[0][0] else 0
            homework_doc.save()
    
    @frappe.whitelist()
    def submit_homework(self):
        """Submit homework for grading."""
        if self.status != "Draft":
            frappe.throw(_("Only draft submissions can be submitted"))
        
        if not self.submission_text and not self.attachments:
            frappe.throw(_("Please provide submission content or attachments"))
        
        self.status = "Submitted"
        self.submission_date = getdate()
        self.submission_time = get_time()
        self.save()
        
        # Notify teacher
        self.notify_teacher()
        
        frappe.msgprint(_("Homework submitted successfully"))
        return self
    
    @frappe.whitelist()
    def grade_submission(self, grade, feedback=None):
        """Grade the submission."""
        if self.status not in ["Submitted", "Resubmitted"]:
            frappe.throw(_("Only submitted homework can be graded"))
        
        if not grade:
            frappe.throw(_("Please provide a grade"))
        
        self.grade = flt(grade)
        self.feedback = feedback
        self.graded_by = frappe.session.user
        self.graded_date = getdate()
        self.status = "Graded"
        
        self.save()
        
        frappe.msgprint(_("Homework graded successfully"))
        return self
    
    @frappe.whitelist()
    def return_for_revision(self, feedback):
        """Return submission for revision."""
        if self.status not in ["Submitted", "Resubmitted"]:
            frappe.throw(_("Only submitted homework can be returned"))
        
        self.feedback = feedback
        self.status = "Returned"
        self.save()
        
        # Notify student
        self.notify_student("returned")
        
        frappe.msgprint(_("Homework returned for revision"))
        return self
    
    @frappe.whitelist()
    def resubmit_homework(self):
        """Resubmit homework after revision."""
        if self.status != "Returned":
            frappe.throw(_("Only returned homework can be resubmitted"))
        
        self.status = "Resubmitted"
        self.submission_date = getdate()
        self.submission_time = get_time()
        self.save()
        
        # Notify teacher
        self.notify_teacher("resubmitted")
        
        frappe.msgprint(_("Homework resubmitted successfully"))
        return self
    
    def notify_teacher(self, action="submitted"):
        """Notify teacher about submission."""
        if not self.homework:
            return
        
        homework_doc = frappe.get_doc("Homework", self.homework)
        teacher = homework_doc.teacher
        
        if teacher:
            if action == "submitted":
                subject = _("New Homework Submission: {0}").format(homework_doc.title)
                message = self.get_submission_message()
            elif action == "resubmitted":
                subject = _("Homework Resubmitted: {0}").format(homework_doc.title)
                message = self.get_resubmission_message()
            
            frappe.sendmail(
                recipients=[teacher],
                subject=subject,
                message=message,
                reference_doctype=self.doctype,
                reference_name=self.name
            )
    
    def notify_student(self, action="graded"):
        """Notify student about grading or return."""
        if not self.student:
            return
        
        student_user = frappe.db.get_value("Student", self.student, "user")
        
        if student_user:
            if action == "graded":
                subject = _("Homework Graded: {0}").format(self.homework)
                message = self.get_grading_message()
            elif action == "returned":
                subject = _("Homework Returned: {0}").format(self.homework)
                message = self.get_return_message()
            
            frappe.sendmail(
                recipients=[student_user],
                subject=subject,
                message=message,
                reference_doctype=self.doctype,
                reference_name=self.name
            )
    
    def get_submission_message(self):
        """Get submission notification message."""
        return _("""
        New Homework Submission
        
        Student: {student_name}
        Homework: {homework}
        Submission Date: {submission_date}
        Status: {status}
        
        {late_info}
        
        Please review and grade the submission.
        """).format(
            student_name=self.student_name,
            homework=self.homework,
            submission_date=self.submission_date,
            status=self.status,
            late_info=_("Note: This is a late submission") if self.is_late else ""
        )
    
    def get_grading_message(self):
        """Get grading notification message."""
        return _("""
        Homework Graded
        
        Homework: {homework}
        Grade: {grade}/{max_grade} ({percentage}%)
        Graded By: {graded_by}
        Graded Date: {graded_date}
        
        Feedback:
        {feedback}
        """).format(
            homework=self.homework,
            grade=self.grade,
            max_grade=self.max_grade,
            percentage=round(self.percentage, 1) if self.percentage else 0,
            graded_by=self.graded_by,
            graded_date=self.graded_date,
            feedback=self.feedback or _("No feedback provided")
        )
    
    def get_return_message(self):
        """Get return notification message."""
        return _("""
        Homework Returned for Revision
        
        Homework: {homework}
        
        Feedback:
        {feedback}
        
        Please revise and resubmit your homework.
        """).format(
            homework=self.homework,
            feedback=self.feedback or _("Please revise your submission")
        )
    
    def get_resubmission_message(self):
        """Get resubmission notification message."""
        return _("""
        Homework Resubmitted
        
        Student: {student_name}
        Homework: {homework}
        Resubmission Date: {submission_date}
        
        The student has revised and resubmitted their homework.
        Please review the updated submission.
        """).format(
            student_name=self.student_name,
            homework=self.homework,
            submission_date=self.submission_date
        )
    
    @frappe.whitelist()
    def get_submission_history(self):
        """Get submission history for this homework and student."""
        return frappe.get_all("Homework Submission",
            filters={
                "homework": self.homework,
                "student": self.student
            },
            fields=["name", "submission_date", "status", "grade", "feedback"],
            order_by="submission_date desc"
        )
    
    @frappe.whitelist()
    def grant_extension(self, extension_date, reason=None):
        """Grant extension for homework submission."""
        self.extension_granted = 1
        self.extension_date = extension_date
        
        if reason:
            self.late_reason = reason
        
        # Recalculate late status
        self.check_late_submission()
        self.save()
        
        # Notify student
        if self.student:
            student_user = frappe.db.get_value("Student", self.student, "user")
            if student_user:
                frappe.sendmail(
                    recipients=[student_user],
                    subject=_("Extension Granted: {0}").format(self.homework),
                    message=_("""
                    Extension Granted
                    
                    Homework: {homework}
                    New Due Date: {extension_date}
                    Reason: {reason}
                    
                    You can now submit your homework until the new due date.
                    """).format(
                        homework=self.homework,
                        extension_date=self.extension_date,
                        reason=reason or _("Extension granted")
                    ),
                    reference_doctype=self.doctype,
                    reference_name=self.name
                )
        
        frappe.msgprint(_("Extension granted successfully"))
        return self
