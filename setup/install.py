try:
	import frappe
	from frappe import _
except ImportError:
	# Handle case when frappe is not available (e.g., during development)
	class MockFrappe:
		def __init__(self):
			self.db = type('obj', (object,), {
				'exists': lambda *args, **kwargs: False,
				'get_value': lambda *args, **kwargs: None,
				'commit': lambda: None
			})()
		
		def new_doc(self, doctype):
			return type('obj', (object,), {
				'insert': lambda **kwargs: None,
				'update': lambda data: None
			})()
	
	frappe = MockFrappe()
	
	def _(text):
		return text


def after_install():
	"""Setup AspireHR after installation"""
	create_default_hr_settings()
	create_default_roles()
	create_default_leave_types()
	create_default_salary_components()
	create_default_departments()
	create_default_designations()
	create_default_employment_types()
	
	frappe.db.commit()
	
	print("AspireHR has been installed successfully!")


def create_default_hr_settings():
	"""Create default HR Settings"""
	if not frappe.db.exists("HR Settings", "HR Settings"):
		hr_settings = frappe.new_doc("HR Settings")
		hr_settings.update({
			"employee_number_series": "EMP-.YYYY.-",
			"max_working_hours_against_timesheet": 10,
			"include_holidays_in_total_working_days": 0,
			"disable_rounded_total": 0,
			"exp_claim_approval_notification_template": "Expense Claim Approval Notification",
			"expense_approver_mandatory_in_expense_claim": 1,
		})
		hr_settings.insert(ignore_permissions=True)


def create_default_roles():
	"""Create default roles for AspireHR"""
	roles = [
		{"role_name": "HR Manager", "desk_access": 1},
		{"role_name": "HR User", "desk_access": 1},
		{"role_name": "Employee", "desk_access": 1},
		{"role_name": "Leave Approver", "desk_access": 1},
		{"role_name": "Expense Approver", "desk_access": 1},
		{"role_name": "Payroll Manager", "desk_access": 1},
		{"role_name": "Payroll User", "desk_access": 1},
		{"role_name": "Recruitment Manager", "desk_access": 1},
		{"role_name": "Training Manager", "desk_access": 1},
	]
	
	for role_data in roles:
		if not frappe.db.exists("Role", role_data["role_name"]):
			role = frappe.new_doc("Role")
			role.update(role_data)
			role.insert(ignore_permissions=True)


def create_default_leave_types():
	"""Create default leave types"""
	leave_types = [
		{
			"leave_type_name": "Annual Leave",
			"max_leaves_allowed": 21,
			"applicable_after": 90,
			"is_earned_leave": 1,
			"earned_leave_frequency": "Monthly",
			"rounding": 0.5,
		},
		{
			"leave_type_name": "Sick Leave",
			"max_leaves_allowed": 12,
			"applicable_after": 30,
		},
		{
			"leave_type_name": "Casual Leave", 
			"max_leaves_allowed": 7,
			"applicable_after": 30,
		},
		{
			"leave_type_name": "Maternity Leave",
			"max_leaves_allowed": 180,
			"applicable_after": 180,
		},
		{
			"leave_type_name": "Paternity Leave",
			"max_leaves_allowed": 15,
			"applicable_after": 180,
		},
		{
			"leave_type_name": "Compensatory Off",
			"is_compensatory": 1,
		},
	]
	
	for leave_type_data in leave_types:
		if not frappe.db.exists("Leave Type", leave_type_data["leave_type_name"]):
			leave_type = frappe.new_doc("Leave Type")
			leave_type.update(leave_type_data)
			leave_type.insert(ignore_permissions=True)


def create_default_salary_components():
	"""Create default salary components"""
	salary_components = [
		{
			"salary_component": "Basic",
			"type": "Earning",
			"description": "Basic Salary",
		},
		{
			"salary_component": "House Rent Allowance",
			"type": "Earning", 
			"description": "House Rent Allowance",
		},
		{
			"salary_component": "Dearness Allowance",
			"type": "Earning",
			"description": "Dearness Allowance",
		},
		{
			"salary_component": "Transport Allowance",
			"type": "Earning",
			"description": "Transport Allowance",
		},
		{
			"salary_component": "Medical Allowance",
			"type": "Earning",
			"description": "Medical Allowance",
		},
		{
			"salary_component": "Professional Tax",
			"type": "Deduction",
			"description": "Professional Tax",
		},
		{
			"salary_component": "Tax Deducted at Source",
			"type": "Deduction",
			"description": "Tax Deducted at Source",
		},
		{
			"salary_component": "Provident Fund",
			"type": "Deduction",
			"description": "Provident Fund",
		},
		{
			"salary_component": "Employee State Insurance",
			"type": "Deduction",
			"description": "Employee State Insurance",
		},
	]
	
	for component_data in salary_components:
		if not frappe.db.exists("Salary Component", component_data["salary_component"]):
			component = frappe.new_doc("Salary Component")
			component.update(component_data)
			component.insert(ignore_permissions=True)


def create_default_departments():
	"""Create default departments"""
	departments = [
		"Human Resources",
		"Finance", 
		"Information Technology",
		"Sales",
		"Marketing",
		"Operations",
		"Administration",
		"Legal",
		"Research and Development",
	]
	
	for dept_name in departments:
		if not frappe.db.exists("Department", dept_name):
			dept = frappe.new_doc("Department")
			dept.department_name = dept_name
			dept.insert(ignore_permissions=True)


def create_default_designations():
	"""Create default designations"""
	designations = [
		"Chief Executive Officer",
		"Chief Technology Officer", 
		"Chief Financial Officer",
		"Vice President",
		"General Manager",
		"Assistant General Manager",
		"Manager",
		"Assistant Manager",
		"Team Lead",
		"Senior Software Engineer",
		"Software Engineer",
		"Junior Software Engineer",
		"Senior Analyst",
		"Analyst",
		"Associate",
		"Executive",
		"Senior Executive",
		"Trainee",
		"Intern",
	]
	
	for designation_name in designations:
		if not frappe.db.exists("Designation", designation_name):
			designation = frappe.new_doc("Designation")
			designation.designation_name = designation_name
			designation.insert(ignore_permissions=True)


def create_default_employment_types():
	"""Create default employment types"""
	employment_types = [
		"Full-time",
		"Part-time", 
		"Contract",
		"Internship",
		"Temporary",
		"Consultant",
	]
	
	for emp_type in employment_types:
		if not frappe.db.exists("Employment Type", emp_type):
			employment_type = frappe.new_doc("Employment Type")
			employment_type.employee_type_name = emp_type
			employment_type.insert(ignore_permissions=True)
