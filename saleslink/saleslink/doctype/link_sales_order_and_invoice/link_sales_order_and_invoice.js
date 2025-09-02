// Copyright (c) 2025, Kanishkar and contributors
// For license information, please see license.txt

frappe.ui.form.on("Link Sales Order and Invoice", {
	refresh(frm) {
        frm.add_custom_button("Link", ()=>{
            let checked_so = (frm.doc.unlinked_sales_order || []).filter(row => row.__checked);
            // get checked sales invoices
            let checked_si = (frm.doc.unlinked_sales_invoice || []).filter(row => row.__checked);

            if (!checked_so.length || !checked_si.length) {
                frappe.msgprint("Please select at least one Sales Order and one Sales Invoice");
                return;
            }
            frappe.call({
                method : "saleslink.link_so_si.link_so_si",
                args : {
                    docname : frm.doc.name,
                    sales_order: checked_so.map(r => r.sales_order),
                    sales_invoice: checked_si.map(r => r.sales_invoice)
                }
            })
        })
	},
})