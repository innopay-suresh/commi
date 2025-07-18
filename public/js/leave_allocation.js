// Dynamic Leave Allocation JavaScript Functions

frappe.provide('aspirehr.leave_allocation');

aspirehr.leave_allocation = {
    
    // Show dynamic leave allocation dialog
    show_allocation_dialog: function() {
        let d = new frappe.ui.Dialog({
            title: __('Dynamic Leave Allocation'),
            fields: [
                {
                    fieldtype: 'Section Break',
                    label: __('Allocation Details')
                },
                {
                    fieldtype: 'Link',
                    fieldname: 'employee',
                    label: __('Employee'),
                    options: 'Employee',
                    description: __('Leave empty to allocate for all active employees')
                },
                {
                    fieldtype: 'Link',
                    fieldname: 'leave_type',
                    label: __('Leave Type'),
                    options: 'Leave Type',
                    description: __('Leave empty to allocate for all active leave types')
                },
                {
                    fieldtype: 'Date',
                    fieldname: 'allocation_date',
                    label: __('Allocation Date'),
                    default: frappe.datetime.get_today(),
                    reqd: 1
                },
                {
                    fieldtype: 'Float',
                    fieldname: 'new_leaves_allocated',
                    label: __('Leaves to Allocate'),
                    reqd: 1,
                    description: __('Number of leaves to allocate')
                },
                {
                    fieldtype: 'Column Break'
                },
                {
                    fieldtype: 'Check',
                    fieldname: 'carry_forward',
                    label: __('Carry Forward Previous Leaves'),
                    description: __('Include unused leaves from previous allocation period')
                },
                {
                    fieldtype: 'Section Break',
                    label: __('Preview & Validation')
                },
                {
                    fieldtype: 'Button',
                    fieldname: 'validate_data',
                    label: __('Validate Allocation Data'),
                    click: function() {
                        aspirehr.leave_allocation.validate_allocation_data(d);
                    }
                },
                {
                    fieldtype: 'HTML',
                    fieldname: 'validation_result',
                    label: __('Validation Result')
                }
            ],
            primary_action_label: __('Allocate Leaves'),
            primary_action: function() {
                aspirehr.leave_allocation.process_allocation(d);
            },
            secondary_action_label: __('Bulk Upload'),
            secondary_action: function() {
                aspirehr.leave_allocation.show_bulk_upload_dialog();
            }
        });
        
        d.show();
    },
    
    // Validate allocation data
    validate_allocation_data: function(dialog) {
        let values = dialog.get_values();
        
        if (!values.allocation_date || !values.new_leaves_allocated) {
            frappe.msgprint(__('Please fill Allocation Date and Leaves to Allocate'));
            return;
        }
        
        frappe.call({
            method: 'aspirehr.api.leave_allocation.validate_leave_allocation_data',
            args: {
                employee: values.employee,
                leave_type: values.leave_type,
                allocation_date: values.allocation_date,
                new_leaves_allocated: values.new_leaves_allocated
            },
            callback: function(r) {
                if (r.message) {
                    let result = r.message;
                    let html = '<div class="validation-result">';
                    
                    if (result.valid) {
                        html += '<div class="alert alert-success"><i class="fa fa-check"></i> Validation Passed</div>';
                    } else {
                        html += '<div class="alert alert-danger"><i class="fa fa-times"></i> Validation Failed</div>';
                    }
                    
                    if (result.errors && result.errors.length > 0) {
                        html += '<div class="alert alert-danger"><strong>Errors:</strong><ul>';
                        result.errors.forEach(error => {
                            html += `<li>${error}</li>`;
                        });
                        html += '</ul></div>';
                    }
                    
                    if (result.warnings && result.warnings.length > 0) {
                        html += '<div class="alert alert-warning"><strong>Warnings:</strong><ul>';
                        result.warnings.forEach(warning => {
                            html += `<li>${warning}</li>`;
                        });
                        html += '</ul></div>';
                    }
                    
                    html += '</div>';
                    
                    dialog.fields_dict.validation_result.$wrapper.html(html);
                }
            }
        });
    },
    
    // Process leave allocation
    process_allocation: function(dialog) {
        let values = dialog.get_values();
        
        if (!values.allocation_date || !values.new_leaves_allocated) {
            frappe.msgprint(__('Please fill all required fields'));
            return;
        }
        
        frappe.confirm(
            __('Are you sure you want to proceed with the leave allocation?'),
            function() {
                frappe.call({
                    method: 'aspirehr.api.leave_allocation.allocate_employee_leaves',
                    args: values,
                    freeze: true,
                    freeze_message: __('Processing leave allocation...'),
                    callback: function(r) {
                        if (r.message && r.message.success) {
                            frappe.msgprint({
                                title: __('Success'),
                                message: r.message.message,
                                indicator: 'green'
                            });
                            
                            dialog.hide();
                            
                            // Show result summary
                            aspirehr.leave_allocation.show_allocation_summary(r.message.data);
                        }
                    }
                });
            }
        );
    },
    
    // Show allocation summary
    show_allocation_summary: function(data) {
        if (!data || data.length === 0) {
            return;
        }
        
        let html = '<div class="allocation-summary">';
        html += `<p><strong>Total Allocations Processed:</strong> ${data.length}</p>`;
        html += '<table class="table table-striped">';
        html += '<thead><tr><th>Employee</th><th>Leave Type</th><th>Leaves Allocated</th><th>Allocation ID</th></tr></thead>';
        html += '<tbody>';
        
        data.forEach(allocation => {
            html += `<tr>
                <td>${allocation.employee}</td>
                <td>${allocation.leave_type}</td>
                <td>${allocation.leaves_allocated}</td>
                <td><a href="/app/leave-allocation/${allocation.allocation}" target="_blank">${allocation.allocation}</a></td>
            </tr>`;
        });
        
        html += '</tbody></table></div>';
        
        frappe.msgprint({
            title: __('Allocation Summary'),
            message: html,
            wide: true
        });
    },
    
    // Show bulk upload dialog
    show_bulk_upload_dialog: function() {
        let d = new frappe.ui.Dialog({
            title: __('Bulk Leave Allocation'),
            fields: [
                {
                    fieldtype: 'Section Break',
                    label: __('Upload CSV File')
                },
                {
                    fieldtype: 'HTML',
                    fieldname: 'upload_help',
                    options: `
                        <div class="alert alert-info">
                            <strong>CSV Format:</strong> employee,leave_type,allocation_date,new_leaves_allocated,carry_forward<br>
                            <strong>Example:</strong><br>
                            EMP-001,Annual Leave,2024-01-01,21,1<br>
                            EMP-002,Sick Leave,2024-01-01,12,0
                        </div>
                    `
                },
                {
                    fieldtype: 'Attach',
                    fieldname: 'csv_file',
                    label: __('CSV File'),
                    reqd: 1
                },
                {
                    fieldtype: 'Section Break',
                    label: __('Or Enter Data Manually')
                },
                {
                    fieldtype: 'Table',
                    fieldname: 'allocation_data',
                    label: __('Allocation Data'),
                    fields: [
                        {
                            fieldtype: 'Link',
                            fieldname: 'employee',
                            label: __('Employee'),
                            options: 'Employee',
                            in_list_view: 1,
                            reqd: 1
                        },
                        {
                            fieldtype: 'Link',
                            fieldname: 'leave_type',
                            label: __('Leave Type'),
                            options: 'Leave Type',
                            in_list_view: 1,
                            reqd: 1
                        },
                        {
                            fieldtype: 'Date',
                            fieldname: 'allocation_date',
                            label: __('Allocation Date'),
                            in_list_view: 1,
                            reqd: 1
                        },
                        {
                            fieldtype: 'Float',
                            fieldname: 'new_leaves_allocated',
                            label: __('Leaves'),
                            in_list_view: 1,
                            reqd: 1
                        },
                        {
                            fieldtype: 'Check',
                            fieldname: 'carry_forward',
                            label: __('Carry Forward'),
                            in_list_view: 1
                        }
                    ]
                }
            ],
            primary_action_label: __('Process Bulk Allocation'),
            primary_action: function() {
                aspirehr.leave_allocation.process_bulk_allocation(d);
            }
        });
        
        d.show();
    },
    
    // Process bulk allocation
    process_bulk_allocation: function(dialog) {
        let values = dialog.get_values();
        let allocation_data = values.allocation_data;
        
        if (!allocation_data || allocation_data.length === 0) {
            frappe.msgprint(__('Please add allocation data'));
            return;
        }
        
        frappe.call({
            method: 'aspirehr.api.leave_allocation.bulk_allocate_leaves',
            args: {
                allocation_data: JSON.stringify(allocation_data)
            },
            freeze: true,
            freeze_message: __('Processing bulk allocation...'),
            callback: function(r) {
                if (r.message && r.message.success) {
                    dialog.hide();
                    
                    let result = r.message;
                    let html = `
                        <div class="bulk-allocation-result">
                            <div class="row">
                                <div class="col-sm-4 text-center">
                                    <div class="alert alert-info">
                                        <h4>${result.summary.total_records}</h4>
                                        <p>Total Records</p>
                                    </div>
                                </div>
                                <div class="col-sm-4 text-center">
                                    <div class="alert alert-success">
                                        <h4>${result.summary.successful}</h4>
                                        <p>Successful</p>
                                    </div>
                                </div>
                                <div class="col-sm-4 text-center">
                                    <div class="alert alert-danger">
                                        <h4>${result.summary.failed}</h4>
                                        <p>Failed</p>
                                    </div>
                                </div>
                            </div>
                    `;
                    
                    if (result.failed && result.failed.length > 0) {
                        html += '<div class="alert alert-warning"><strong>Failed Records:</strong><ul>';
                        result.failed.forEach(failed => {
                            html += `<li>Employee: ${failed.data.employee}, Error: ${failed.error}</li>`;
                        });
                        html += '</ul></div>';
                    }
                    
                    html += '</div>';
                    
                    frappe.msgprint({
                        title: __('Bulk Allocation Result'),
                        message: html,
                        wide: true
                    });
                }
            }
        });
    },
    
    // Show leave adjustment dialog
    show_adjustment_dialog: function() {
        let d = new frappe.ui.Dialog({
            title: __('Adjust Leave Allocation'),
            fields: [
                {
                    fieldtype: 'Link',
                    fieldname: 'employee',
                    label: __('Employee'),
                    options: 'Employee',
                    reqd: 1
                },
                {
                    fieldtype: 'Link',
                    fieldname: 'leave_type',
                    label: __('Leave Type'),
                    options: 'Leave Type',
                    reqd: 1
                },
                {
                    fieldtype: 'Date',
                    fieldname: 'adjustment_date',
                    label: __('Adjustment Date'),
                    default: frappe.datetime.get_today(),
                    reqd: 1
                },
                {
                    fieldtype: 'Float',
                    fieldname: 'adjustment_amount',
                    label: __('Adjustment Amount'),
                    description: __('Positive for addition, negative for deduction'),
                    reqd: 1
                },
                {
                    fieldtype: 'Small Text',
                    fieldname: 'reason',
                    label: __('Reason for Adjustment'),
                    reqd: 1
                }
            ],
            primary_action_label: __('Adjust Allocation'),
            primary_action: function() {
                let values = d.get_values();
                
                frappe.call({
                    method: 'aspirehr.api.leave_allocation.adjust_employee_leave_allocation',
                    args: values,
                    callback: function(r) {
                        if (r.message && r.message.success) {
                            frappe.msgprint({
                                title: __('Success'),
                                message: r.message.message,
                                indicator: 'green'
                            });
                            d.hide();
                        }
                    }
                });
            }
        });
        
        d.show();
    },
    
    // Show leave balance dialog
    show_balance_dialog: function() {
        let d = new frappe.ui.Dialog({
            title: __('Check Leave Balance'),
            fields: [
                {
                    fieldtype: 'Link',
                    fieldname: 'employee',
                    label: __('Employee'),
                    options: 'Employee',
                    reqd: 1
                },
                {
                    fieldtype: 'Link',
                    fieldname: 'leave_type',
                    label: __('Leave Type'),
                    options: 'Leave Type',
                    description: __('Leave empty to show all leave types')
                },
                {
                    fieldtype: 'Date',
                    fieldname: 'as_on_date',
                    label: __('As On Date'),
                    default: frappe.datetime.get_today(),
                    reqd: 1
                },
                {
                    fieldtype: 'Section Break'
                },
                {
                    fieldtype: 'HTML',
                    fieldname: 'balance_result',
                    label: __('Leave Balance')
                }
            ],
            primary_action_label: __('Check Balance'),
            primary_action: function() {
                let values = d.get_values();
                
                frappe.call({
                    method: 'aspirehr.api.leave_allocation.get_employee_leave_balance',
                    args: values,
                    callback: function(r) {
                        if (r.message && r.message.success) {
                            let html = '<div class="leave-balance-result">';
                            
                            if (r.message.balances) {
                                // Multiple leave types
                                html += '<table class="table table-striped">';
                                html += '<thead><tr><th>Leave Type</th><th>Balance</th></tr></thead>';
                                html += '<tbody>';
                                
                                r.message.balances.forEach(balance => {
                                    html += `<tr><td>${balance.leave_type}</td><td>${balance.balance}</td></tr>`;
                                });
                                
                                html += '</tbody></table>';
                            } else {
                                // Single leave type
                                html += `<div class="alert alert-info">
                                    <h4>${r.message.leave_type}: ${r.message.balance} days</h4>
                                    <p>As on ${r.message.as_on_date}</p>
                                </div>`;
                            }
                            
                            html += '</div>';
                            
                            d.fields_dict.balance_result.$wrapper.html(html);
                        }
                    }
                });
            }
        });
        
        d.show();
    }
};

// Add to global namespace for easy access
window.aspirehr_leave_allocation = aspirehr.leave_allocation;
