try:
	import frappe
	from frappe import _
	from frappe.utils import today, getdate, cint
except ImportError:
	# Handle case when frappe is not available (e.g., during development)
	import datetime
	
	class MockFrappe:
		def __init__(self):
			self.session = type('obj', (object,), {'user': 'Administrator'})()
			self.db = type('obj', (object,), {
				'get_value': lambda *args, **kwargs: None,
				'get_all': lambda *args, **kwargs: [],
				'exists': lambda *args, **kwargs: False,
				'commit': lambda: None
			})()
			self.utils = type('obj', (object,), {
				'cint': lambda x: int(x) if x else 0
			})()
		
		def throw(self, msg):
			raise Exception(msg)
		
		def has_permission(self, doctype, ptype="read"):
			return True
		
		def log_error(self, msg):
			print(f"Error: {msg}")
		
		def whitelist(self):
			def decorator(func):
				return func
			return decorator
	
	frappe = MockFrappe()
	
	def _(text):
		return text
	
	def today():
		return datetime.date.today().strftime("%Y-%m-%d")
	
	def getdate(date_str):
		if isinstance(date_str, str):
			return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
		return date_str
	
	def cint(value):
		return int(value) if value else 0

from aspirehr.human_resources.utils import (
    allocate_leaves_dynamically,
    bulk_leave_allocation,
    adjust_leave_allocation,
    get_leave_balance_on_date
)


@frappe.whitelist()
def allocate_employee_leaves(employee=None, leave_type=None, allocation_date=None, 
                           new_leaves_allocated=None, carry_forward=False):
    """
    API endpoint to dynamically allocate leaves for employees
    
    Args:
        employee (str): Employee ID (optional - if not provided, applies to all active employees)
        leave_type (str): Leave Type (optional - if not provided, applies to all active leave types)
        allocation_date (str): Date for allocation (optional - defaults to today)
        new_leaves_allocated (float): Number of leaves to allocate
        carry_forward (bool): Whether to carry forward unused leaves from previous period
    
    Returns:
        dict: Result with processed allocations and any errors
    """
    
    # Check permissions
    if not frappe.has_permission("Leave Allocation", "create"):
        frappe.throw(_("Not permitted to create Leave Allocations"))
    
    try:
        # Convert string values to appropriate types
        if new_leaves_allocated:
            new_leaves_allocated = float(new_leaves_allocated)
        
        carry_forward = cint(carry_forward)
        
        result = allocate_leaves_dynamically(
            employee=employee,
            leave_type=leave_type, 
            allocation_date=allocation_date,
            new_leaves_allocated=new_leaves_allocated,
            carry_forward=carry_forward
        )
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Leave allocation completed successfully"),
            "data": result
        }
        
    except Exception as e:
        frappe.log_error(f"Leave allocation API error: {str(e)}")
        frappe.throw(_("Error in leave allocation: {0}").format(str(e)))


@frappe.whitelist()
def bulk_allocate_leaves(allocation_data):
    """
    API endpoint for bulk leave allocation
    
    Args:
        allocation_data (str): JSON string containing list of allocation records
        
    Example allocation_data:
    [
        {
            "employee": "EMP-001",
            "leave_type": "Annual Leave", 
            "allocation_date": "2024-01-01",
            "new_leaves_allocated": 21,
            "carry_forward": true
        }
    ]
    """
    
    # Check permissions
    if not frappe.has_permission("Leave Allocation", "create"):
        frappe.throw(_("Not permitted to create Leave Allocations"))
    
    try:
        # Parse allocation data
        if isinstance(allocation_data, str):
            import json
            allocation_data = json.loads(allocation_data)
        
        result = bulk_leave_allocation(allocation_data)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Bulk leave allocation completed"),
            "processed": result["processed"],
            "failed": result["failed"],
            "summary": {
                "total_records": len(allocation_data),
                "successful": len(result["processed"]),
                "failed": len(result["failed"])
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Bulk leave allocation API error: {str(e)}")
        frappe.throw(_("Error in bulk leave allocation: {0}").format(str(e)))


@frappe.whitelist()
def adjust_employee_leave_allocation(employee, leave_type, adjustment_date, 
                                   adjustment_amount, reason=None):
    """
    API endpoint to adjust existing leave allocation
    
    Args:
        employee (str): Employee ID
        leave_type (str): Leave Type
        adjustment_date (str): Date of adjustment
        adjustment_amount (float): Amount to adjust (positive for addition, negative for deduction)
        reason (str): Reason for adjustment (optional)
    """
    
    # Check permissions
    if not frappe.has_permission("Leave Allocation", "write"):
        frappe.throw(_("Not permitted to modify Leave Allocations"))
    
    try:
        adjustment_amount = float(adjustment_amount)
        
        result = adjust_leave_allocation(
            employee=employee,
            leave_type=leave_type,
            adjustment_date=adjustment_date,
            adjustment_amount=adjustment_amount,
            reason=reason
        )
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Leave allocation adjusted successfully"),
            "allocation": result.name,
            "new_total": result.total_leaves_allocated
        }
        
    except Exception as e:
        frappe.log_error(f"Leave adjustment API error: {str(e)}")
        frappe.throw(_("Error in leave allocation adjustment: {0}").format(str(e)))


@frappe.whitelist()
def get_employee_leave_balance(employee, leave_type=None, as_on_date=None):
    """
    API endpoint to get leave balance for an employee
    
    Args:
        employee (str): Employee ID
        leave_type (str): Leave Type (optional - if not provided, returns all leave types)
        as_on_date (str): Date to check balance (optional - defaults to today)
    """
    
    # Check permissions
    if not frappe.has_permission("Leave Allocation", "read"):
        frappe.throw(_("Not permitted to view Leave Allocations"))
    
    try:
        if not as_on_date:
            as_on_date = today()
        
        if leave_type:
            # Get balance for specific leave type
            balance = get_leave_balance_on_date(employee, leave_type, as_on_date)
            return {
                "success": True,
                "employee": employee,
                "leave_type": leave_type,
                "balance": balance,
                "as_on_date": as_on_date
            }
        else:
            # Get balance for all leave types
            leave_types = frappe.get_all("Leave Type", 
                filters={"is_active": 1}, 
                fields=["name"]
            )
            
            balances = []
            for lt in leave_types:
                balance = get_leave_balance_on_date(employee, lt.name, as_on_date)
                balances.append({
                    "leave_type": lt.name,
                    "balance": balance
                })
            
            return {
                "success": True,
                "employee": employee,
                "balances": balances,
                "as_on_date": as_on_date
            }
            
    except Exception as e:
        frappe.log_error(f"Leave balance API error: {str(e)}")
        frappe.throw(_("Error getting leave balance: {0}").format(str(e)))


@frappe.whitelist()
def get_leave_allocation_history(employee, leave_type=None, from_date=None, to_date=None):
    """
    API endpoint to get leave allocation history for an employee
    
    Args:
        employee (str): Employee ID
        leave_type (str): Leave Type (optional)
        from_date (str): Start date for history (optional)
        to_date (str): End date for history (optional)
    """
    
    # Check permissions
    if not frappe.has_permission("Leave Allocation", "read"):
        frappe.throw(_("Not permitted to view Leave Allocations"))
    
    try:
        filters = {"employee": employee, "docstatus": 1}
        
        if leave_type:
            filters["leave_type"] = leave_type
            
        if from_date:
            filters["from_date"] = [">=", from_date]
            
        if to_date:
            filters["to_date"] = ["<=", to_date]
        
        allocations = frappe.get_all("Leave Allocation",
            filters=filters,
            fields=["name", "leave_type", "from_date", "to_date", 
                   "new_leaves_allocated", "carry_forwarded_leaves", 
                   "total_leaves_allocated", "creation", "modified"],
            order_by="from_date desc"
        )
        
        return {
            "success": True,
            "employee": employee,
            "allocations": allocations
        }
        
    except Exception as e:
        frappe.log_error(f"Leave allocation history API error: {str(e)}")
        frappe.throw(_("Error getting leave allocation history: {0}").format(str(e)))


@frappe.whitelist()
def validate_leave_allocation_data(employee, leave_type, allocation_date, new_leaves_allocated):
    """
    API endpoint to validate leave allocation data before processing
    
    Args:
        employee (str): Employee ID
        leave_type (str): Leave Type
        allocation_date (str): Allocation date
        new_leaves_allocated (float): Number of leaves to allocate
    """
    
    try:
        errors = []
        warnings = []
        
        # Validate employee
        if not frappe.db.exists("Employee", employee):
            errors.append(f"Employee {employee} does not exist")
        else:
            emp_status = frappe.db.get_value("Employee", employee, "status")
            if emp_status != "Active":
                warnings.append(f"Employee {employee} is not active (Status: {emp_status})")
        
        # Validate leave type
        if not frappe.db.exists("Leave Type", leave_type):
            errors.append(f"Leave Type {leave_type} does not exist")
        else:
            lt_active = frappe.db.get_value("Leave Type", leave_type, "is_active")
            if not lt_active:
                warnings.append(f"Leave Type {leave_type} is not active")
        
        # Validate allocation amount
        if float(new_leaves_allocated) < 0:
            errors.append("Leave allocation cannot be negative")
        
        # Check for existing allocation
        allocation_date = getdate(allocation_date)
        
        existing = frappe.db.get_value("Leave Allocation", {
            "employee": employee,
            "leave_type": leave_type,
            "from_date": ["<=", allocation_date],
            "to_date": [">=", allocation_date],
            "docstatus": ["!=", 2]
        })
        
        if existing:
            warnings.append(f"An allocation already exists for this period: {existing}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
        
    except Exception as e:
        frappe.log_error(f"Leave allocation validation error: {str(e)}")
        return {
            "valid": False,
            "errors": [f"Validation error: {str(e)}"],
            "warnings": []
        }
