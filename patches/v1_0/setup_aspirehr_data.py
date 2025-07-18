try:
	import frappe
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
				'update': lambda data: None,
				'set': lambda key, value: None
			})()
	
	frappe = MockFrappe()


def execute():
	"""Setup initial AspireHR data and configurations"""
	
	# Create default HR settings if not exists
	setup_hr_settings()
	
	# Create default notification templates
	setup_notification_templates()
	
	# Setup default custom fields
	setup_custom_fields()
	
	# Setup default workflows
	setup_workflows()
	
	frappe.db.commit()


def setup_hr_settings():
	"""Setup default HR settings"""
	if not frappe.db.exists("HR Settings", "HR Settings"):
		hr_settings = frappe.new_doc("HR Settings")
		hr_settings.update({
			"employee_number_series": "EMP-.YYYY.-",
			"max_working_hours_against_timesheet": 10,
			"include_holidays_in_total_working_days": 0,
			"disable_rounded_total": 0,
		})
		hr_settings.insert(ignore_permissions=True)


def setup_notification_templates():
	"""Setup default email notification templates"""
	
	templates = [
		{
			"name": "Leave Application Approval",
			"subject": "Leave Application Approved - {employee_name}",
			"message": """
Dear {employee_name},

Your leave application from {from_date} to {to_date} has been approved.

Reason: {leave_type}
Days: {total_leave_days}

Please ensure proper handover before proceeding on leave.

Best regards,
HR Team
			""",
			"doctype": "Leave Application"
		},
		{
			"name": "Leave Application Rejection",
			"subject": "Leave Application Rejected - {employee_name}",
			"message": """
Dear {employee_name},

Your leave application from {from_date} to {to_date} has been rejected.

Reason for rejection: {reason}

Please contact HR for further clarification.

Best regards,
HR Team
			""",
			"doctype": "Leave Application"
		},
		{
			"name": "Birthday Reminder",
			"subject": "Happy Birthday {employee_name}!",
			"message": """
Dear {employee_name},

Wishing you a very Happy Birthday! 🎉

May this special day bring you joy, happiness, and success.

Best wishes,
AspireHR Team
			""",
			"doctype": "Employee"
		}
	]
	
	for template_data in templates:
		if not frappe.db.exists("Email Template", template_data["name"]):
			template = frappe.new_doc("Email Template")
			template.update(template_data)
			template.insert(ignore_permissions=True)


def setup_custom_fields():
	"""Setup custom fields for AspireHR"""
	
	custom_fields = [
		{
			"doctype": "Employee",
			"fieldname": "aspirehr_employee_id",
			"label": "AspireHR Employee ID",
			"fieldtype": "Data",
			"unique": 1,
			"insert_after": "employee"
		},
		{
			"doctype": "Employee", 
			"fieldname": "emergency_contact_section",
			"label": "Emergency Contact",
			"fieldtype": "Section Break",
			"insert_after": "personal_details"
		},
		{
			"doctype": "Employee",
			"fieldname": "emergency_contact_name",
			"label": "Emergency Contact Name",
			"fieldtype": "Data",
			"insert_after": "emergency_contact_section"
		},
		{
			"doctype": "Employee",
			"fieldname": "emergency_contact_relation",
			"label": "Relation",
			"fieldtype": "Select",
			"options": "Father\nMother\nSpouse\nSibling\nChild\nOther",
			"insert_after": "emergency_contact_name"
		},
		{
			"doctype": "Employee",
			"fieldname": "emergency_contact_phone",
			"label": "Emergency Contact Phone",
			"fieldtype": "Phone",
			"insert_after": "emergency_contact_relation"
		}
	]
	
	for field_data in custom_fields:
		create_custom_field(field_data)


def create_custom_field(field_data):
	"""Create custom field if it doesn't exist"""
	field_name = f"{field_data['doctype']}-{field_data['fieldname']}"
	
	if not frappe.db.exists("Custom Field", field_name):
		custom_field = frappe.new_doc("Custom Field")
		custom_field.update({
			"dt": field_data["doctype"],
			"fieldname": field_data["fieldname"],
			"label": field_data["label"],
			"fieldtype": field_data["fieldtype"],
			"insert_after": field_data["insert_after"]
		})
		
		# Add additional properties if present
		for prop in ["options", "unique", "reqd", "read_only"]:
			if prop in field_data:
				custom_field.set(prop, field_data[prop])
		
		custom_field.insert(ignore_permissions=True)


def setup_workflows():
	"""Setup default workflows for AspireHR"""
	
	# Leave Application Workflow
	if not frappe.db.exists("Workflow", "Leave Application Approval"):
		workflow = frappe.new_doc("Workflow")
		workflow.update({
			"workflow_name": "Leave Application Approval",
			"document_type": "Leave Application",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"states": [
				{
					"state": "Draft",
					"allow_edit": "Employee",
					"doc_status": "0"
				},
				{
					"state": "Pending Approval",
					"allow_edit": "Leave Approver",
					"doc_status": "0"
				},
				{
					"state": "Approved",
					"allow_edit": "HR Manager",
					"doc_status": "1"
				},
				{
					"state": "Rejected",
					"allow_edit": "",
					"doc_status": "2"
				}
			],
			"transitions": [
				{
					"state": "Draft",
					"action": "Submit",
					"next_state": "Pending Approval",
					"allowed": "Employee"
				},
				{
					"state": "Pending Approval",
					"action": "Approve", 
					"next_state": "Approved",
					"allowed": "Leave Approver"
				},
				{
					"state": "Pending Approval",
					"action": "Reject",
					"next_state": "Rejected", 
					"allowed": "Leave Approver"
				}
			]
		})
		workflow.insert(ignore_permissions=True)
