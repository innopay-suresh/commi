// AspireHR Common JavaScript Functions

frappe.provide('aspirehr');

aspirehr.utils = {
    // Format employee name with ID
    format_employee_name: function(employee, employee_name) {
        if (employee && employee_name) {
            return `${employee_name} (${employee})`;
        }
        return employee_name || employee || '';
    },

    // Get employee details
    get_employee_details: function(employee, callback) {
        if (!employee) {
            callback({});
            return;
        }

        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Employee',
                name: employee
            },
            callback: function(r) {
                callback(r.message || {});
            }
        });
    },

    // Validate date range
    validate_date_range: function(from_date, to_date) {
        if (!from_date || !to_date) {
            frappe.msgprint(__('Please select both From Date and To Date'));
            return false;
        }

        if (frappe.datetime.get_diff(to_date, from_date) < 0) {
            frappe.msgprint(__('To Date cannot be before From Date'));
            return false;
        }

        return true;
    },

    // Calculate working days
    calculate_working_days: function(from_date, to_date, holiday_list, callback) {
        frappe.call({
            method: 'erpnext.setup.utils.get_exchange_rate',
            args: {
                from_date: from_date,
                to_date: to_date,
                holiday_list: holiday_list
            },
            callback: function(r) {
                callback(r.message || 0);
            }
        });
    },

    // Show employee quick info
    show_employee_info: function(employee) {
        frappe.call({
            method: 'aspirehr.human_resources.utils.get_employee_info',
            args: {
                employee: employee
            },
            callback: function(r) {
                if (r.message) {
                    let info = r.message;
                    let html = `
                        <div class="aspirehr-employee-info">
                            <h4>${info.employee_name}</h4>
                            <p><strong>Employee ID:</strong> ${info.name}</p>
                            <p><strong>Department:</strong> ${info.department || ''}</p>
                            <p><strong>Designation:</strong> ${info.designation || ''}</p>
                            <p><strong>Company:</strong> ${info.company || ''}</p>
                            <p><strong>Date of Joining:</strong> ${frappe.datetime.str_to_user(info.date_of_joining) || ''}</p>
                        </div>
                    `;
                    
                    frappe.msgprint({
                        title: __('Employee Information'),
                        message: html,
                        wide: true
                    });
                }
            }
        });
    },

    // Format currency for payroll
    format_payroll_currency: function(amount, currency) {
        return format_currency(amount, currency || frappe.defaults.get_default('currency'));
    },

    // Get attendance status color
    get_attendance_status_color: function(status) {
        const color_map = {
            'Present': 'green',
            'Absent': 'red',
            'Half Day': 'orange',
            'Work From Home': 'blue',
            'On Leave': 'purple'
        };
        return color_map[status] || 'gray';
    },

    // Show attendance summary
    show_attendance_summary: function(employee, from_date, to_date) {
        frappe.call({
            method: 'aspirehr.human_resources.utils.get_attendance_summary',
            args: {
                employee: employee,
                from_date: from_date,
                to_date: to_date
            },
            callback: function(r) {
                if (r.message) {
                    let data = r.message;
                    let html = `
                        <div class="aspirehr-attendance-summary">
                            <div class="row">
                                <div class="col-sm-3 text-center">
                                    <div class="aspirehr-stat-card">
                                        <span class="aspirehr-stat-number text-success">${data.present}</span>
                                        <span class="aspirehr-stat-label">Present</span>
                                    </div>
                                </div>
                                <div class="col-sm-3 text-center">
                                    <div class="aspirehr-stat-card">
                                        <span class="aspirehr-stat-number text-danger">${data.absent}</span>
                                        <span class="aspirehr-stat-label">Absent</span>
                                    </div>
                                </div>
                                <div class="col-sm-3 text-center">
                                    <div class="aspirehr-stat-card">
                                        <span class="aspirehr-stat-number text-warning">${data.half_day}</span>
                                        <span class="aspirehr-stat-label">Half Day</span>
                                    </div>
                                </div>
                                <div class="col-sm-3 text-center">
                                    <div class="aspirehr-stat-card">
                                        <span class="aspirehr-stat-number text-info">${data.on_leave}</span>
                                        <span class="aspirehr-stat-label">On Leave</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    frappe.msgprint({
                        title: __('Attendance Summary'),
                        message: html,
                        wide: true
                    });
                }
            }
        });
    }
};

// AspireHR Dashboard Functions
aspirehr.dashboard = {
    // Show HR Dashboard
    show_hr_dashboard: function() {
        frappe.set_route('query-report', 'AspireHR Dashboard');
    },

    // Quick actions for HR
    add_quick_actions: function(page) {
        page.add_action_icon('fa fa-plus', function() {
            let actions = [
                {
                    label: __('New Employee'),
                    action: () => frappe.new_doc('Employee')
                },
                {
                    label: __('New Leave Application'),
                    action: () => frappe.new_doc('Leave Application')
                },
                {
                    label: __('New Expense Claim'),
                    action: () => frappe.new_doc('Expense Claim')
                },
                {
                    label: __('Mark Attendance'),
                    action: () => frappe.set_route('Form', 'Employee Attendance Tool')
                }
            ];

            let d = new frappe.ui.Dialog({
                title: __('Quick Actions'),
                fields: [
                    {
                        fieldtype: 'HTML',
                        options: aspirehr.dashboard.get_quick_actions_html(actions)
                    }
                ]
            });

            d.show();
        });
    },

    get_quick_actions_html: function(actions) {
        let html = '<div class="aspirehr-quick-actions">';
        actions.forEach(action => {
            html += `<button class="aspirehr-quick-action-btn" onclick="${action.action}">${action.label}</button>`;
        });
        html += '</div>';
        return html;
    }
};

// Initialize AspireHR on page load
$(document).ready(function() {
    // Add AspireHR specific styles
    if (!$('link[href*="aspirehr.css"]').length) {
        $('<link>')
            .appendTo('head')
            .attr({
                type: 'text/css',
                rel: 'stylesheet',
                href: '/assets/aspirehr/css/aspirehr.css'
            });
    }
});
