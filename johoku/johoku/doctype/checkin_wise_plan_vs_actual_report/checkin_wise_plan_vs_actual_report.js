// Copyright (c) 2026, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Checkin Wise Plan Vs Actual Report', {
	   
    download: function(frm) {
        if (frm.doc.date) {  
            frm.trigger('get_data_system');
        }
        
    },
    view: function(frm) {
        if (frm.doc.date) {  
            var path = "johoku.johoku.doctype.checkin_wise_plan_vs_actual_report.checkin_wise_plan_vs_actual_report.download";
            var args = $.param({
                date: frm.doc.date,
                shift: frm.doc.shift,
                department: frm.doc.department
            });
        }
        if (path && args) {
            window.location.href = repl(frappe.request.url +
                '?cmd=%(cmd)s&%(args)s', {
                cmd: path,
                args: args
            });
        }
    },
    onload: function(frm) {
        frm.set_value("date", frappe.datetime.nowdate())
        const roles = frappe.user_roles;
        const has_miss_punch = roles.includes("Miss Punch");

        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Employee",
                fieldname: ["name", "department"],
                filters: { "user_id": frappe.session.user }
            },
            callback: function(r) {
                const emp = r.message;

                if(emp) {
                    if(!has_miss_punch) {
                        frm.set_value('department', emp.department);
                        frm.set_df_property('department', 'read_only', 1);
                    } else {
                        frm.set_df_property('department', 'read_only', 0);
                    }
                } else {
                    frm.set_df_property('department', 'read_only', 0);
                }
            }
        });
        frappe.call({
			method: 'johoku.johoku.doctype.live_shiftwise_dashboard.live_shiftwise_dashboard.get_shift',
			args:{
				'attendance_date':frm.doc.date
			},
			callback(r){
				if(r.message){
					console.log(r.message)
					if (r.message > "16:40"){
						frm.set_value('shift',2);
					}
					else if (r.message < "07:50" ){
						frm.set_value('shift',3);
					}
					else if (r.message > "07:50"){
						frm.set_value('shift',1);
					}
				}
			}
		});
        // if (frm.doc.date && frm.doc.shift) {  
        //     frm.trigger('get_data_system');
        // }
    },

    get_data_system: function(frm) {
        // frm.disable_save(); 
        if (frm.doc.date) {  
            frappe.call({
                freeze: true,
                freeze_message: 'Processing the data',
                method: "johoku.johoku.doctype.checkin_wise_plan_vs_actual_report.checkin_wise_plan_vs_actual_report.get_data_system",
                args: {
                    date: frm.doc.date,
                    shift: frm.doc.shift,
                    department: frm.doc.department
                },
                callback: function(r) {
                    frm.fields_dict.plan_vs_actual.$wrapper.empty().append(r.message);
                    // console.log(r.message)
                }
            });
        }
    },

});
