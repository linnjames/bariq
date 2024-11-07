odoo.define('pw_pos_invoice_number.models', function (require) {
    "use strict"

    var model = require("point_of_sale.models");
    const { PosGlobalState, Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');


    const PwONPosGlobalState = (PosGlobalState) => class PwONPosGlobalState extends PosGlobalState {
        _flush_orders(orders, options) {
            var self = this;
            var res = super._flush_orders(...arguments);
            _.each(orders, function (order) {
                if (!order.to_invoice)
                    res.then(function (order_server_id) {
                        self.env.services.rpc({
                            model: 'pos.order',
                            method: 'read',
                            args: [order_server_id[0]?.id, ['account_move']] // Using optional chaining operator
                        }).then(function (result_dict) {
                            if (result_dict.length) {
                                let invoice = result_dict[0].account_move[1].split(' ')[0];
                                self.get_order().invoice_number = invoice;
                            }
                        })
                            .catch(function (error) {
                                console.error(error);
                                // Handle error appropriately
                            })
                    })
            })
            return res
        }
    }

    Registries.Model.extend(PosGlobalState, PwONPosGlobalState);

    const PosOrderNumber = (Order) => class PosOrderNumber extends Order {
        export_for_printing() {
            var receipt = super.export_for_printing(...arguments);
            if (this.invoice_number) {
                receipt.invoice_number = this.invoice_number;

            }
            return receipt;
        }
    }
    Registries.Model.extend(Order, PosOrderNumber);
})

