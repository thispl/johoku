frappe.ui.form.on('Manpower Plan vs Actual', {
    refresh: function(frm) {
        frm.disable_save(); 
    },
    
    
    download: function(frm) {
        frm.trigger('get_data_system');
        
    },
    onload: function(frm) {
        frm.set_value("date", frappe.datetime.nowdate())
    },

    get_data_system: function(frm) {
        // frm.disable_save(); 
        frappe.call({
            freeze: true,
            freeze_message: 'Processing the data',
            method: "johoku.johoku.doctype.manpower_plan_vs_actual.manpower_plan_vs_actual.get_data_system",
            args: {
                date: frm.doc.date,
                shift: frm.doc.shift,
            },
            callback: function(r) {
                frm.fields_dict.plan_vs_actual.$wrapper.empty().append(r.message);
                // console.log(r.message)
            }
        });
    },

    get_data_system_for_all_shift: function(frm) {
        // frm.disable_save(); 
        frappe.call({
            freeze: true,
            freeze_message: 'Processing the data',
            method: "johoku.johoku.doctype.manpower_plan_vs_actual.manpower_plan_vs_actual.get_data_system_for_all_shift",
            args: {
                date: frm.doc.date,
            },
            callback: function(r) {
                frm.fields_dict.plan_vs_actual.$wrapper.empty().append(r.message);
                console.log("All shifts data loaded into plan_vs_actual field");
                // console.log(r.message)
            }
        });
    }
});
