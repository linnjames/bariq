
odoo.define('fbno_offline_pos.pos_offline', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var PosDB = require('point_of_sale.DB');
    var core = require('web.core');
    var _t = core._t;
    const { Gui } = require('point_of_sale.Gui');
    const SetSaleOrderButton = require('pos_sale.SetSaleOrderButton');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const IndependentToOrderScreen = require('point_of_sale.IndependentToOrderScreen');
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { isConnectionError } = require('point_of_sale.utils');

    models.load_models({
        model: 'sale.order',
        fields: ['id', 'date_order', 'name', 'partner_id', 'user_id', 'amount_total', 'state', 'payment_term_id', 'order_line'],
        domain: null,
        loaded: function(self, orders) {
            self.orders = orders;
            self.db.add_sale_orders(orders);
        },
    });

    models.load_models({
        model: 'sale.order.line',
        fields: ['id', 'order_id', 'product_id', 'price_unit', 'name', 'product_uom_qty'],
        domain: null,
        loaded: function(self, order_lines) {
            self.order_lines = order_lines;
            self.db.add_sale_order_lines(order_lines);
        },
    });


    PosDB.include({
        init: function(options) {
            this._super(options);
            this.sale_orders = [];
            this.sale_order_lines = [];
        },
        add_sale_orders: function(orders) {
            this.sale_orders = orders;
        },
        add_sale_order_lines: function(order_lines) {
            this.sale_order_lines = order_lines;
            this.sale_orders.forEach(order => {
                order.order_lines = order_lines.filter(line => line.order_id[0] === order.id);
            });
        },
        get_product_by_id: function(id){
            return this.product_by_id[id];
        },
        get_sale_orders: function() {
            return this.sale_orders;
        },
        get_sale_order_lines: function() {
            return this.sale_order_lines;
        },
    });

    const SetSaleOrderButtonExtend = (SetSaleOrderButton) =>

        class extends SetSaleOrderButton {
            async onClick() {
                const sale_orders = this.env.pos.db.get_sale_orders();
                this.showScreen('SaleOrderManagementScreen');
            }
        }

    SetSaleOrderButtonExtend.template = 'SetSaleOrderButton';

    Registries.Component.extend(SetSaleOrderButton, SetSaleOrderButtonExtend);
    return SetSaleOrderButton;
});







