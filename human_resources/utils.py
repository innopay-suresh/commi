try:
	import frappe
	from frappe import _
	from frappe.utils import getdate, today, add_years, cint, nowdate
except ImportError:
	# Handle case when frappe is not available (e.g., during development)
	import datetime
	
	class MockFrappe:
		def __init__(self):
			self.session = type('obj', (object,), {'user': 'Administrator'})()
			self.db = type('obj', (object,), {
				'get_value': lambda *args, **kwargs: None,
				'sql': lambda *args, **kwargs: [[0]],
				'exists': lambda *args, **kwargs: False,
				'commit': lambda: None
			})()
			self.utils = type('obj', (object,), {
				'cint': lambda x: int(x) if x else 0
			})()
		
		def throw(self, msg):
			raise Exception(msg)
		
		def get_roles(self, user):
			return ["Administrator"]
		
		def get_all(self, doctype, **kwargs):
			return []
		
		def get_doc(self, doctype, name=None):
			return type('obj', (object,), {'name': name or 'test'})()
		
		def new_doc(self, doctype):
			return type('obj', (object,), {
				'insert': lambda **kwargs: None,
				'submit': lambda: None,
				'update': lambda data: None,
				'save': lambda: None,
				'cancel': lambda: None
			})()
		
		def copy_doc(self, doc):
			return self.new_doc("Test")
		
		def log_error(self, msg):
			print(f"Error: {msg}")
		
		def publish_realtime(self, *args, **kwargs):
			pass
		
		def get_cached_doc(self, doctype):
			return self.new_doc(doctype)
		
		def has_permission(self, doctype, ptype="read"):
			return True
	
	def log_event(self, *args, **kwargs):
		pass

	frappe = MockFrappe()
	
	def _(text):
		return text
	
	def getdate(date_str):
		if isinstance(date_str, str):
			return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
		return date_str
	
	def today():
		return datetime.date.today().strftime("%Y-%m-%d")
	
	def add_years(date, years):
		if isinstance(date, str):
			date = getdate(date)
		return date.replace(year=date.year + years)
	
	def cint(value):
		return int(value) if value else 0

	def nowdate():
		return datetime.date.today().strftime("%Y-%m-%d")


def check_app_permission():
	"""Check if user has permission to access AspireHR app"""
	if frappe.session.user == "Administrator":
		return True
	
	# Check if user has any HR related roles
	user_roles = frappe.get_roles(frappe.session.user)
	hr_roles = ["HR Manager", "HR User", "Employee", "Leave Approver", "Expense Approver"]
	
	return bool(set(user_roles) & set(hr_roles))


def validate_employee(doc, method):
	"""Validate employee data"""
	if not doc.employee_name:
		frappe.throw(_("Employee Name is mandatory"))
	
	if not doc.company:
		frappe.throw(_("Company is mandatory"))


def update_employee_work_history(doc, method):
	"""Update employee work history when employee is updated"""
	pass


def create_employee_from_user(doc, method):
	"""Create employee record when user is created"""
	pass


def validate_attendance(doc, method):
	"""Validate attendance data"""
	if doc.status == "Present" and not doc.in_time:
		frappe.throw(_("In Time is mandatory for Present attendance"))


def validate_leave_application(doc, method):
	"""Validate leave application"""
	if doc.from_date > doc.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"))


def on_submit_leave_application(doc, method):
	"""Actions to perform when leave application is submitted"""
	pass


def send_daily_attendance_reminder():
	"""Send daily attendance reminder to employees"""
	pass


def mark_absent_employees():
	"""Mark employees as absent if they haven't marked attendance"""
	pass


def auto_attendance_marking():
	"""Auto mark attendance based on employee checkin/checkout"""
	pass


def send_birthday_reminders():
	"""Send birthday reminders"""
	pass


def send_work_anniversary_reminders():
	"""Send work anniversary reminders"""
	pass


def weekly_off_attendance():
	"""Mark weekly off attendance"""
	pass


def monthly_attendance_sheet():
	"""Generate monthly attendance sheet"""
	pass


def get_permission_query_conditions_for_employee(user):
	"""Get permission query conditions for employee"""
	if not user:
		user = frappe.session.user
	
	if "HR Manager" in frappe.get_roles(user):
		return ""
	
	return f"(`tabEmployee`.user_id = '{user}' or `tabEmployee`.reports_to in (select name from `tabEmployee` where user_id = '{user}'))"


def get_permission_query_conditions_for_attendance(user):
	"""Get permission query conditions for attendance"""
	if not user:
		user = frappe.session.user
	
	if "HR Manager" in frappe.get_roles(user):
		return ""
	
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if employee:
		return f"(`tabAttendance`.employee = '{employee}')"
	
	return "1=0"


def get_permission_query_conditions_for_leave_application(user):
	"""Get permission query conditions for leave application"""
	if not user:
		user = frappe.session.user
	
	if "HR Manager" in frappe.get_roles(user):
		return ""
	
	employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
	if employee:
		return f"(`tabLeave Application`.employee = '{employee}')"
	
	return "1=0"


def has_permission(doc, user):
	"""Check if user has permission for the document"""
	if not user:
		user = frappe.session.user
	
	if "HR Manager" in frappe.get_roles(user):
		return True
	
	if hasattr(doc, 'employee') and doc.employee:
		employee_user = frappe.db.get_value("Employee", doc.employee, "user_id")
		if employee_user == user:
			return True
	
	return False


def get_employee_name(employee):
	"""Get employee name from employee ID"""
	if not employee:
		return ""
	
	return frappe.db.get_value("Employee", employee, "employee_name") or ""


def get_department_name(department):
	"""Get department name from department ID"""
	if not department:
		return ""
	
	return frappe.db.get_value("Department", department, "department_name") or ""


def get_designation_name(designation):
	"""Get designation name from designation ID"""
	if not designation:
		return ""
	
	return frappe.db.get_value("Designation", designation, "designation_name") or ""


def allocate_leaves_on_onboarding(employee_doc):
	"""Allocate leaves automatically during employee onboarding (Employee creation)."""
	if employee_doc.status != "Active" or employee_doc.relieving_date and getdate(employee_doc.relieving_date) <= getdate(nowdate()):
		return

	joining_date = getdate(employee_doc.date_of_joining) if employee_doc.date_of_joining else getdate(nowdate())

	leave_types = frappe.get_all("Leave Type",
		filters={"auto_allocate": 1, "is_active": 1},
		fields=["name", "allocation_frequency", "allocation_amount", "is_earned_leave", "earned_leave_frequency"]
	)

	for leave_type in leave_types:
		allocation_amount = cint(leave_type.allocation_amount)
		if allocation_amount <= 0:
			continue

		if leave_type.allocation_frequency == "Yearly":
			from_date = getdate(f"{joining_date.year}-01-01")
			to_date = getdate(f"{joining_date.year}-12-31")

			existing_allocation = frappe.db.exists("Leave Allocation", {
				"employee": employee_doc.name,
				"leave_type": leave_type.name,
				"from_date": from_date,
				"to_date": to_date,
				"docstatus": ["!=", 2]
			})

			if not existing_allocation:
				create_leave_allocation_record(employee_doc.name, leave_type.name, from_date, to_date, allocation_amount, "Onboarding")

		elif leave_type.allocation_frequency == "Monthly" and leave_type.is_earned_leave and leave_type.earned_leave_frequency == "Monthly":
			# For monthly earned leaves on onboarding, allocate for the current month
			from_date = getdate(f"{joining_date.year}-{joining_date.month:02d}-01")
			import calendar
			last_day = calendar.monthrange(joining_date.year, joining_date.month)[1]
			to_date = getdate(f"{joining_date.year}-{joining_date.month:02d}-{last_day}")

			existing_allocation = frappe.db.exists("Leave Allocation", {
				"employee": employee_doc.name,
				"leave_type": leave_type.name,
				"from_date": from_date,
				"to_date": to_date,
				"docstatus": ["!=", 2]
			})

			if not existing_allocation:
				create_leave_allocation_record(employee_doc.name, leave_type.name, from_date, to_date, allocation_amount, "Onboarding")


def allocate_scheduled_leaves():
	"""Allocate leaves monthly/annually for all active employees based on configuration."""
	today_date = getdate(nowdate())

	active_employees = frappe.get_all("Employee",
		filters={"status": "Active", "relieving_date": ["is", "not set"]},
		fields=["name", "date_of_joining"]
	)

	leave_types = frappe.get_all("Leave Type",
		filters={"auto_allocate": 1, "is_active": 1},
		fields=["name", "allocation_frequency", "allocation_amount", "is_earned_leave", "earned_leave_frequency"]
	)

	for employee in active_employees:
		employee_doc = frappe.get_doc("Employee", employee.name)
		joining_date = getdate(employee_doc.date_of_joining) if employee_doc.date_of_joining else None

		for leave_type in leave_types:
			allocation_amount = cint(leave_type.allocation_amount)
			if allocation_amount <= 0:
				continue

			if leave_type.allocation_frequency == "Yearly" and today_date.month == 1 and today_date.day == 1:
				from_date = getdate(f"{today_date.year}-01-01")
				to_date = getdate(f"{today_date.year}-12-31")

				existing_allocation = frappe.db.exists("Leave Allocation", {
					"employee": employee.name,
					"leave_type": leave_type.name,
					"from_date": from_date,
					"to_date": to_date,
					"docstatus": ["!=", 2]
				})

				if not existing_allocation:
					create_leave_allocation_record(employee.name, leave_type.name, from_date, to_date, allocation_amount, "Scheduled Yearly Allocation")

			elif leave_type.allocation_frequency == "Monthly" and leave_type.is_earned_leave and leave_type.earned_leave_frequency == "Monthly" and joining_date and today_date.day == joining_date.day: # Allocate on the joining day of each month
				from_date = getdate(f"{today_date.year}-{today_date.month:02d}-{1}")
				import calendar
				last_day = calendar.monthrange(today_date.year, today_date.month)[1]
				to_date = getdate(f"{today_date.year}-{today_date.month:02d}-{last_day}")

				existing_allocation = frappe.db.exists("Leave Allocation", {
					"employee": employee.name,
					"leave_type": leave_type.name,
					"from_date": from_date,
					"to_date": to_date,
					"docstatus": ["!=", 2]
				})

				if not existing_allocation:
					create_leave_allocation_record(employee.name, leave_type.name, from_date, to_date, allocation_amount, "Scheduled Monthly Allocation")


def create_leave_allocation_record(employee, leave_type, from_date, to_date, allocated_leaves, allocation_type):
	"""Creates a Leave Allocation and a Leave Allocation Log record."""
	try:
		allocation_doc = frappe.new_doc("Leave Allocation")
		allocation_doc.employee = employee
		allocation_doc.leave_type = leave_type
		allocation_doc.from_date = from_date
		allocation_doc.to_date = to_date
		allocation_doc.new_leaves_allocated = allocated_leaves
		allocation_doc.save()
		allocation_doc.submit()

		log_allocation(employee, leave_type, from_date, to_date, allocated_leaves, allocation_type, allocation_doc.name)
		frappe.log_event(f"Leave Allocation created for {employee} - {leave_type} ({allocated_leaves} leaves) for period {from_date} to {to_date}")

	except Exception as e:
		frappe.log_error(f"Error creating Leave Allocation for {employee} - {leave_type}: {str(e)}")
		# Log the failure in the custom log doctype as well
		log_allocation(employee, leave_type, from_date, to_date, allocated_leaves, allocation_type, None, str(e))


def log_allocation(employee, leave_type, from_date, to_date, allocated_leaves, allocation_type, leave_allocation_doc=None, error_message=None):
	"""Logs automatic leave allocation in the Leave Allocation Log DocType."""
	try:
		log_doc = frappe.new_doc("Leave Allocation Log")
		log_doc.employee = employee
		log_doc.leave_type = leave_type
		log_doc.from_date = from_date
		log_doc.to_date = to_date
		log_doc.allocated_leaves = allocated_leaves
		log_doc.allocation_type = allocation_type
		log_doc.leave_allocation = leave_allocation_doc
		log_doc.status = "Success" if not error_message else "Failed"
		log_doc.error_message = error_message
		log_doc.save()

	except Exception as e:
		frappe.log_error(f"Error logging Leave Allocation for {employee} - {leave_type}: {str(e)}")



def allocate_leaves_dynamically(employee=None, leave_type=None, allocation_date=None, new_leaves_allocated=None, carry_forward=False):
	"""
	Dynamically allocate leaves for employees on custom dates
	
	Args:
		employee (str): Employee ID (if None, applies to all employees)
		leave_type (str): Leave Type (if None, applies to all leave types)
		allocation_date (str): Date for the allocation (if None, uses current date)
		new_leaves_allocated (float): Number of leaves to allocate
		carry_forward (bool): Whether to carry forward unused leaves
	"""
	
	if not allocation_date:
		allocation_date = today()
	
	allocation_date = getdate(allocation_date)
	
	# Get employees to process
	employees = []
	if employee:
		employees = [employee]
	else:
		employees = frappe.get_all("Employee", 
			filters={"status": "Active"}, 
			fields=["name"]
		)
		employees = [emp.name for emp in employees]
	
	# Get leave types to process
	leave_types = []
	if leave_type:
		leave_types = [leave_type]
	else:
		leave_types = frappe.get_all("Leave Type", 
			filters={"is_active": 1}, 
			fields=["name"]
		)
		leave_types = [lt.name for lt in leave_types]
	
	processed_allocations = []
	
	for emp in employees:
		for lt in leave_types:
			try:
				allocation = create_or_update_leave_allocation(
					emp, lt, allocation_date, new_leaves_allocated, carry_forward
				)
				if allocation:
					processed_allocations.append({
						"employee": emp,
						"leave_type": lt,
						"allocation": allocation.name,
						"leaves_allocated": allocation.new_leaves_allocated
					})
			except Exception as e:
				frappe.log_error(f"Error allocating leaves for {emp} - {lt}: {str(e)}")
				continue
	
	return processed_allocations


def create_or_update_leave_allocation(employee, leave_type, allocation_date, new_leaves_allocated, carry_forward=False):
	"""Create or update leave allocation for specific employee and leave type"""
	
	allocation_date = getdate(allocation_date)
	from_date = allocation_date
	to_date = add_years(from_date, 1)
	
	# Check if allocation already exists for this period
	existing_allocation = frappe.db.get_value("Leave Allocation", {
		"employee": employee,
		"leave_type": leave_type,
		"from_date": ["<=", allocation_date],
		"to_date": [">=", allocation_date],
		"docstatus": ["!=", 2]
	})
	
	if existing_allocation:
		# Update existing allocation
		allocation_doc = frappe.get_doc("Leave Allocation", existing_allocation)
		
		if new_leaves_allocated is not None:
			allocation_doc.new_leaves_allocated = new_leaves_allocated
		
		if carry_forward:
			# Calculate carry forward leaves
			carry_forward_leaves = get_carry_forward_leaves(employee, leave_type, allocation_date)
			allocation_doc.carry_forward = 1
			allocation_doc.carry_forwarded_leaves = carry_forward_leaves
		
		allocation_doc.save()
		if allocation_doc.docstatus == 0:
			allocation_doc.submit()
		
		return allocation_doc
	else:
		# Create new allocation
		allocation_doc = frappe.new_doc("Leave Allocation")
		allocation_doc.update({
			"employee": employee,
			"leave_type": leave_type,
			"from_date": from_date,
			"to_date": to_date,
			"new_leaves_allocated": new_leaves_allocated or 0,
			"carry_forward": carry_forward
		})
		
		if carry_forward:
			carry_forward_leaves = get_carry_forward_leaves(employee, leave_type, allocation_date)
			allocation_doc.carry_forwarded_leaves = carry_forward_leaves
		
		allocation_doc.insert()
		allocation_doc.submit()
		
		return allocation_doc


def get_carry_forward_leaves(employee, leave_type, allocation_date):
	"""Calculate carry forward leaves from previous allocation"""
	
	allocation_date = getdate(allocation_date)
	previous_year_start = add_years(allocation_date, -1)
	
	# Get previous allocation
	previous_allocation = frappe.db.get_value("Leave Allocation", {
		"employee": employee,
		"leave_type": leave_type,
		"from_date": ["<=", previous_year_start],
		"to_date": [">=", previous_year_start],
		"docstatus": 1
	}, ["name", "total_leaves_allocated"])
	
	if not previous_allocation:
		return 0
	
	# Calculate used leaves in previous period
	used_leaves = frappe.db.sql("""
		SELECT COALESCE(SUM(total_leave_days), 0) as used_leaves
		FROM `tabLeave Application`
		WHERE employee = %s 
		AND leave_type = %s
		AND from_date >= %s
		AND to_date <= %s
		AND docstatus = 1
	""", (employee, leave_type, previous_year_start, allocation_date))[0][0]
	
	# Calculate carry forward (allocated - used)
	total_allocated = previous_allocation[1] if previous_allocation else 0
	carry_forward = max(0, total_allocated - used_leaves)
	
	# Check leave type carry forward limits
	leave_type_doc = frappe.get_doc("Leave Type", leave_type)
	if leave_type_doc.max_carry_forwarded_leaves > 0:
		carry_forward = min(carry_forward, leave_type_doc.max_carry_forwarded_leaves)
	
	return carry_forward


def bulk_leave_allocation(allocation_data):
	"""
	Bulk allocate leaves for multiple employees
	
	Args:
		allocation_data (list): List of dictionaries containing allocation details
		Example: [
			{
				"employee": "EMP-001",
				"leave_type": "Annual Leave",
				"allocation_date": "2024-01-01",
				"new_leaves_allocated": 21,
				"carry_forward": True
			}
		]
	"""
	processed = []
	failed = []
	
	for data in allocation_data:
		try:
			result = allocate_leaves_dynamically(
				employee=data.get("employee"),
				leave_type=data.get("leave_type"),
				allocation_date=data.get("allocation_date"),
				new_leaves_allocated=data.get("new_leaves_allocated"),
				carry_forward=data.get("carry_forward", False)
			)
			processed.extend(result)
		except Exception as e:
			failed.append({
				"data": data,
				"error": str(e)
			})
			frappe.log_error(f"Bulk allocation failed for {data}: {str(e)}")
	
	return {
		"processed": processed,
		"failed": failed
	}


def adjust_leave_allocation(employee, leave_type, adjustment_date, adjustment_amount, reason=None):
	"""
	Adjust existing leave allocation by adding or subtracting leaves
	
	Args:
		employee (str): Employee ID
		leave_type (str): Leave Type
		adjustment_date (str): Date of adjustment
		adjustment_amount (float): Amount to adjust (positive for addition, negative for deduction)
		reason (str): Reason for adjustment
	"""
	
	adjustment_date = getdate(adjustment_date)
	
	# Find active allocation for the adjustment date
	allocation = frappe.db.get_value("Leave Allocation", {
		"employee": employee,
		"leave_type": leave_type,
		"from_date": ["<=", adjustment_date],
		"to_date": [">=", adjustment_date],
		"docstatus": 1
	})
	
	if not allocation:
		frappe.throw(_("No active leave allocation found for {0} - {1} on {2}").format(
			employee, leave_type, adjustment_date
		))
	
	allocation_doc = frappe.get_doc("Leave Allocation", allocation)
	
	# Calculate new allocation
	new_allocation = allocation_doc.new_leaves_allocated + adjustment_amount
	
	if new_allocation < 0:
		frappe.throw(_("Adjustment would result in negative leave allocation"))
	
	# Cancel and amend the allocation
	allocation_doc.cancel()
	
	amended_allocation = frappe.copy_doc(allocation_doc)
	amended_allocation.new_leaves_allocated = new_allocation
	amended_allocation.amended_from = allocation_doc.name
	
	if reason:
		amended_allocation.add_comment("Comment", f"Adjusted by {adjustment_amount} leaves. Reason: {reason}")
	
	amended_allocation.insert()
	amended_allocation.submit()
	
	return amended_allocation


def schedule_leave_allocation(schedule_date, employee=None, leave_type=None, leaves_to_allocate=None):
	"""
	Schedule future leave allocation
	This can be used with scheduler to automatically allocate leaves on specific dates
	"""
	
	schedule_date = getdate(schedule_date)
	
	if schedule_date <= getdate(today()):
		# Execute immediately if schedule date is today or past
		return allocate_leaves_dynamically(
			employee=employee,
			leave_type=leave_type,
			allocation_date=schedule_date,
			new_leaves_allocated=leaves_to_allocate
		)
	else:
		# Create a scheduled job (you might want to use a custom doctype for this)
		frappe.log_error(f"Scheduled leave allocation for {schedule_date} - Feature needs custom implementation")
		return None


def get_leave_balance_on_date(employee, leave_type, as_on_date):
	"""Get leave balance for an employee on a specific date"""
	
	as_on_date = getdate(as_on_date)
	
	# Get total allocated leaves up to the date
	allocated = frappe.db.sql("""
		SELECT COALESCE(SUM(total_leaves_allocated), 0) as total_allocated
		FROM `tabLeave Allocation`
		WHERE employee = %s 
		AND leave_type = %s
		AND from_date <= %s
		AND docstatus = 1
	""", (employee, leave_type, as_on_date))[0][0]
	
	# Get total used leaves up to the date
	used = frappe.db.sql("""
		SELECT COALESCE(SUM(total_leave_days), 0) as total_used
		FROM `tabLeave Application`
		WHERE employee = %s 
		AND leave_type = %s
		AND from_date <= %s
		AND docstatus = 1
	""", (employee, leave_type, as_on_date))[0][0]
	
	return allocated - used


def annual_leave_allocation():
	"""Automatically allocate annual leaves at the beginning of year"""
	
	today_date = getdate(today())
	
	# Check if it's January 1st
	if today_date.month == 1 and today_date.day == 1:
		# Get all active employees
		employees = frappe.get_all("Employee", 
			filters={"status": "Active"}, 
			fields=["name"]
		)
		
		# Get leave types that should be allocated annually
		leave_types = frappe.get_all("Leave Type", 
			filters={"is_active": 1, "is_earned_leave": 0}, 
			fields=["name", "max_leaves_allowed"]
		)
		
		for employee in employees:
			for leave_type in leave_types:
				try:
					allocate_leaves_dynamically(
						employee=employee.name,
						leave_type=leave_type.name,
						allocation_date=today(),
						new_leaves_allocated=leave_type.max_leaves_allowed,
						carry_forward=True
					)
				except Exception as e:
					frappe.log_error(f"Annual allocation failed for {employee.name} - {leave_type.name}: {str(e)}")


def monthly_leave_allocation():
	"""Process monthly earned leave allocation"""
	
	# Get leave types that are earned monthly
	earned_leave_types = frappe.get_all("Leave Type", 
		filters={"is_active": 1, "is_earned_leave": 1, "earned_leave_frequency": "Monthly"}, 
		fields=["name", "max_leaves_allowed", "rounding"]
	)
	
	if not earned_leave_types:
		return
	
	# Get all active employees
	employees = frappe.get_all("Employee", 
		filters={"status": "Active"}, 
		fields=["name", "date_of_joining"]
	)
	
	today_date = getdate(today())
	
	for employee in employees:
		# Check if employee has completed probation period
		if employee.date_of_joining:
			join_date = getdate(employee.date_of_joining)
			months_completed = (today_date.year - join_date.year) * 12 + (today_date.month - join_date.month)
			
			if months_completed < 6:  # Skip if less than 6 months
				continue
		
		for leave_type in earned_leave_types:
			try:
				# Calculate monthly earned leaves
				annual_leaves = leave_type.max_leaves_allowed or 21
				monthly_leaves = annual_leaves / 12
				
				if leave_type.rounding:
					monthly_leaves = round(monthly_leaves, leave_type.rounding)
				
				# Check if allocation already exists for this month
				existing = frappe.db.get_value("Leave Allocation", {
					"employee": employee.name,
					"leave_type": leave_type.name,
					"from_date": [">=", f"{today_date.year}-{today_date.month:02d}-01"],
					"from_date": ["<", f"{today_date.year}-{today_date.month + 1:02d}-01"],
					"docstatus": ["!=", 2]
				})
				
				if not existing:
					create_or_update_leave_allocation(
						employee=employee.name,
						leave_type=leave_type.name,
						allocation_date=today(),
						new_leaves_allocated=monthly_leaves,
						carry_forward=False
					)
			except Exception as e:
				frappe.log_error(f"Monthly allocation failed for {employee.name} - {leave_type.name}: {str(e)}")


def process_scheduled_leave_allocations():
	"""Process any scheduled leave allocations (this could be extended with a custom doctype)"""
	# This is a placeholder for future implementation
	# You could create a "Scheduled Leave Allocation" doctype to store future allocations
	# and process them here when their date arrives
	pass
