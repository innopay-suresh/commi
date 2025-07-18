# Dynamic Leave Allocation - AspireHR

## Overview
The Dynamic Leave Allocation feature in AspireHR allows HR administrators to allocate leaves to employees on customized dates with flexible options and automation.

## Features

### 1. Dynamic Leave Allocation
- Allocate leaves to individual employees or all employees at once
- Specify custom allocation dates
- Support for carry forward from previous periods
- Bulk allocation from CSV files or manual entry

### 2. Leave Allocation Adjustment
- Adjust existing allocations by adding or subtracting leaves
- Maintain audit trail with reasons for adjustments
- Automatic calculation of new totals

### 3. Leave Balance Inquiry
- Check leave balances for any employee on any date
- View balances for specific leave types or all types
- Historical balance tracking

### 4. Automated Allocation
- Annual allocation on January 1st for all leave types
- Monthly earned leave allocation for qualifying employees
- Scheduled allocations based on custom dates

## API Endpoints

### Allocate Employee Leaves
```
POST /api/method/aspirehr.api.leave_allocation.allocate_employee_leaves

Parameters:
- employee (optional): Employee ID
- leave_type (optional): Leave Type
- allocation_date (optional): Allocation date (defaults to today)
- new_leaves_allocated: Number of leaves to allocate
- carry_forward: Boolean for carry forward option
```

### Bulk Leave Allocation
```
POST /api/method/aspirehr.api.leave_allocation.bulk_allocate_leaves

Parameters:
- allocation_data: JSON array of allocation records
```

### Adjust Leave Allocation
```
POST /api/method/aspirehr.api.leave_allocation.adjust_employee_leave_allocation

Parameters:
- employee: Employee ID
- leave_type: Leave Type
- adjustment_date: Date of adjustment
- adjustment_amount: Amount to adjust (positive/negative)
- reason: Reason for adjustment
```

### Get Leave Balance
```
GET /api/method/aspirehr.api.leave_allocation.get_employee_leave_balance

Parameters:
- employee: Employee ID
- leave_type (optional): Leave Type
- as_on_date (optional): Date to check balance
```

## Usage Instructions

### From Employee List
1. Go to Employee List
2. Click "Dynamic Leave Allocation" button
3. Fill in allocation details
4. Click "Allocate Leaves"

### From Leave Allocation List
1. Go to Leave Allocation List
2. Click "Dynamic Allocation" for single allocation
3. Click "Bulk Allocation" for multiple allocations

### From Leave Type List
1. Go to Leave Type List
2. Select a leave type
3. Click "Allocate to All Employees"
4. Specify allocation details

### Bulk Upload Format
CSV format for bulk allocation:
```
employee,leave_type,allocation_date,new_leaves_allocated,carry_forward
EMP-001,Annual Leave,2024-01-01,21,1
EMP-002,Sick Leave,2024-01-01,12,0
```

## Scheduled Tasks

### Annual Allocation (January 1st, 2:00 AM)
- Automatically allocates leaves for all non-earned leave types
- Includes carry forward from previous year
- Processes all active employees

### Monthly Allocation (1st of every month, 2:00 AM)
- Allocates earned leaves for qualifying employees
- Only for employees with 6+ months of service
- Calculates monthly accrual based on annual entitlement

## Configuration

### Leave Type Setup
- Mark leave types as "Earned Leave" for monthly accrual
- Set "Earned Leave Frequency" to "Monthly"
- Configure "Max Carry Forwarded Leaves" for limits

### Employee Setup
- Ensure proper "Date of Joining" for eligibility calculations
- Set employee status to "Active" for inclusion in automatic allocations

### HR Settings
- Configure leave policies and approval workflows
- Set up email templates for notifications
- Define company-specific leave rules

## Validation Rules

### Employee Validation
- Employee must exist and be active
- Employee must have proper joining date for earned leaves

### Leave Type Validation
- Leave type must exist and be active
- Earned leave frequency must be properly configured

### Date Validation
- Allocation date cannot be in the future for certain operations
- Date ranges must be logical (from_date <= to_date)

### Amount Validation
- Leave allocation cannot be negative
- Adjustments cannot result in negative totals

## Error Handling

### API Errors
- Proper error messages with specific failure reasons
- Logging of all errors for debugging
- Rollback on partial failures in bulk operations

### Validation Errors
- Pre-validation before processing
- Warning messages for potential issues
- Confirmation dialogs for critical operations

## Security

### Permissions
- Create permission required for new allocations
- Write permission required for adjustments
- Read permission required for balance inquiries

### Audit Trail
- All allocations are logged with timestamps
- Adjustments include reasons and user information
- Full history tracking for compliance

## Performance Considerations

### Bulk Operations
- Batch processing for large datasets
- Progress indicators for long-running operations
- Error reporting without stopping entire process

### Scheduled Tasks
- Off-peak timing for automatic allocations
- Efficient queries to minimize database load
- Proper indexing on date and employee fields

## Troubleshooting

### Common Issues
1. **Allocation fails for some employees**: Check employee status and leave type configuration
2. **Carry forward not working**: Verify previous allocation exists and dates are correct
3. **Scheduled allocation not running**: Check cron job configuration and server time

### Debugging
- Check error logs in Frappe for detailed error messages
- Use validation endpoint to pre-check data before processing
- Verify permissions for the user performing operations

## Future Enhancements

### Planned Features
- Custom allocation rules based on department/designation
- Integration with attendance for automatic accrual
- Advanced reporting and analytics
- Mobile app support for leave allocation

### Customization Options
- Custom fields for allocation tracking
- Workflow customization for approval processes
- Integration with third-party HRIS systems
- Multi-company support with separate policies
