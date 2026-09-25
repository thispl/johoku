frappe.ui.form.on('Miss Punch Application', {
	// date:function(frm) {
	// 	if (frm.doc.__islocal){
	// 		frappe.call({
	// 			'method':'frappe.client.get_value',
	// 			'args':{
	// 				'doctype':'Attendance',
	// 				'filters':{
	// 					'employee':frm.doc.employee,
	// 					'attendance_date':frm.doc.date
	// 				},
	// 				'fieldname':['in_time','out_time','shift','name']
	// 			},
	// 			callback(r){
	// 				if(r.message){
	// 					// frm.set_value('in_time',r.message.in_time)
	// 					// frm.set_value('out_time',r.message.out_time)
	// 					frm.set_value('shift',r.message.shift)
	// 					// frm.set_value('attendance_marked',r.message.name)
	// 				}
	// 			}
	// 		})
	// 	}
	// },
	after_workflow_action: function(frm) {
        frappe.call({
            method: "johoku.johoku.doctype.miss_punch_application.miss_punch_application.update_approval_role",
            args: {
                workflow_state: frm.doc.workflow_state,
                name: frm.doc.name
            },
            callback: function(response) {
                if (response) {
                    console.log('test');
                    frm.reload_doc();
                } 
            }
        });
    },
	in_punch:function(frm) {
		if(frm.doc.in_punch){
			if (frm.doc.__islocal){
				frappe.call({
					'method':'frappe.client.get_value',
					'args':{
						'doctype':'Attendance',
						'filters':{
							'employee':frm.doc.employee,
							'attendance_date':frm.doc.date,
							'docstatus': ['!=', 2]
						},
						'fieldname':['in_time','out_time','shift','name']
					},
					callback(r) {
						if (r.message) {
							frm.set_value('out_time', r.message.out_time);
							frm.set_value('in_time', '');
							// frm.set_value('shift', r.message.shift);
							frm.set_value('attendance_marked', r.message.name);
							if (r.message.in_time) {
								console.log(r.message)
								console.log(frappe.session.user);
								if (frappe.user.has_role("Miss Punch")){
									console.log(frappe.session.user)
									frm.set_df_property('in_time', 'read_only', 0);
									frm.set_value('in_time',r.message.in_time );
								}
								else{
									frm.set_df_property('in_time', 'read_only', 1);
									frappe.throw(`In time is already there at <b>${r.message.in_time}</b>. Not applicable for Miss Punch`);
								}
							} else {
								let shift_name = r.message.shift || frm.doc.shift;								
								frappe.db.get_value('Shift Type', shift_name, 'start_time', (value) => {
									if (value && value.start_time) {
										let start_time = value.start_time;
										let date = frm.doc.date; 
										let datetime_string = date + ' ' + start_time;
										let datetime = new Date(datetime_string);
										let day = String(datetime.getDate()).padStart(2, '0'); 
										let month = String(datetime.getMonth() + 1).padStart(2, '0'); 
										let year = datetime.getFullYear();
										let hours = String(datetime.getHours()).padStart(2, '0');  
										let minutes = String(datetime.getMinutes()).padStart(2, '0');  
										let formatted_datetime = `${year}-${month}-${day} ${hours}:${minutes}`;
										// console.log(formatted_datetime); 
										// console.log(frappe.session.user);
										frm.set_value('in_time',formatted_datetime);
										if (frappe.user.has_role("Miss Punch")){
											// console.log(frappe.session.user)
											frm.set_df_property('in_time', 'read_only', 0);
										}

									} else {
										frappe.msgprint(__('Start time not found for shift: ') + shift_name);
									}
								});
							}
						}
					}
					
				})
			}
		}
		
	},
	out_punch:function(frm) {
		if(frm.doc.out_punch){
			if (frm.doc.__islocal){
				frappe.call({
					'method':'frappe.client.get_value',
					'args':{
						'doctype':'Attendance',
						'filters':{
							'employee':frm.doc.employee,
							'attendance_date':frm.doc.date,
							'docstatus': ['!=', 2]
						},
						'fieldname':['in_time','out_time','shift','name']
					},
					callback(r){
						if(r.message){
								frm.set_value('in_time',r.message.in_time)
								frm.set_value('out_time', '');
								frm.set_value('attendance_marked',r.message.name)
								if (r.message.out_time) {
									if (frappe.user.has_role("Miss Punch")){
										frm.set_value('out_time', r.message.out_time);
										frm.set_df_property('in_punch', 'read_only', 0);
									}
									else{
										frm.set_df_property('out_time', 'read_only', 1);
										frappe.throw(`Out time is already there at <b>${r.message.out_time}</b>. Not applicable for Miss Punch`);
									}
									
								}
								else{
									if (frappe.user.has_role("Miss Punch")){
										frm.set_df_property('in_punch', 'read_only', 0);
										if (r.message.in_time) {
											frm.set_value('in_time',r.message.in_time)
										}
									}
								}
							
						}
					}
				})
			}
		}
		
	}
});