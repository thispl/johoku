// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Power Trend', {
	// refresh: function(frm) {

	// }
	download(frm) {

		if (frm.doc.from_date && frm.doc.to_date) {  // Ensure both date and shift are present
			var path = 'johoku.johoku.doctype.maintenance_power_trend.maintenance_power_trend_new.download';
			var args = "from_date=" + encodeURIComponent(frm.doc.from_date) +
				"&to_date=" + encodeURIComponent(frm.doc.to_date);  // Include shift in args
		}
		if (path && args) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				from_date:frm.doc.from_date,
				to_date:frm.doc.to_date
			});
		}
	}
});
