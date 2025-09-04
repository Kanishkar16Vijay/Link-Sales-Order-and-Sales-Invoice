frappe.ui.form.on("Link Sales Order and Invoice", {
	refresh: function(frm) {
        frm.add_custom_button("Link", ()=>{
            
            let checked_so = (frm.doc.unlinked_sales_order || []).filter(row => row.__checked);
            // get checked sales invoices
            let checked_si = (frm.doc.unlinked_sales_invoice || []).filter(row => row.__checked);

            if (!checked_so.length || !checked_si.length) {
                frappe.msgprint("Please select at least one Sales Order and one Sales Invoice");
                return;
            }
            if (checked_so.length > 1 || checked_si.length > 1) {
                frappe.msgprint("Please select only one Sales Order and one Sales Invoice");
                return;
            }

            so = checked_so.map(r => r.sales_order)
            si = checked_si.map(r => r.sales_invoice)

            frappe.call({
                method : "frappe.client.get_list",
                args : {
                    doctype: "Sales Order Invoice Link Request",
                    filters: {
                        customer: frm.doc.customer,
                        sales_order: so[0],
                        sales_invoice: si[0],
                        status: ["in", ["Pending", "Rejected"]]
                    },
                    fields: ["name", "status"]
                },

                callback: function(r){
                    if(r.message && r.message.length > 0){
                        frappe.msgprint(`The request is already <b>${r.message[0].status}</b>`)
                    }
                    else{
                        frappe.call({
                            method : "frappe.client.insert",
                            args : {
                                doc : {
                                    doctype : "Sales Order Invoice Link Request",
                                    customer : frm.doc.customer,
                                    status : "Pending",
                                    sales_order : so[0],
                                    sales_invoice : si[0],
                                    request_by : frappe.session.user
                                }
                            },

                            callback: function(r){
                                if(!r.exc){
                                    frappe.call({
                                        method : "frappe.client.submit",
                                        args : {
                                            doc : r.message
                                        },

                                        callback: function(r){
                                            if(!r.exc){
                                                frappe.msgprint("Sales Order Invoice Link Request Submitted Successfully!")
                                            }
                                        }
                                    })
                                }
                            }
                        })
                    }
                }
            })
        })
	},
})
