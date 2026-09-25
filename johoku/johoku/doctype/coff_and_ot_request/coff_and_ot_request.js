// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('COFF and OT Request', {
	// request_type: function(frm) {
	// 	frm.trigger('calculate_working_hours');
	// },
	// employee: function(frm) {
	// 	frm.trigger('calculate_working_hours');
	// },
	// ot_date: function(frm) {
	// 	frm.trigger('calculate_working_hours');
	// },
	// calculate_working_hours: function(frm){
	// 	if (frm.doc.request_type == 'OT' && frm.doc.employee && frm.doc.ot_date) {
	// 		frappe.call({
	// 			method: 'johoku.johoku.doctype.coff_and_ot_request.coff_and_ot_request.calculate_ot_hours', // Corrected 'methood' to 'method'
	// 			args: {
	// 				employee: frm.doc.employee,
	// 				ot_date: frm.doc.ot_date
	// 			},
	// 			callback: function(r) {
	// 				console.log(r.message);
	// 				if (r.message) {
	// 					console.log(r.message);
	// 					frm.set_value('working_hours', r.message);
	// 				}
	// 			}
	// 		});
	// 	}
	// }
});
