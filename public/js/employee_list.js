// Add Dynamic Leave Allocation to Employee List
frappe.listview_settings['Employee'] = {
    onload: function(listview) {
        // Add custom button for dynamic leave allocation
        listview.page.add_action_item(__('Dynamic Leave Allocation'), function() {
            aspirehr.leave_allocation.show_allocation_dialog();
        });
        
        listview.page.add_action_item(__('Adjust Leave Allocation'), function() {
            aspirehr.leave_allocation.show_adjustment_dialog();
        });
        
        listview.page.add_action_item(__('Check Leave Balance'), function() {
            aspirehr.leave_allocation.show_balance_dialog();
        });
    }
};

// Add to Leave Allocation List
frappe.listview_settings['Leave Allocation'] = {
    onload: function(listview) {
        listview.page.add_action_item(__('Dynamic Allocation'), function() {
            aspirehr.leave_allocation.show_allocation_dialog();
        });
        
        listview.page.add_action_item(__('Bulk Allocation'), function() {
            aspirehr.leave_allocation.show_bulk_upload_dialog();
        });
    }
};

// Add to Leave Type List
frappe.listview_settings['Leave Type'] = {
    onload: function(listview) {
        listview.page.add_action_item(__('Allocate to All Employees'), function() {
            // Get selected leave types or show dialog to select
            let selected = listview.get_checked_items();
            if (selected.length > 0) {
                let leave_type = selected[0].name;
                
                let d = new frappe.ui.Dialog({
                    title: __('Allocate {0} to All Employees', [leave_type]),
                    fields: [
                        {
                            fieldtype: 'Date',
                            fieldname: 'allocation_date',
                            label: __('Allocation Date'),
                            default: frappe.datetime.get_today(),
                            reqd: 1
                        },
                        {
                            fieldtype: 'Float',
                            fieldname: 'leaves_to_allocate',
                            label: __('Leaves to Allocate'),
                            reqd: 1
                        },
                        {
                            fieldtype: 'Check',
                            fieldname: 'carry_forward',
                            label: __('Carry Forward Previous Leaves')
                        }
                    ],
                    primary_action_label: __('Allocate'),
                    primary_action: function() {
                        let values = d.get_values();
                        
                        frappe.call({
                            method: 'aspirehr.api.leave_allocation.allocate_employee_leaves',
                            args: {
                                leave_type: leave_type,
                                allocation_date: values.allocation_date,
                                new_leaves_allocated: values.leaves_to_allocate,
                                carry_forward: values.carry_forward
                            },
                            callback: function(r) {
                                if (r.message && r.message.success) {
                                    frappe.msgprint(__('Allocation completed successfully'));
                                    d.hide();
                                }
                            }
                        });
                    }
                });
                
                d.show();
            } else {
                frappe.msgprint(__('Please select a leave type first'));
            }
        });
    }
};
