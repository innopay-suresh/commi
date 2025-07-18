app_name = "aspirehr"
app_title = "AspireHR"
app_publisher = "Your Company"
app_description = "Modern HR and Payroll Management System"
app_email = "admin@yourcompany.com"
app_license = "MIT"
required_apps = ["frappe"]

# Minimal configuration to avoid build issues
app_include_js = []
app_include_css = []
doctype_js = {}
doctype_list_js = {}
doctype_tree_js = {}
doctype_calendar_js = {}

# Basic document events (optional)
doc_events = {}

# Installation hooks
after_install = "aspirehr.setup.install.after_install"
