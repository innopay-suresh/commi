try:
	import frappe
except ImportError:
	# Handle case when frappe is not available (e.g., during development)
	class MockFrappe:
		def __init__(self):
			self.db = type('obj', (object,), {'commit': lambda: None})()
		
		def get_all(self, *args, **kwargs):
			return []
		
		def delete_doc(self, *args, **kwargs):
			pass
	
	frappe = MockFrappe()


def before_uninstall():
	"""Clean up before uninstalling AspireHR"""
	print("Cleaning up AspireHR data...")
	
	# Remove custom fields if any
	cleanup_custom_fields()
	
	# Remove custom doctypes (optional - be careful with this)
	# cleanup_custom_doctypes()
	
	frappe.db.commit()
	print("AspireHR cleanup completed.")


def cleanup_custom_fields():
	"""Remove custom fields created by AspireHR"""
	custom_fields = frappe.get_all("Custom Field", 
		filters={"module": "AspireHR"},
		fields=["name"]
	)
	
	for cf in custom_fields:
		frappe.delete_doc("Custom Field", cf.name, ignore_permissions=True)


def cleanup_custom_doctypes():
	"""Remove custom doctypes created by AspireHR (use with caution)"""
	# This is optional and should be used carefully
	# as it will delete all data in these doctypes
	
	aspirehr_doctypes = [
		# Add your custom doctype names here if you want to remove them
		# "AspireHR Custom DocType",
	]
	
	for doctype in aspirehr_doctypes:
		if frappe.db.exists("DocType", doctype):
			frappe.delete_doc("DocType", doctype, ignore_permissions=True)
