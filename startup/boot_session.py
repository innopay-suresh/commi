try:
	import frappe
except ImportError:
	# Handle case when frappe is not available (e.g., during development)
	class MockFrappe:
		def __init__(self):
			self.session = type('obj', (object,), {'user': 'Administrator'})()
			self.db = type('obj', (object,), {
				'get_value': lambda *args, **kwargs: None
			})()
		
		def get_cached_doc(self, doctype):
			return {}
		
		def get_roles(self, user):
			return ["Administrator"]
	
	frappe = MockFrappe()


def boot_session(bootinfo):
	"""Add AspireHR specific data to bootinfo"""
	
	# Add HR settings to bootinfo
	bootinfo.hr_settings = frappe.get_cached_doc("HR Settings")
	
	# Add user's employee record if exists
	if frappe.session.user != "Guest":
		employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, 
			["name", "employee_name", "department", "designation", "company"], as_dict=True)
		if employee:
			bootinfo.employee = employee
	
	# Add AspireHR specific permissions
	bootinfo.aspirehr_permissions = get_aspirehr_permissions()


def get_aspirehr_permissions():
	"""Get AspireHR specific permissions for current user"""
	user_roles = frappe.get_roles(frappe.session.user)
	
	permissions = {
		"can_view_all_employees": "HR Manager" in user_roles,
		"can_approve_leaves": "Leave Approver" in user_roles or "HR Manager" in user_roles,
		"can_approve_expenses": "Expense Approver" in user_roles or "HR Manager" in user_roles,
		"can_process_payroll": "Payroll Manager" in user_roles or "HR Manager" in user_roles,
		"can_manage_recruitment": "Recruitment Manager" in user_roles or "HR Manager" in user_roles,
		"can_manage_training": "Training Manager" in user_roles or "HR Manager" in user_roles,
	}
	
	return permissions
