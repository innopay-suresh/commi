try:
	import frappe
	from frappe import _
except ImportError:
	# Handle case when frappe is not available (e.g., during development)
	class MockFrappe:
		def __init__(self):
			self.session = type('obj', (object,), {'user': 'Administrator'})()
			self.db = type('obj', (object,), {
				'get_value': lambda *args, **kwargs: None,
				'get_all': lambda *args, **kwargs: [],
			})()
		
		def throw(self, msg):
			raise Exception(msg)
		
		def get_roles(self, user):
			return ["Administrator"]
	
	frappe = MockFrappe()
	
	def _(text):
		return text


def validate_salary_slip(doc, method):
	"""Validate salary slip before save"""
	if not doc.employee:
		frappe.throw(_("Employee is mandatory"))
	
	if not doc.start_date or not doc.end_date:
		frappe.throw(_("Start Date and End Date are mandatory"))
	
	if doc.start_date > doc.end_date:
		frappe.throw(_("Start Date cannot be greater than End Date"))


def on_submit_salary_slip(doc, method):
	"""Actions to perform when salary slip is submitted"""
	# Create Journal Entry for salary payment
	create_salary_payment_entry(doc)


def create_salary_payment_entry(salary_slip):
	"""Create journal entry for salary payment"""
	pass


def process_auto_salary_structure():
	"""Process automatic salary structure updates"""
	pass


def get_permission_query_conditions_for_salary_slip(user):
	"""Get permission query conditions for salary slip"""
	if not user:
		user = frappe.session.user
	
	if "HR Manager" in frappe.get_roles(user) or "Accounts Manager" in frappe.get_roles(user):
		return ""
	
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if employee:
		return f"(`tabSalary Slip`.employee = '{employee}')"
	
	return "1=0"


def has_permission(doc, user):
	"""Check if user has permission for the salary slip document"""
	if not user:
		user = frappe.session.user
	
	user_roles = frappe.get_roles(user)
	if "HR Manager" in user_roles or "Accounts Manager" in user_roles:
		return True
	
	if hasattr(doc, 'employee') and doc.employee:
		employee_user = frappe.db.get_value("Employee", doc.employee, "user_id")
		if employee_user == user:
			return True
	
	return False


def calculate_salary_components(employee, salary_structure, start_date, end_date):
	"""Calculate salary components for an employee"""
	pass


def calculate_tax_deductions(gross_pay, employee):
	"""Calculate tax deductions based on gross pay and employee details"""
	pass


def calculate_annual_eligible_hra_exemption(annual_hra, annual_basic, monthly_house_rent, rented_in_metro_city):
	"""Calculate HRA exemption (can be overridden by regional modules)"""
	pass


def calculate_hra_exemption(hra_amount, basic_salary, house_rent, metro_city):
	"""Calculate HRA exemption (can be overridden by regional modules)"""
	pass
