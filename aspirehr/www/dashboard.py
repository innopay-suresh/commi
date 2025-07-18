import frappe

def get_context(context):
	# Fetch the current user's full name
	user_fullname = frappe.db.get_value("User", frappe.session.user, "full_name")

	context.user_fullname = user_fullname if user_fullname else frappe.session.user

	# Add dashboard cards data
	context.dashboard_cards = [
		{
			"label": "Add Employee",
			"icon": "fas fa-user-plus",
			"route": "Form/Employee",
			"color_class": "color-blue"
		},
		{
			"label": "Update Payroll Data",
			"icon": "fas fa-coins",
			"route": "update-payroll-data", # Replace with actual route
			"color_class": "color-orange"
		},
		{
			"label": "Process Payroll",
			"icon": "fas fa-calculator",
			"route": "Process Payroll", # Replace with actual route
			"color_class": "color-purple"
		},
		# Add more card data as needed
	]

