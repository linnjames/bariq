odoo.define('fbno_pos_partial_pymnt.pos_invoice_report', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');

    models.PosModel = models.PosModel.extend({
        push_and_invoice_order: function (order) {
        var self = this;
        return new Promise((resolve, reject) => {
            if (!order.get_client()) {
                reject({ code: 400, message: 'Missing Customer', data: {} });
            } else {
                var order_id = self.db.add_order(order.export_as_JSON());
                self.flush_mutex.exec(async () => {
                    try {
                        const server_ids = await self._flush_orders([self.db.get_order(order_id)], {
                            timeout: 30000,
                            to_invoice: true,
                        });
                        if (server_ids.length) {
                            const [orderWithInvoice] = await self.rpc({
                                method: 'read',
                                model: 'pos.order',
                                args: [server_ids, ['account_move']],
                                kwargs: { load: false },
                            });
                                  await self.do_action('base_customisation.action_vat_account_invoices', {
                                    additional_context: {
                                        active_ids: [orderWithInvoice.account_move],
                                    },
                                })
                                .catch(() => {
                                    reject({ code: 401, message: 'Backend Invoice', data: { order: order } });
                                });



                        } else {
                            reject({ code: 401, message: 'Backend Invoice', data: { order: order } });
                        }
                        resolve(server_ids);
                    } catch (error) {
                        reject(error);
                    }
                });
            }
        });
    },

});
});