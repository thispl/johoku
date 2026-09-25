// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Man Power Category  Wise  Plan Vs Actual Summary', {
	// refresh: function(frm) {

	// }
	download(frm) {
		if (frm.doc.report === 'Man Power Category  Wise  Plan Vs Actual Summary') {
			if (frm.doc.date) {  // Ensure both date and shift are present
				var path = 'johoku.johoku.doctype.man_power_category__wise__plan_vs_actual_summary.man_power_category__wise__plan_vs_actual_summary.download';
				var args = "start_date=" + encodeURIComponent(frm.doc.date) +
					"&end_date=" + encodeURIComponent(frm.doc.to_date) +
					"&shift=" + encodeURIComponent(frm.doc.shift);  // Include shift in args
			}
		}
	
		if (path && args) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args
			});
		}
	},
	});
