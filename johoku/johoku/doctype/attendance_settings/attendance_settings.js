// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Settings', {
	refresh: function(frm) {
		frm.disable_save()
	},
	process_attendance(frm){
		// console.log("HI");
		if (frm.doc.date && frm.doc.to_date){
			frappe.call({
				"method": "johoku.mark_attendance.enqueue_mark_att_process",
				"args":{
					from_date  : frm.doc.date,
					to_date  : frm.doc.to_date,
				},
				freeze: true,
				freeze_message: 'Processing Attendance....',
				callback(r){
					console.log("HI");
					console.log(r.message)
					if(r.message == "ok"){
						frappe.msgprint("Attendance is Marking in the Background. Kindly check after sometime")
					}
				}
			})
		}

		if (frm.doc.date && frm.doc.to_date && frm.doc.employee){
			console.log("Check OD JMPLS209")
			frappe.call({
				"method": "johoku.mark_attendance.mark_att_with_employee",
				"args":{
					from_date  : frm.doc.date,
					to_date  : frm.doc.to_date,
					employee  : frm.doc.employee
				},
				freeze: true,
				freeze_message: 'Processing Attendance....',
				callback(r){
					console.log("HI");
					console.log(r.message)
					if(r.message == "ok"){
						frappe.msgprint("Attendance is updated Successfully . Kindly check")
					}
				}
			})
		}
	},
	process_checkin(frm){
		// console.log("HI");
		if (frm.doc.date && frm.doc.to_date){
			frappe.call({
				"method": "johoku.attendance_settings_custom.get_urc_to_ec",
				"args":{
					from_date  : frm.doc.date,
					to_date  : frm.doc.to_date,
				},
				freeze: true,
				freeze_message: 'Processing Checkin....',
				callback(r){
					console.log("HI");
					console.log(r.message)
					if(r.message == "ok"){
						frappe.msgprint("Checkin is Marking in the Background. Kindly check after sometime")
					}
				}
			})
		}
	},
	process_checkin_2(frm){
		// console.log("HI");
		if (frm.doc.date && frm.doc.to_date){
			frappe.call({
				"method": "johoku.attendance_settings_custom.push_punch",
				"args":{
					from_date  : frm.doc.date,
					to_date  : frm.doc.to_date,
				},
				freeze: true,
				freeze_message: 'Processing Checkin Easytimepro to HRPRO....',
				callback(r){
					console.log("HI");
					console.log(r.message)
					if(r.message == "ok"){
						frappe.msgprint("Checkin is Marking in the Background. Kindly check after sometime")
					}
				}
			
			})
		}
	},
	backup_datas(frm){
		if (frm.doc.date && frm.doc.to_date){
			frappe.call({
				"method": "johoku.attendance_settings_custom.download_easytimepro_excel",
				"args":{
					from_date  : frm.doc.date,
					to_date  : frm.doc.to_date,
				},
				freeze: true,
				freeze_message: 'Processing Checkin Easytimepro to HRPRO....',
				callback(r){
					
					console.log(r.message)
					if(r.message == "ok"){
						console.log("HI");
						frappe.msgprint("Backup Data is Marking in the Background. Kindly check after sometime")
					}
				}
			
			})
		}
	},
	submit_attendance(frm){
		if (frm.doc.date && frm.doc.to_date){
			frappe.call({
				"method": "johoku.mark_attendance.att_draft_to_submit_without_employee",
				"args": {
					"from_date": frm.doc.date,
					"to_date": frm.doc.to_date,
				},
				freeze: true,
				freeze_message: "Submitting...",
				callback(r){
					if(r.message == 'ok'){
						frappe.msgprint("Attendance Submitted Successfully")
					}
				}
			})
		}
	},
	submit_overtime(frm){
		if (frm.doc.date && frm.doc.to_date){
			frappe.call({
				"method": "johoku.johoku.doctype.employee_benefits_regularization.employee_benefits_regularization.create_additional_salary",
				"args": {
					"from_date": frm.doc.date,
					"to_date": frm.doc.to_date,
				},
				freeze: true,
				freeze_message: "Creating Additional Salary...",
				callback(r){
					if(r.message == 'ok'){
						frappe.msgprint("Additional Salary created Successfully")
					}
				}
			})
		}
	},
	
});
