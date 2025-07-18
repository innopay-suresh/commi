app_name = "aspirehr"
app_title = "AspireHR"
app_publisher = "Your Company"
app_description = "Modern HR and Payroll Management System"
app_email = "admin@yourcompany.com"
app_license = "MIT"
required_apps = ["frappe"]
source_link = "https://github.com/yourcompany/aspirehr"
app_logo_url = "/assets/aspirehr/images/aspirehr-logo.svg"
app_home = "/app/aspirehr-overview"

add_to_apps_screen = [
	{
		"name": "aspirehr",
		"logo": "/assets/aspirehr/images/aspirehr-logo.svg",
		"title": "AspireHR",
		"route": "/app/aspirehr-overview",
		"has_permission": "aspirehr.human_resources.utils.check_app_permission",
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_js = [
	"/assets/aspirehr/js/aspirehr.js",
]
app_include_css = [
	"/assets/aspirehr/css/aspirehr.css"
]

# include js in doctype views
doctype_js = {
	"Employee": "public/js/employee_list.js",
}

doctype_list_js = {
	"Employee": "public/js/employee_list.js",
}

doctype_tree_js = {}

doctype_calendar_js = {}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Employee": {
		"validate": "aspirehr.human_resources.utils.validate_employee",
		"on_update": "aspirehr.human_resources.utils.update_employee_work_history",
	},
	"User": {
		"after_insert": "aspirehr.human_resources.utils.create_employee_from_user",
	},
	"Attendance": {
		"validate": "aspirehr.human_resources.utils.validate_attendance",
	},
	"Salary Slip": {
		"validate": "aspirehr.payroll.utils.validate_salary_slip",
		"on_submit": "aspirehr.payroll.utils.on_submit_salary_slip",
	},
	"Leave Application": {
		"validate": "aspirehr.human_resources.utils.validate_leave_application",
		"on_submit": "aspirehr.human_resources.utils.on_submit_leave_application",
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"0 8 * * *": [
			"aspirehr.human_resources.utils.send_daily_attendance_reminder"
		],
		"0 18 * * *": [
			"aspirehr.human_resources.utils.mark_absent_employees"
		],
		"0 2 1 1 *": [
			"aspirehr.human_resources.utils.annual_leave_allocation"
		],
		"0 2 1 * *": [
			"aspirehr.human_resources.utils.monthly_leave_allocation"
		],
	},
	"daily": [
		"aspirehr.human_resources.utils.auto_attendance_marking",
		"aspirehr.human_resources.utils.send_birthday_reminders",
		"aspirehr.human_resources.utils.send_work_anniversary_reminders",
	],
	"weekly": [
		"aspirehr.human_resources.utils.weekly_off_attendance",
	],
	"monthly": [
		"aspirehr.payroll.utils.process_auto_salary_structure",
		"aspirehr.human_resources.utils.monthly_attendance_sheet",
		"aspirehr.human_resources.utils.process_scheduled_leave_allocations",
		# Auto leave allocation for monthly frequency
		"human_resources.utils.allocate_scheduled_leaves",
	]
}

# Testing
# -------

before_tests = "aspirehr.setup.utils.before_tests"

# Overriding Methods
# ------------------------------

override_whitelisted_methods = {
	"frappe.desk.query_report.run": "aspirehr.human_resources.query_report.run"
}

# Permissions
# -----------

permission_query_conditions = {
	"Employee": "aspirehr.human_resources.utils.get_permission_query_conditions_for_employee",
	"Salary Slip": "aspirehr.payroll.utils.get_permission_query_conditions_for_salary_slip",
	"Attendance": "aspirehr.human_resources.utils.get_permission_query_conditions_for_attendance",
	"Leave Application": "aspirehr.human_resources.utils.get_permission_query_conditions_for_leave_application",
}

has_permission = {
	"Employee": "aspirehr.human_resources.utils.has_permission",
	"Salary Slip": "aspirehr.payroll.utils.has_permission",
	"Attendance": "aspirehr.human_resources.utils.has_permission",
	"Leave Application": "aspirehr.human_resources.utils.has_permission",
}

# Website Settings
# ----------------

website_generators = ["Job Opening"]

fixtures = [
	{"dt": "Custom Field", "filters": [["name", "in", []]]},
	{"dt": "Property Setter", "filters": [["name", "in", []]]},
	{"dt": "Role", "filters": [["name", "in", ["HR Manager", "HR User", "Employee", "Leave Approver"]]]},
	{"dt": "Workflow State", "filters": [["name", "in", []]]},
	{"dt": "Workflow", "filters": [["name", "in", []]]},
]

# Installation
# ------------

after_install = "aspirehr.setup.install.after_install"
before_uninstall = "aspirehr.setup.uninstall.before_uninstall"

# Uninstallation
# --------------

before_uninstall = "aspirehr.setup.uninstall.before_uninstall"

# Boot Session
# ------------

boot_session = "aspirehr.startup.boot_session"

# Jinja Templates
# ---------------

jinja = {
	"methods": [
		"aspirehr.human_resources.utils.get_employee_name",
		"aspirehr.human_resources.utils.get_department_name",
		"aspirehr.human_resources.utils.get_designation_name",
	]
}

# Standard Portal Items
# ---------------------

standard_portal_menu_items = [
	{
		"title": "Employee Profile",
		"route": "/employee-profile",
		"reference_doctype": "Employee",
		"role": "Employee"
	},
	{
		"title": "Leave Application",
		"route": "/leave-application", 
		"reference_doctype": "Leave Application",
		"role": "Employee"
	},
	{
		"title": "Expense Claim",
		"route": "/expense-claim",
		"reference_doctype": "Expense Claim", 
		"role": "Employee"
	},
	{
		"title": "Attendance",
		"route": "/attendance",
		"reference_doctype": "Attendance",
		"role": "Employee"
	}
]

# Regional Settings
# -----------------

regional_overrides = {
	"India": {
		"aspirehr.payroll.utils.calculate_annual_eligible_hra_exemption": "aspirehr.regional.india.utils.calculate_annual_eligible_hra_exemption",
		"aspirehr.payroll.utils.calculate_hra_exemption": "aspirehr.regional.india.utils.calculate_hra_exemption"
	}
}

# Email Notifications
# -------------------

notification_config = "aspirehr.notifications.get_notification_config"

# Global Search
# -------------

global_search_doctypes = {
	"Employee": {
		"search_fields": ["employee_name", "employee_number", "personal_email", "company_email"],
		"route": ["Form", "Employee"],
		"title_field": "employee_name"
	}
}

# Translation
# ------------

# Contribution Guidelines
# -----------------------

# Apps
# ----
