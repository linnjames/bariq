odoo.define('fbno_pos_partial_pymnt.pos_pymnt',function(require) {
    "use strict";

var gui = require('point_of_sale.Gui');
var core = require('web.core');
 var rpc = require('web.rpc');

var QWeb = core.qweb;

    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const { useState, useRef } = owl.hooks;
    const { Gui } = require('point_of_sale.Gui');




    class PayPartialPaymentPopupWidget extends PosComponent {


        constructor() {
            super(...arguments);

            this.options = {};
            this.uom_list = [];

            }

        mounted(options){

//            var current_uom = this.env.pos.units_by_id[this.props.options.uom_list[0]];
            var uom_list = this.env.pos.expense_types;
            var exp_prdcts = this.env.pos.expense_types;

//            var uom_by_category = this.get_units_by_category(uom_list, current_uom.category_id);
            this.uom_list = this.env.pos.expense_types;
//            this.current_uom = this.props.options.uom_list[0];
//            this.render();

        }



    click_confirm(){
                var self = this;
				var entered_code = parseFloat($("#entered_amount").val());
				var payment_type = document.getElementById("payment_type");
				var value = payment_type.value;
                var pyment_type =payment_type.options[payment_type.selectedIndex].text;
                var customer = this.env.pos.get_order().get_client();

				console.log("888888888888888888888----",pyment_type,entered_code,value,partner_id,self.env.pos.config.partial_journal_id[0]);
				var partial_journal = self.env.pos.config.partial_journal_id[0];
				var partner_id = customer;
				var pos_confg = self.env.pos.config.name;
				var pos_session_id = self.env.pos.pos_session.name;

				if (!partner_id) {
					Gui.showPopup('ErrorPopup', {
                        title: 'Unknown customer',
                        body: 'You cannot Pay Partial Payment. Set customer first.',
                    });
					return;
				}
				else {
				rpc.query({
                    model: 'res.partner',
                    method: 'pay_partial_payment',
                    args: [partner_id ? partner_id.id : 0,pos_confg,pos_session_id,partner_id,entered_code,value,partial_journal,pyment_type],
                }).then(function(output_amount) {
                     alert('Credit Payment Done !!!!');
//									var partial = partner_id.custom_credit - output_amount;
//									rpc.query({
//										model: 'res.partner',
//										method: 'write',
//										args: [[partner_id.id], {'custom_credit': partial}],
//									});
//									self.gui.show_screen('partial_payment_receipt',{
//										journal_entry : output,
//										partner_id : partner_id,
//										amount: entered_code,
//									});
                });
}
//
        this.trigger('close-popup');
        return;

    }
    click_cancel(){
        this.trigger('close-popup');
    }

    }

    PayPartialPaymentPopupWidget.template = 'PayPartialPaymentPopupWidget';
    PayPartialPaymentPopupWidget.defaultProps = {
        confirmText: 'Return',
        cancelText: 'Cancel',
        title: 'Confirm ?',
        body: '',
    };
    Registries.Component.add(PayPartialPaymentPopupWidget);
    return PayPartialPaymentPopupWidget;
});

