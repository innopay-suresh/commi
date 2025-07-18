import frappe

@frappe.whitelist()
def get_employee_count():
    """Returns the total number of active employees."""
    try:
        active_employees = frappe.db.count("Employee", {"status": "Active"})
        return active_employees
    except Exception as e:
        frappe.log_error(f"Error fetching employee count: {e}", "HR Metrics API")
        return 0

@frappe.whitelist()
def get_pending_leaves_count():
    """Returns the total number of pending leave applications."""
    try:
        pending_leaves = frappe.db.count("Leave Application", {"status": "Open"})
        return pending_leaves
    except Exception as e:
        frappe.log_error(f"Error fetching pending leaves count: {e}", "HR Metrics API")
        return 0