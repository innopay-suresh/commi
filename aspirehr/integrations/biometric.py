import frappe
from frappe.utils import now_datetime
# You might need to import specific libraries for different device types (e.g., ZKTeco)

def connect_device(ip_address, port, device_type):
    """
    Establishes a connection to the biometric device.
    This is a placeholder and needs implementation for specific device types/protocols.
    """
    try:
        # Implementation depends on device type and protocol (TCP/IP, HTTP API, etc.)
        # Example: For ZKTeco, you might use a library like pyzk or zklib
        # connection = YourDeviceLibrary.connect(ip_address, port)
        # return connection
        frappe.logger("biometric_integration").info(f"Attempting to connect to {device_type} device at {ip_address}:{port}")
        # Simulate a successful connection
        return True
    except Exception as e:
        frappe.logger("biometric_integration").error(f"Failed to connect to device at {ip_address}:{port}: {e}")
        return False

def get_logs(device):
    """
    Polls logs from the connected biometric device.
    This is a placeholder and needs implementation for specific device types/protocols.
    Should return a list of raw log data.
    """
    ip_address = device.ip_address
    port = device.port
    device_type = device.device_type

    frappe.logger("biometric_integration").info(f"Polling logs from {device_type} device at {ip_address}:{port}")
    logs = []
    try:
        # Implementation depends on device type and protocol
        # Example: Fetch logs from the device API or protocol
        # raw_logs = connection.get_attendance_logs()
        # logs = [parse_raw_log(raw) for raw in raw_logs] # You'd need a helper to parse raw data
        
        # Simulate fetching some logs
        simulated_logs = [
            {"device_employee_id": "101", "timestamp": now_datetime(), "punch_type": "0", "raw_data": "raw_log_string_1"},
            {"device_employee_id": "102", "timestamp": now_datetime(), "punch_type": "0", "raw_data": "raw_log_string_2"},
            # More simulated logs
        ]
        logs = simulated_logs

    except Exception as e:
        frappe.logger("biometric_integration").error(f"Failed to get logs from device at {ip_address}:{port}: {e}")

    return logs

def process_log(log_data, device):
    """
    Parses a single log entry and maps it to a Frappe Employee.
    Returns a dictionary with processed log data.
    """
    processed_log = {}
    try:
        device_employee_id = log_data.get("device_employee_id")
        timestamp = log_data.get("timestamp")
        punch_type_code = log_data.get("punch_type") # Assuming a code from the device

        # Map device punch type code to Frappe punch type (e.g., "0" -> "Check In")
        punch_type_mapping = {
            "0": "Check In",
            "1": "Check Out",
            # Add more mappings as needed
        }
        punch_type = punch_type_mapping.get(punch_type_code, "Unknown")

        # Find employee by biometric_id
        employee = frappe.db.get_value("Employee", {"biometric_id": device_employee_id}, ["name", "employee_name"], as_dict=True)

        if employee:
            processed_log = {
                "employee": employee.name,
                "timestamp": timestamp,
                "punch_type": punch_type,
                "device": device.name,
                "device_employee_id": device_employee_id,
                "raw_data": log_data.get("raw_data") # Store raw data if needed
            }
        else:
            frappe.logger("biometric_integration").warning(f"No employee found with biometric_id: {device_employee_id} from device {device.name}")

    except Exception as e:
        frappe.logger("biometric_integration").error(f"Failed to process log data from device {device.name}: {log_data}. Error: {e}")

    return processed_log

def create_attendance_entry(employee, timestamp, punch_type, device):
    """
    Creates or updates an Attendance DocType entry.
    Handles check-in/check-out logic based on existing entries for the day.
    """
    date = timestamp.date()

    try:
        # Check for existing attendance for the employee on the same date
        existing_attendance = frappe.db.get_value(
            "Attendance",
            {"employee": employee, "attendance_date": date, "docstatus": 0}, # Only consider Draft or Submitted attendance
            ["name", "check_in", "check_out"],
            as_dict=True
        )

        if existing_attendance:
            # Update existing attendance
            doc = frappe.get_doc("Attendance", existing_attendance.name)
            if punch_type == "Check In" and not doc.check_in:
                doc.check_in = timestamp
                doc.db_update() # Use db_update for partial update
                frappe.logger("biometric_integration").info(f"Updated Check In for Employee {employee} on {date} from device {device.name}")
            elif punch_type == "Check Out" and not doc.check_out:
                doc.check_out = timestamp
                doc.db_update() # Use db_update for partial update
                frappe.logger("biometric_integration").info(f"Updated Check Out for Employee {employee} on {date} from device {device.name}")
            else:
                 frappe.logger("biometric_integration").info(f"Skipping duplicate punch type ({punch_type}) for Employee {employee} on {date} from device {device.name}")

        else:
            # Create new attendance entry
            doc = frappe.new_doc("Attendance")
            doc.employee = employee
            doc.attendance_date = date
            if punch_type == "Check In":
                doc.check_in = timestamp
            elif punch_type == "Check Out":
                doc.check_out = timestamp
            doc.attendance_from = "Biometric" # Custom field to indicate source
            doc.insert(ignore_permissions=True) # Insert ignoring permissions for background job
            frappe.logger("biometric_integration").info(f"Created new Attendance entry for Employee {employee} on {date} with {punch_type} from device {device.name}")

        # Log the allocation in Biometric Log (if implemented)
        if frappe.db.exists("DocType", "Biometric Log"):
             log_doc = frappe.new_doc("Biometric Log")
             log_doc.device = device.name
             log_doc.device_employee_id = frappe.db.get_value("Employee", employee, "biometric_id") # Get biometric_id from Employee
             log_doc.timestamp = timestamp
             log_doc.punch_type = punch_type
             # log_doc.raw_data = raw_log_data # If you stored raw data in process_log
             log_doc.insert(ignore_permissions=True)

    except Exception as e:
        frappe.logger("biometric_integration").error(f"Failed to create/update Attendance for Employee {employee} on {date} from device {device.name}. Error: {e}")


def sync_device(device_name):
    """
    Main function to orchestrate the sync process for a single device.
    """
    device = frappe.get_doc("Biometric Device", device_name)
    ip_address = device.ip_address
    port = device.port
    device_type = device.device_type

    if not device.enabled:
        frappe.logger("biometric_integration").info(f"Device {device_name} is disabled. Skipping sync.")
        return

    frappe.logger("biometric_integration").info(f"Starting sync for device {device_name} ({device_type} at {ip_address}:{port})")

    connection = None
    try:
        # Step 1: Connect to the device
        connection = connect_device(ip_address, port, device_type)
        if not connection:
            frappe.throw(f"Failed to connect to device {device_name}")

        # Step 2: Get logs from the device
        raw_logs = get_logs(device)

        # Step 3: Process logs and create/update attendance
        for log_data in raw_logs:
            processed_log = process_log(log_data, device)
            if processed_log:
                create_attendance_entry(
                    processed_log["employee"],
                    processed_log["timestamp"],
                    processed_log["punch_type"],
                    device
                )

        # Update last sync timestamp
        device.last_sync_timestamp = now_datetime()
        device.save(ignore_permissions=True)

        frappe.logger("biometric_integration").info(f"Sync completed successfully for device {device_name}")

    except Exception as e:
        frappe.logger("biometric_integration").error(f"Sync failed for device {device_name}. Error: {e}")
        # Implement email alert for device offline status if needed
        # frappe.sendmail(recipients="admin@example.com", subject=f"Biometric Device Offline: {device_name}", message=f"Failed to sync with biometric device {device_name} at {ip_address}:{port}. Error: {e}")

    finally:
        # Step 4: Disconnect from the device (if applicable)
        if connection:
            try:
                # connection.disconnect()
                frappe.logger("biometric_integration").info(f"Disconnected from device {device_name}")
            except Exception as e:
                frappe.logger("biometric_integration").error(f"Failed to disconnect from device {device_name}: {e}")

@frappe.background_task
def sync_all_devices():
    """
    Background task to sync all enabled biometric devices.
    """
    frappe.logger("biometric_integration").info("Starting scheduled sync for all enabled devices")
    devices = frappe.get_all("Biometric Device", filters={"enabled": 1}, pluck="name")
    for device_name in devices:
        sync_device(device_name)
    frappe.logger("biometric_integration").info("Scheduled sync completed for all enabled devices")