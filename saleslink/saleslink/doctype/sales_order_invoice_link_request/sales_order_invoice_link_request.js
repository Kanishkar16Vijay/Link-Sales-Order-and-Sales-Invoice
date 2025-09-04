frappe.ui.form.on("Sales Order Invoice Link Request", {
	refresh: function(frm) {
        if(frappe.user.has_role("Sales Order Invoice Linker") && frm.doc.status == "Pending"){
            frm.add_custom_button("Link", ()=>{
                frappe.call({
                    method : "saleslink.link_so_si.link_so_si",
                    args : {
                        sales_order : frm.doc.sales_order,
                        sales_invoice : frm.doc.sales_invoice,
                        link_name : frm.doc.name
                    }
                })
            })
        }
	},
});
