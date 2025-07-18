try:
	import frappe
except ImportError:
	# Handle case when frappe is not available (e.g., during development)
	class MockFrappe:
		def __init__(self):
			pass
	
	frappe = MockFrappe()


def get_notification_config():
	"""Get notification configuration for AspireHR"""
	
	config = {
		"for_doctype": {
			"Employee": {"seen": 0},
			"Leave Application": {"status": "Open"},
			"Expense Claim": {"approval_status": "Draft"},
			"Job Applicant": {"status": "Open"},
			"Interview": {"status": "Pending"},
			"Training Program": {"status": "Completed"},
			"Appraisal": {"status": "Draft"},
			"Employee Onboarding": {"boarding_status": "Pending"},
			"Employee Separation": {"boarding_status": "Pending"},
		},
		"targets": {
			"Employee": {
				"filters": [
					{
						"fieldname": "status",
						"fieldtype": "Select", 
						"options": ["Active", "Inactive", "Left"]
					}
				],
				"color_field": "status",
				"color_field_map": {
					"Active": "green",
					"Inactive": "orange", 
					"Left": "red"
				}
			},
			"Leave Application": {
				"filters": [
					{
						"fieldname": "status",
						"fieldtype": "Select",
						"options": ["Open", "Approved", "Rejected", "Cancelled"]
					}
				],
				"color_field": "status",
				"color_field_map": {
					"Open": "orange",
					"Approved": "green",
					"Rejected": "red",
					"Cancelled": "gray"
				}
			},
			"Expense Claim": {
				"filters": [
					{
						"fieldname": "approval_status", 
						"fieldtype": "Select",
						"options": ["Draft", "Approved", "Rejected", "Cancelled"]
					}
				],
				"color_field": "approval_status",
				"color_field_map": {
					"Draft": "orange",
					"Approved": "green", 
					"Rejected": "red",
					"Cancelled": "gray"
				}
			}
		}
	}
	
	return config
