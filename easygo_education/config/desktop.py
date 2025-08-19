"""Desktop configuration for EasyGo Education modules."""

from frappe import _


def get_data():
    """Return desktop icons configuration."""
    return [
        {
            "module_name": "Scolarité",
            "category": "Modules",
            "label": _("Academics"),
            "color": "blue",
            "icon": "octicon octicon-book",
            "type": "module",
            "description": _("Student management, academics, timetables, assessments"),
        },
        {
            "module_name": "Vie Scolaire",
            "category": "Modules", 
            "label": _("School Life"),
            "color": "green",
            "icon": "octicon octicon-calendar",
            "type": "module",
            "description": _("Attendance, discipline, health, activities"),
        },
        {
            "module_name": "Finances RH",
            "category": "Modules",
            "label": _("Finance & HR"),
            "color": "orange",
            "icon": "octicon octicon-credit-card",
            "type": "module",
            "description": _("Fee management, payroll, budgeting"),
        },
        {
            "module_name": "Administration Comms",
            "category": "Modules",
            "label": _("Administration"),
            "color": "purple",
            "icon": "octicon octicon-megaphone",
            "type": "module",
            "description": _("Communications, notifications, meetings"),
        },
        {
            "module_name": "Gestion Etablissement",
            "category": "Modules",
            "label": _("Facility Management"),
            "color": "red",
            "icon": "octicon octicon-home",
            "type": "module",
            "description": _("Assets, maintenance, transport, canteen"),
        },
        {
            "module_name": "Referentiels",
            "category": "Modules",
            "label": _("References"),
            "color": "grey",
            "icon": "octicon octicon-gear",
            "type": "module",
            "description": _("Settings, grading scales, reference data"),
        },
    ]
