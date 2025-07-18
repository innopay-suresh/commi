import unittest
import frappe
from frappe.tests.utils import FrappeTestCase
from datetime import date, timedelta

from human_resources.utils import allocate_leaves_on_onboarding, allocate_scheduled_leaves

class TestLeaveAllocation(FrappeTestCase):
    def setUp(self):
        # Create necessary Leave Types with auto-allocation enabled
        self.casual_leave_type = frappe.get_doc({
            "doctype": "Leave Type",
            "leave_type_name": "Casual Leave (Auto)",
            "auto_allocate": 1,
            "allocation_frequency": "Yearly",
            "allocation_amount": 12,
            "is_earned_leave": 0,
        }).insert(ignore_permissions=True)

        self.sick_leave_type = frappe.get_doc({
            "doctype": "Leave Type",
            "leave_type_name": "Sick Leave (Auto Monthly)",
            "auto_allocate": 1,
            "allocation_frequency": "Monthly",
            "allocation_amount": 1,
            "is_earned_leave": 0,
        }).insert(ignore_permissions=True)

    def tearDown(self):
        # Clean up created documents
        frappe.delete_doc("Leave Type", self.casual_leave_type.name)
        frappe.delete_doc("Leave Type", self.sick_leave_type.name)
        frappe.db.sql("delete from `tabEmployee` where employee_name like 'Test Employee%'")
        frappe.db.sql("delete from `tabLeave Allocation` where leave_type like '%(Auto)%' or leave_type like '%(Auto Monthly)%'")
        frappe.db.sql("delete from `tabLeave Allocation Log` where employee like 'Test Employee%'")
        frappe.db.commit()

    def create_employee(self, employee_name, status="Active", date_of_joining=None, relieving_date=None):
        if date_of_joining is None:
            date_of_joining = date.today()
        employee = frappe.get_doc({
            "doctype": "Employee",
            "employee_name": employee_name,
            "gender": "Male",
            "date_of_joining": date_of_joining,
            "status": status,
            "relieving_date": relieving_date
        })
        employee.insert(ignore_permissions=True)
        employee.submit()
        return employee

    def test_auto_allocation_on_onboarding(self):
        employee_name = "Test Employee Onboarding"
        employee = self.create_employee(employee_name)

        allocate_leaves_on_onboarding(employee)

        # Check for yearly allocation
        casual_allocation = frappe.db.exists(
            "Leave Allocation", {
                "employee": employee.name,
                "leave_type": self.casual_leave_type.name,
                "from_date": date(date.today().year, 1, 1),
                "to_date": date(date.today().year, 12, 31),
                "allocated_leaves": 12
            }
        )
        self.assertTrue(casual_allocation)

        # Check for monthly allocation
        sick_allocation = frappe.db.exists(
            "Leave Allocation", {
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
                "from_date": date(date.today().year, date.today().month, 1),
                "to_date": date(date.today().year, date.today().month, frappe.utils.get_last_day(date.today())),
                "allocated_leaves": 1
            }
        )
        self.assertTrue(sick_allocation)

        # Check for log entries
        casual_log = frappe.db.exists(
            "Leave Allocation Log", {
                "employee": employee.name,
                "leave_type": self.casual_leave_type.name,
                "allocated_amount": 12
            }
        )
        self.assertTrue(casual_log)
        sick_log = frappe.db.exists(
            "Leave Allocation Log", {
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
                "allocated_amount": 1
            }
        )
        self.assertTrue(sick_log)

    def test_scheduled_allocation_active_employee(self):
        employee_name = "Test Employee Scheduled Active"
        employee = self.create_employee(employee_name)

        # Run scheduled allocation
        allocate_scheduled_leaves()

        # Check for monthly allocation (yearly might have already been done on onboarding)
        sick_allocation = frappe.db.exists(
            "Leave Allocation", {
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
                "from_date": date(date.today().year, date.today().month, 1),
                "to_date": date(date.today().year, date.today().month, frappe.utils.get_last_day(date.today())),
                "allocated_leaves": 1
            }
        )
        self.assertTrue(sick_allocation)

        # Check for log entry
        sick_log = frappe.db.exists(
            "Leave Allocation Log", {
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
                "allocated_amount": 1
            }
        )
        self.assertTrue(sick_log)


    def test_scheduled_allocation_skip_inactive(self):
        employee_name = "Test Employee Scheduled Inactive"
        employee = self.create_employee(employee_name, status="Inactive")

        # Run scheduled allocation
        allocate_scheduled_leaves()

        # Check that no allocation was created
        allocation = frappe.db.exists(
            "Leave Allocation", {
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
            }
        )
        self.assertFalse(allocation)

        # Check that no log entry was created
        log = frappe.db.exists(
            "Leave Allocation Log", {
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
            }
        )
        self.assertFalse(log)

    def test_scheduled_allocation_skip_on_notice(self):
        employee_name = "Test Employee Scheduled Notice"
        # Set a relieving date in the future
        relieving_date = date.today() + timedelta(days=30)
        employee = self.create_employee(employee_name, status="Active", relieving_date=relieving_date)

        # Run scheduled allocation
        allocate_scheduled_leaves()

        # Check that no allocation was created
        allocation = frappe.db.exists(
            "Leave Allocation", {
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
            }
        )
        self.assertFalse(allocation)

        # Check that no log entry was created
        log = frappe.db.exists(
            "Leave Allocation Log", {
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
            }
        )
        self.assertFalse(log)

    def test_scheduled_allocation_skip_existing(self):
        employee_name = "Test Employee Scheduled Existing"
        employee = self.create_employee(employee_name)

        # Manually create an allocation for the current period
        frappe.get_doc({
            "doctype": "Leave Allocation",
            "employee": employee.name,
            "leave_type": self.sick_leave_type.name,
            "from_date": date(date.today().year, date.today().month, 1),
            "to_date": date(date.today().year, date.today().month, frappe.utils.get_last_day(date.today())),
            "allocated_leaves": 1,
            "new_leaves_allocated": 1,
        }).insert(ignore_permissions=True)

        # Run scheduled allocation
        allocate_scheduled_leaves()

        # Check that only one allocation exists for the period
        allocations = frappe.get_list(
            "Leave Allocation",
            filters={
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
                "from_date": date(date.today().year, date.today().month, 1),
                "to_date": date(date.today().year, date.today().month, frappe.utils.get_last_day(date.today())),
            }
        )
        self.assertEqual(len(allocations), 1)

        # Check that only one log entry exists for the period (manual allocation wouldn't create a log in this system)
        logs = frappe.get_list(
            "Leave Allocation Log",
            filters={
                "employee": employee.name,
                "leave_type": self.sick_leave_type.name,
            }
        )
        self.assertEqual(len(logs), 0) # Assuming manual allocation doesn't create a log entry based on the requirements
