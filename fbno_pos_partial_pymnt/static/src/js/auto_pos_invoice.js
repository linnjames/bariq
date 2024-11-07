odoo.define('fbno_pos_partial_pymnt.auto_pos_invoice', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosInvoiceAutomatePaymentScreen = (PaymentScreen) =>
          class extends PaymentScreen {
              constructor() {
                 super(...arguments);
                 if(this.env.pos.config.invoice_auto_check){
                    this.currentOrder.set_to_invoice(true);
                 }
              }
          };

    Registries.Component.extend(PaymentScreen, PosInvoiceAutomatePaymentScreen);

    return PaymentScreen;
});