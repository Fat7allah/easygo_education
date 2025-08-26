"""Parent Consent DocType."""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, now_datetime, add_days


class ParentConsent(Document):
    """Parent Consent management."""
    
    def validate(self):
        """Validate parent consent data."""
        self.validate_dates()
        self.validate_guardian()
        self.set_defaults()
    
    def validate_dates(self):
        """Validate consent dates."""
        if self.activity_date and self.request_date:
            if getdate(self.activity_date) < getdate(self.request_date):
                frappe.throw(_("Activity date cannot be before request date"))
        
        if self.expiry_date and self.request_date:
            if getdate(self.expiry_date) <= getdate(self.request_date):
                frappe.throw(_("Expiry date must be after request date"))
    
    def validate_guardian(self):
        """Validate guardian relationship with student."""
        if self.student and self.guardian:
            guardian_students = frappe.db.get_all("Student Guardian",
                filters={"guardian": self.guardian},
                fields=["parent"]
            )
            
            student_list = [g.parent for g in guardian_students]
            
            if self.student not in student_list:
                frappe.throw(_("Selected guardian is not associated with this student"))
    
    def set_defaults(self):
        """Set default values."""
        if not self.status:
            self.status = "Pending"
        
        if not self.expiry_date and self.activity_date:
            # Set expiry date to 7 days after activity date
            self.expiry_date = add_days(self.activity_date, 7)
    
    def on_update(self):
        """Actions after update."""
        if self.consent_given and not self.consent_date:
            self.consent_date = now_datetime()
            self.status = "Approved"
        
        self.check_expiry()
    
    def check_expiry(self):
        """Check if consent has expired."""
        if self.expiry_date and getdate() > getdate(self.expiry_date):
            if self.status not in ["Expired", "Declined", "Withdrawn"]:
                self.status = "Expired"
    
    @frappe.whitelist()
    def send_consent_request(self):
        """Send consent request to guardian."""
        if self.status != "Pending":
            frappe.throw(_("Only pending consent requests can be sent"))
        
        guardian_doc = frappe.get_doc("Guardian", self.guardian)
        
        if guardian_doc.email_address:
            # Send email with consent form
            self.send_consent_email()
        
        if guardian_doc.mobile_number:
            # Send SMS notification
            self.send_consent_sms()
        
        frappe.msgprint(_("Consent request sent successfully"))
        return self
    
    def send_consent_email(self):
        """Send consent request email."""
        guardian_doc = frappe.get_doc("Guardian", self.guardian)
        
        subject = _("Consent Request: {0}").format(self.consent_title)
        message = self.get_consent_email_message()
        
        # Generate consent form URL
        consent_url = self.get_consent_form_url()
        
        frappe.sendmail(
            recipients=[guardian_doc.email_address],
            subject=subject,
            message=message,
            reference_doctype=self.doctype,
            reference_name=self.name,
            attachments=self.get_consent_attachments()
        )
    
    def send_consent_sms(self):
        """Send consent request SMS."""
        guardian_doc = frappe.get_doc("Guardian", self.guardian)
        
        message = _("Consent required for {0}. Please check your email or visit the parent portal. School: {1}").format(
            self.consent_title,
            frappe.db.get_single_value("School Settings", "school_name")
        )
        
        # Use SMS adapter
        from easygo_education.finances_rh.adapters.sms import send_sms
        send_sms(guardian_doc.mobile_number, message)
    
    @frappe.whitelist()
    def approve_consent(self, digital_signature=None):
        """Approve consent (guardian action)."""
        if self.status != "Pending":
            frappe.throw(_("Only pending consent requests can be approved"))
        
        self.consent_given = 1
        self.consent_date = now_datetime()
        self.status = "Approved"
        
        if digital_signature:
            self.digital_signature = digital_signature
        
        self.save()
        
        # Notify school
        self.notify_school("approved")
        
        frappe.msgprint(_("Consent approved successfully"))
        return self
    
    @frappe.whitelist()
    def decline_consent(self, reason=None):
        """Decline consent (guardian action)."""
        if self.status != "Pending":
            frappe.throw(_("Only pending consent requests can be declined"))
        
        self.consent_given = 0
        self.status = "Declined"
        
        if reason:
            self.description = (self.description or "") + f"\n\nDeclined Reason: {reason}"
        
        self.save()
        
        # Notify school
        self.notify_school("declined", reason)
        
        frappe.msgprint(_("Consent declined"))
        return self
    
    @frappe.whitelist()
    def withdraw_consent(self, reason=None):
        """Withdraw previously given consent."""
        if self.status != "Approved":
            frappe.throw(_("Only approved consent can be withdrawn"))
        
        self.consent_given = 0
        self.status = "Withdrawn"
        
        if reason:
            self.description = (self.description or "") + f"\n\nWithdrawal Reason: {reason}"
        
        self.save()
        
        # Notify school
        self.notify_school("withdrawn", reason)
        
        frappe.msgprint(_("Consent withdrawn"))
        return self
    
    def notify_school(self, action, reason=None):
        """Notify school about consent status change."""
        if self.responsible_teacher:
            subject = _("Consent {0}: {1}").format(action.title(), self.consent_title)
            message = self.get_school_notification_message(action, reason)
            
            frappe.sendmail(
                recipients=[self.responsible_teacher],
                subject=subject,
                message=message,
                reference_doctype=self.doctype,
                reference_name=self.name
            )
        
        # Also notify education manager
        education_manager = frappe.db.get_single_value("School Settings", "education_manager")
        if education_manager and education_manager != self.responsible_teacher:
            frappe.sendmail(
                recipients=[education_manager],
                subject=_("Consent Update: {0}").format(self.consent_title),
                message=self.get_school_notification_message(action, reason),
                reference_doctype=self.doctype,
                reference_name=self.name
            )
    
    def get_consent_email_message(self):
        """Get consent request email message."""
        return _("""
        Dear Parent/Guardian,
        
        We are requesting your consent for the following activity involving your child:
        
        Student: {student_name}
        Activity: {consent_title}
        Type: {consent_type}
        Date: {activity_date}
        Location: {activity_location}
        
        Description:
        {description}
        
        Responsible Teacher: {responsible_teacher}
        Emergency Contact: {emergency_contact}
        
        Please review the details and provide your consent by clicking the link below:
        {consent_url}
        
        If you have any questions, please contact the school.
        
        Thank you,
        {school_name}
        """).format(
            student_name=self.student_name,
            consent_title=self.consent_title,
            consent_type=self.consent_type,
            activity_date=self.activity_date or "TBD",
            activity_location=self.activity_location or "TBD",
            description=self.description,
            responsible_teacher=self.responsible_teacher or "School Staff",
            emergency_contact=self.emergency_contact or "School Office",
            consent_url=self.get_consent_form_url(),
            school_name=frappe.db.get_single_value("School Settings", "school_name")
        )
    
    def get_school_notification_message(self, action, reason=None):
        """Get school notification message."""
        message = _("""
        Consent Status Update
        
        Student: {student_name}
        Guardian: {guardian}
        Activity: {consent_title}
        Status: {status}
        Action Date: {consent_date}
        
        """).format(
            student_name=self.student_name,
            guardian=self.guardian,
            consent_title=self.consent_title,
            status=action.title(),
            consent_date=self.consent_date
        )
        
        if reason:
            message += f"Reason: {reason}\n\n"
        
        if action == "approved":
            message += _("The parent has given consent for this activity.")
        elif action == "declined":
            message += _("The parent has declined consent for this activity.")
        elif action == "withdrawn":
            message += _("The parent has withdrawn their previously given consent.")
        
        return message
    
    def get_consent_form_url(self):
        """Get consent form URL for parent portal."""
        site_url = frappe.utils.get_url()
        return f"{site_url}/app/parent-consent/{self.name}"
    
    def get_consent_attachments(self):
        """Get consent form attachments."""
        attachments = []
        
        if self.consent_form_template:
            template_doc = frappe.get_doc("Document Template", self.consent_form_template)
            if template_doc.template_file:
                attachments.append({
                    "fname": f"Consent_Form_{self.name}.pdf",
                    "fcontent": template_doc.template_file
                })
        
        # Add other attachments
        for attachment in self.attachments:
            if attachment.file_url:
                attachments.append({
                    "fname": attachment.file_name,
                    "fcontent": frappe.get_doc("File", {"file_url": attachment.file_url}).get_content()
                })
        
        return attachments
    
    @frappe.whitelist()
    def generate_consent_report(self):
        """Generate consent status report."""
        return {
            "consent_id": self.name,
            "student": self.student_name,
            "guardian": self.guardian,
            "activity": self.consent_title,
            "type": self.consent_type,
            "request_date": self.request_date,
            "activity_date": self.activity_date,
            "status": self.status,
            "consent_given": self.consent_given,
            "consent_date": self.consent_date,
            "expiry_date": self.expiry_date,
            "responsible_teacher": self.responsible_teacher
        }
    
    @frappe.whitelist()
    def get_related_consents(self):
        """Get related consent requests for the same student."""
        return frappe.get_all("Parent Consent",
            filters={
                "student": self.student,
                "name": ["!=", self.name]
            },
            fields=["name", "consent_title", "consent_type", "status", "request_date"],
            order_by="request_date desc",
            limit=10
        )
    
    def get_consent_summary(self):
        """Get consent summary for dashboard."""
        return {
            "total_requests": frappe.db.count("Parent Consent"),
            "pending_requests": frappe.db.count("Parent Consent", {"status": "Pending"}),
            "approved_requests": frappe.db.count("Parent Consent", {"status": "Approved"}),
            "declined_requests": frappe.db.count("Parent Consent", {"status": "Declined"}),
            "expired_requests": frappe.db.count("Parent Consent", {"status": "Expired"})
        }
