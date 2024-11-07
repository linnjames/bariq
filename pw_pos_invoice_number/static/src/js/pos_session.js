odoo.define('pos_custom_receipt.OrderReceipt', function(require) {
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    const { onWillUpdateProps } = owl;

    const ExtendOrderReceipt = (OrderReceipt) =>
        class extends OrderReceipt {
            setup() {
                super.setup();
            }

            get_product_description(description){
                var cleanedResult = "";
                if (typeof description != "undefined") {
                    var tempDiv = document.createElement('div');
                    tempDiv.innerHTML = description;
                     cleanedResult = tempDiv.textContent || tempDiv.innerText || "";
                }
                return cleanedResult;
            }

        }
    Registries.Component.extend(OrderReceipt, ExtendOrderReceipt);
    return ExtendOrderReceipt;
});

