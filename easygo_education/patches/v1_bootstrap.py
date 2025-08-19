"""Bootstrap patch for EasyGo Education v1.0."""

import frappe
from frappe import _


def execute():
    """Execute bootstrap patch - creates initial demo data."""
    if frappe.db.exists("Academic Year", "2024-2025"):
        # Patch already executed
        return
    
    print("Executing EasyGo Education bootstrap patch...")
    
    # This will be implemented in Phase 7
    # For now, just create a marker to prevent re-execution
    frappe.get_doc({
        "doctype": "Academic Year",
        "name": "2024-2025",
        "year_start_date": "2024-09-01",
        "year_end_date": "2025-06-30",
        "is_default": 1
    }).insert(ignore_permissions=True)
    
    print("Bootstrap patch executed successfully")
