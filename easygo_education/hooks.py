"""Hooks configuration for EasyGo Education app."""

from . import __version__ as app_version

app_name = "easygo_education"
app_title = "EasyGo Education"
app_publisher = "EasyGo Education Team"
app_description = "Comprehensive educational institution management system for Morocco"
app_icon = "octicon octicon-mortar-board"
app_color = "blue"
app_email = "contact@easygo-education.ma"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/easygo_education/css/easygo_education.min.css"
app_include_js = "/assets/easygo_education/js/easygo_education.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/easygo_education/css/easygo_education.css"
# web_include_js = "/assets/easygo_education/js/easygo_education.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "easygo_education/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "easygo_education.utils.jinja_methods",
# 	"filters": "easygo_education.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "easygo_education.install.before_install"
after_install = "easygo_education.patches.v1_bootstrap.execute"

# Uninstallation
# ------------

# before_uninstall = "easygo_education.uninstall.before_uninstall"
# after_uninstall = "easygo_education.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "easygo_education.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Student": {
        "validate": "easygo_education.scolarite.doctype.student.student.validate_student",
        "after_insert": "easygo_education.scolarite.doctype.student.student.send_welcome_email",
    },
    "Student Attendance": {
        "after_insert": "easygo_education.vie_scolaire.doctype.student_attendance.student_attendance.notify_guardian",
    },
    "Course Schedule": {
        "validate": "easygo_education.scolarite.doctype.course_schedule.course_schedule.validate_schedule",
    },
    "Fee Bill": {
        "before_submit": "easygo_education.finances_rh.doctype.fee_bill.fee_bill.freeze_totals",
        "on_submit": "easygo_education.finances_rh.doctype.fee_bill.fee_bill.create_ledger_entry",
    },
    "Payment Entry": {
        "on_submit": "easygo_education.finances_rh.doctype.payment_entry.payment_entry.allocate_to_bills",
    },
    "Leave Application": {
        "validate": "easygo_education.finances_rh.doctype.leave_application.leave_application.validate_leave",
    },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "easygo_education.jobs.daily.check_overdue_fees",
        "easygo_education.jobs.daily.maintenance_reminders",
        "easygo_education.jobs.daily.attendance_anomalies",
    ],
    "weekly": [
        "easygo_education.jobs.weekly.attendance_summaries",
        "easygo_education.jobs.weekly.teacher_load_analysis",
        "easygo_education.jobs.weekly.budget_burn_rate",
    ],
    "monthly": [
        "easygo_education.jobs.monthly.massar_exports",
        "easygo_education.jobs.monthly.payroll_checks",
        "easygo_education.jobs.monthly.asset_rollup",
    ],
}

# Testing
# -------

# before_tests = "easygo_education.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "easygo_education.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "easygo_education.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"easygo_education.auth.validate"
# ]

# Fixtures
# --------
# Export fixtures for the app

fixtures = [
    {
        "doctype": "Role",
        "filters": [
            [
                "name",
                "in",
                [
                    "Student",
                    "Parent",
                    "Teacher",
                    "Principal",
                    "Accountant",
                    "HR Manager",
                    "Maintenance",
                    "Transport",
                    "Canteen",
                    "Director",
                ],
            ]
        ],
    },
    {
        "doctype": "Desktop Icon",
        "filters": [["module_name", "=", "EasyGo Education"]],
    },
    "Letter Head",
    "Web Form",
]

# Website
# -------

website_route_rules = [
    {"from_route": "/student/<path:app_path>", "to_route": "student"},
    {"from_route": "/parent/<path:app_path>", "to_route": "parent"},
    {"from_route": "/teacher/<path:app_path>", "to_route": "teacher"},
]

# Portal menu items
portal_menu_items = [
    {
        "title": "Student Portal",
        "route": "/student",
        "reference_doctype": "Student",
        "role": "Student",
    },
    {
        "title": "Parent Portal",
        "route": "/parent",
        "reference_doctype": "Guardian",
        "role": "Parent",
    },
    {
        "title": "Teacher Portal",
        "route": "/teacher",
        "reference_doctype": "Employee",
        "role": "Teacher",
    },
]

# Whitelisted API endpoints
whitelist_for_web = [
    "easygo_education.api.portal.get_portal_home",
    "easygo_education.api.portal.get_timetable",
    "easygo_education.api.portal.get_attendance",
    "easygo_education.api.portal.submit_attendance_justification",
    "easygo_education.api.portal.list_homework",
    "easygo_education.api.portal.submit_homework",
    "easygo_education.api.portal.list_assessments",
    "easygo_education.api.portal.submit_grades",
    "easygo_education.api.portal.list_fee_bills",
    "easygo_education.api.portal.initiate_payment",
    "easygo_education.api.portal.list_messages",
    "easygo_education.api.portal.post_message",
    "easygo_education.api.portal.book_meeting",
    "easygo_education.api.portal.confirm_meeting",
]
