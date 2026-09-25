// frappe.ui.form.on("Full and Final Settlement", {

//     employee: function(frm) {
//         fetch_salary(frm);
//     },

// });


frappe.ui.form.on("Full and Final Settlement", {

    employee: function(frm) {
        fetch_salary(frm);
    },

    previous_year_bonus: function(frm) {
        update_bonus(frm);
    },

    current_year_bonus: function(frm) {
        update_bonus(frm);
    },
    

    notice_period_recovery: function(frm){
        update_npr(frm);
    },
    lop_days: function(frm){
        update_lop(frm);
    },
    
    validate: function(frm){
        calculate_totals(frm);
    },
    current_year_el: function(frm) {

        let existing = 0;

        (frm.doc.earning || []).forEach(row => {
            if (row.salary_component === "EL Encashment") {
                existing = row.earned_amount || 0;
            }
        });


        let fixed_basic = frm.doc.fixed_basic || 0;
        let working_days = frm.doc.total_working_days || 0;
        let el_days = frm.doc.el_leave_days || 0;
        let current_el = frm.doc.current_year_el || 0;

        if (!working_days) {
            return;
        }

        let per_day = fixed_basic / working_days;

        let new_el = existing + Math.ceil(per_day * (el_days + current_el));


        let row = (frm.doc.earning || []).find(r => r.salary_component === "EL Encashment");

        if (row) {
            row.earned_amount = new_el;
        }

        frm.refresh_field("earning");

    },

    days_worked: function(frm) {

        if (!frm.doc.employee || !frm.doc.relieving_date || !frm.doc.days_worked) return;

        frappe.call({
            method: "johoku.johoku.doctype.full_and_final_settlement.full_and_final_settlement.this_month_salary",
            args: {
                employee: frm.doc.employee,
                relieving_date: frm.doc.relieving_date,
                days_worked: frm.doc.days_worked   
            },
            // callback: function(r) {

            //     if (!r.message) return;

            //     let data = r.message;
                
            //     data.earning.forEach(calc_row => {

            //         let existing_row = frm.doc.earnings.find(
            //             e => e.salary_component === calc_row.salary_component
            //         );

            //         if (existing_row) {
            //             existing_row.amount = calc_row.earned_amount;
            //         }
            //     });

            //     frm.refresh_field("earning");

            // }
            callback: function(r) {

                if (!r.message) return;

                let data = r.message;

                console.log(data);
                console.log("Returned Data", data);
                console.log("Earnings Table", frm.doc.earning);
                console.log("Returned Earnings", data.earnings);
                console.log("Form Earnings", frm.doc.earning);
                data.earnings.forEach(calc_row => {

                    console.log("Searching:", calc_row.salary_component);

                    let existing_row = frm.doc.earning.find(
                        e => (e.salary_component || "").trim().toLowerCase() ===
                            (calc_row.salary_component || "").trim().toLowerCase()
                    );

                    console.log("Found Row:", existing_row);

                    if (existing_row) {

                        existing_row.amount = calc_row.earned_amount;
                        existing_row.earned_amount = calc_row.earned_amount;
                        existing_row.fixed_amount = calc_row.fixed_amount;
                        console.log(
                            existing_row.salary_component,
                            existing_row.amount,
                            existing_row.earned_amount
                        );
                    }
                });

                frm.refresh_field("earning");
            }
            
        });
    }

});

// function update_bonus(frm) {

//     let prev_bonus = flt(frm.doc.previous_year_bonus);
//     let curr_bonus = flt(frm.doc.current_year_bonus);

//     // remove existing Bonus
//     (frm.doc.earning || []).forEach(row => {
//         if (row.salary_component === "Bonus") {
//             frappe.model.clear_doc(row.doctype, row.name);
//         }
//     });

//     if (prev_bonus > 0 || curr_bonus > 0) {

//         let total_bonus = prev_bonus + curr_bonus;
//         let bonus_amount = total_bonus * 8.33;  // ✅ correct %

//         let child = frm.add_child("earning");
//         child.salary_component = "Bonus";
//         child.earned_amount = bonus_amount;
//         child.fixed_amount = 0;
//     }

//     frm.refresh_field("earning");
// }

function update_bonus(frm) {

    let prev_amt = flt(frm.doc.previous_year_basic);
    let curr_amt = flt(frm.doc.fixed_basic);

    let prev_month = flt(frm.doc.previous_year_bonus);
    let curr_month = flt(frm.doc.current_year_bonus);

    // Remove existing Bonus row
    (frm.doc.earning || []).forEach(row => {
        if (row.salary_component === "Bonus") {
            frappe.model.clear_doc(row.doctype, row.name);
        }
    });

    // Current year bonus
    let current_bonus = (curr_amt * 8.33 / 100) * curr_month;

    // Previous year bonus
    let previous_bonus = (prev_amt * 8.33 / 100) * prev_month;

    // Total bonus
    let total_bonus = current_bonus + previous_bonus;

    if (total_bonus > 0) {

        let child = frm.add_child("earning");

        child.salary_component = "Bonus";
        child.earned_amount = total_bonus;
        child.fixed_amount = 0;
    }

    frm.refresh_field("earning");
}

function calculate_gratuity(frm) {
    console.log("HI1");
    let basic = flt(frm.doc.fixed_basic);
    let doj = frm.doc.date_of_joining;
    let relieving = frm.doc.relieving_date;

    if (!basic || !doj || !relieving) return;

    let start = moment(doj);
    let end = moment(relieving);

    let years = end.diff(start, 'years');
    let months = end.diff(start.add(years, 'years'), 'months');
    console.log(years);
    console.log(months);
    if (months >= 8) {
        years += 1;
    }
    console.log("HI3");
    console.log(years);
    // remove existing Gratuity
    (frm.doc.earning || []).forEach(row => {
        if (row.salary_component === "Gratuity") {
            frappe.model.clear_doc(row.doctype, row.name);
        }
    });

    // if (years < 5) {
    //     frm.refresh_field("earning");
    //     return;
    // }

    let gratuity = (basic * 15 * years) / 26;
    console.log("HI4");
    let child = frm.add_child("earning");
    child.salary_component = "Gratuity";
    child.earned_amount = gratuity;
    child.fixed_amount = 0;
    console.log(gratuity);
    frm.refresh_field("earning");
}


function update_npr(frm) {

    console.log("NPR");

    let npr = flt(frm.doc.notice_period_recovery);

    let fixed_amount = flt(frm.doc.fixed_basic);
    let working_days = flt(frm.doc.total_working_days);

    let category = frm.doc.employee_category;

    // Staff special condition
    if (category == "Staff" && working_days > 31) {
        working_days = working_days - 15;
    }

    // Remove existing NPR row
    (frm.doc.deduction || []).forEach(row => {
        if (row.salary_component === "Notice Period Recovery") {
            frappe.model.clear_doc(row.doctype, row.name);
        }
    });
    console.log(working_days)
    // NPR Calculation
    let total_npr = (fixed_amount / working_days) * npr;

    console.log(total_npr);

    if (npr > 0) {

        let child = frm.add_child("deduction");

        child.salary_component = "Notice Period Recovery";
        child.deductions_amount = total_npr;
    }

    frm.refresh_field("deduction");
}


function update_lop(frm) {

    console.log("LOP");

    let lop = flt(frm.doc.lop_days);

    let fixed_amount = flt(frm.doc.fixed_basic);
    let working_days = flt(frm.doc.total_working_days);

    let category = frm.doc.employee_category;

    // Staff special condition
    if (category == "Staff" && working_days > 31) {
        working_days = working_days - 15;
    }

    // Remove existing NPR row
    (frm.doc.deduction || []).forEach(row => {
        if (row.salary_component === "LOP") {
            frappe.model.clear_doc(row.doctype, row.name);
        }
    });
    let total_lop = (fixed_amount / working_days) * lop;
    if (lop > 0) {

        let child = frm.add_child("deduction");

        child.salary_component = "LOP";
        child.deductions_amount = total_lop;
    }

    frm.refresh_field("deduction");
}



function fetch_salary(frm) {
    if (frm.doc.employee && frm.doc.relieving_date) {

        frappe.call({
            method: "johoku.johoku.doctype.full_and_final_settlement.full_and_final_settlement.get_salary_details",
            args: {
                employee: frm.doc.employee,
                relieving_date: frm.doc.relieving_date,
                fixed_basic: frm.doc.fixed_basic, 
                working_days: frm.doc.total_working_days,
                el_leave_days: frm.doc.el_leave_days
                
            },
            callback: function(r) {
                if (r.message) {

                    let data = r.message;

                    frm.set_value("no_of_present_days", data.payment_days);
                    frm.set_value("lop_days", data.lop_days);
                    frm.set_value("total_working_days", data.total_working_days);
        
                    frm.set_value("total_payable_amount", data.total_payable_amount);
                    frm.set_value("total_receivable_amount", data.total_receivable_amount);
                    frm.clear_table("earning");
                    frm.clear_table("deduction");

                    (data.earnings || []).forEach(e => {
                        let row = frm.add_child("earning");
                        row.salary_component = e.salary_component;
                        row.earned_amount = e.earned_amount;
                        row.fixed_amount = e.fixed_amount;
                    });

                    (data.deductions || []).forEach(d => {
                        let row = frm.add_child("deduction");
                        row.salary_component = d.salary_component;
                        row.deductions_amount = d.deductions_amount;
                    });

                    frm.refresh_field("earning");
                    frm.refresh_field("deduction");

                    console.log("HI");
                    calculate_gratuity(frm);
                    update_bonus(frm);
                    update_npr(frm);
                    update_lop(frm);
                    calculate_totals(frm);
                    let manual_items = ["Uniform", "Shoe", "Laptop", "Cap","Other Earnings"];

                    manual_items.forEach(item => {

                        // avoid duplicate
                        let exists = (frm.doc.earning || []).some(r => r.salary_component === item);

                        if (!exists) {
                            let child = frm.add_child("earning");
                            child.salary_component = item;
                            child.earned_amount = 0;   
                            child.fixed_amount = 0;
                        }
                    });

                    frm.refresh_field("earning");


                    let manual_deductions = ["Other Deductions", "Notice Period Recovery", "LOP"];

                    manual_deductions.forEach(item => {

                        // avoid duplicate
                        let exists = (frm.doc.deduction || []).some(
                            r => r.salary_component === item
                        );

                        if (!exists) {
                            let child = frm.add_child("deduction");

                            child.salary_component = item;
                            child.deductions_amount = 0;
                        }
                    });

                    frm.refresh_field("deduction");
                }
            }
        });

        frappe.call({
            method: "johoku.johoku.doctype.full_and_final_settlement.full_and_final_settlement.get_el_leave_balance",
            args: {
                employee: frm.doc.employee,
                relieving_date: frm.doc.relieving_date
            },
            callback: function(r) {
                if (r.message !== undefined) {
                    frm.set_value("el_leave_days", r.message);
                }
            }
        });

        
    }
}


function calculate_totals(frm) {

    let total_earnings = 0;
    let total_deductions = 0;

    // Earnings Total
    (frm.doc.earning || []).forEach(row => {
        total_earnings += flt(row.earned_amount);
    });

    // Deduction Total
    (frm.doc.deduction || []).forEach(row => {
        total_deductions += flt(row.deductions_amount);
    });

    frm.set_value("total_payable_amount", total_earnings);

    frm.set_value("total_receivable_amount", total_deductions);
}