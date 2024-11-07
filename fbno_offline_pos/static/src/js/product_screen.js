
odoo.define('fbno_offline_pos.product_screen', function (require) {
    'use strict';

    var core = require('web.core');
    var _t = core._t;
    const { useListener } = require('web.custom_hooks');
    const SaleOrderManagementScreen = require('pos_sale.SaleOrderManagementScreen');
    const Registries = require('point_of_sale.Registries');
    const models = require('point_of_sale.models');
    const Orderline = models.Orderline;

    const { sprintf } = require('web.utils');
    const { parse } = require('web.field_utils');
    const { useContext } = owl.hooks;
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const SaleOrderFetcher = require('pos_sale.SaleOrderFetcher');
    const IndependentToOrderScreen = require('point_of_sale.IndependentToOrderScreen');
    const contexts = require('point_of_sale.PosContext');

    const CustomSaleOrderManagementScreen = (SaleOrderManagementScreen) =>
        class extends SaleOrderManagementScreen {
            constructor() {
                super(...arguments);
                useListener('close-screen', this.close);
                useListener('click-sale-order', this._onClickSaleOrder);
                useListener('next-page', this._onNextPage);
                useListener('prev-page', this._onPrevPage);
                useListener('search', this._onSearch);

                SaleOrderFetcher.setComponent(this);
                this.orderManagementContext = useContext(contexts.orderManagement);
            }

            mounted() {
                SaleOrderFetcher.on('update', this, this.render);
                this.env.pos.get('orders').on('add remove', this.render, this);

                const flexContainer = this.el.querySelector('.flex-container');
                const cpEl = this.el.querySelector('.control-panel');
                const headerEl = this.el.querySelector('.header-row');
                const val = Math.trunc(
                    (flexContainer.offsetHeight - cpEl.offsetHeight - headerEl.offsetHeight) /
                        headerEl.offsetHeight
                );
                SaleOrderFetcher.setNPerPage(val);

                setTimeout(() => SaleOrderFetcher.fetch(), 0);
            }

            willUnmount() {
                SaleOrderFetcher.off('update', this);
                this.env.pos.get('orders').off('add remove', null, this);
            }

            get selectedClient() {
                const order = this.orderManagementContext.selectedOrder;
                return order ? order.get_client() : null;
            }

            get orders() {
                return SaleOrderFetcher.get();
            }

            async _setNumpadMode(event) {
                const { mode } = event.detail;
                this.numpadMode = mode;
                NumberBuffer.reset();
            }

            _onNextPage() {
                SaleOrderFetcher.nextPage();
            }

            _onPrevPage() {
                SaleOrderFetcher.prevPage();
            }

            _onSearch({ detail: domain }) {
                SaleOrderFetcher.setSearchDomain(domain);
                SaleOrderFetcher.setPage(1);
                SaleOrderFetcher.fetch();
            }

            async _onClickSaleOrder(event) {
                const clickedOrder = event.detail;

                const { confirmed, payload: selectedOption } = await this.showPopup('SelectionPopup', {
                    title: this.env._t('What do you want to do?'),
                    list: [
                        { id: "0", label: this.env._t("Apply a down payment"), item: false },
                        { id: "1", label: this.env._t("Settle the order"), item: true }
                    ],
                });

                if (confirmed) {
                    let currentPOSOrder = this.env.pos.db.get_sale_orders();
                    let selected_sale_order = currentPOSOrder.find(order => order.id === clickedOrder.id);
                    if (selected_sale_order) {
                        let currentPOSOrder = this.env.pos.get_order();
                        let order_partner = this.env.pos.db.get_partner_by_id(selected_sale_order.partner_id[0]);
                        if (order_partner) {
                            currentPOSOrder.set_client(order_partner);
                        } else {
                            console.error("Partner not found in local database");
                        }
                    }

                    let orderFiscalPos = selected_sale_order.fiscal_position_id ? this.env.pos.fiscal_positions.find(
                        (position) => position.id === selected_sale_order.fiscal_position_id[0]
                    ) : false;
                    if (orderFiscalPos) {
                        this.env.pos.get_order().fiscal_position = orderFiscalPos;
                    }

                    let orderPricelist = selected_sale_order.pricelist_id ? this.env.pos.pricelists.find(
                          (pricelist) => pricelist.id === selected_sale_order.pricelist_id[0]
                    ): false;
                    if (orderPricelist){
                          currentPOSOrder.set_pricelist(orderPricelist);
                    }

                    if (selectedOption) {
                        // settle the order
                        let lines = selected_sale_order.order_lines;
                        let product_to_add_in_pos = lines.filter(line => !this.env.pos.db.get_product_by_id(line.product_id[0])).map(line => line.product_id[0]);


                        if (product_to_add_in_pos.length) {
                            const { confirmed } = await this.showPopup('ConfirmPopup', {
                                title: this.env._t('Products not available in POS'),
                                body: this.env._t('Some of the products in your Sale Order are not available in POS, do you want to import them?'),
                                confirmText: this.env._t('Yes'),
                                cancelText: this.env._t('No'),
                            });
                            if (confirmed) {
                                await this.env.pos._addProducts(product_to_add_in_pos);
                            }
                        }

                        let new_order = selected_sale_order.order_line;
                        for (let i = 0; i < lines.length; i++) {
                            let line = lines[i];
                            if (!this.env.pos.db.get_product_by_id(line.product_id[0])) {
                                continue;
                            }

                            let new_line = new models.Orderline({}, {
                                pos: this.env.pos,
                                order: this.env.pos.get_order(),
                                product: this.env.pos.db.get_product_by_id(line.product_id[0]),
                                description: line.product_id[1],
                                price: line.price_unit,
                                tax_ids: orderFiscalPos ? undefined : line.tax_id,
                                price_manually_set: true,
                                sale_order_origin_id: clickedOrder,
                                sale_order_line_id: line,
                                customer_note: line.customer_note,
                            });

                            this.env.pos.get_order().set_orderline_options(new_line, line);
                            new_line.set_unit_price(line.price_unit);
                            new_line.set_discount(line.discount);
                            new_line.set_quantity(line.product_uom_qty);

                            this.env.pos.get_order().add_orderline(new_line);
                        }
                    } else {
                       // apply a downpayment
                       if (this.env.pos.config.down_payment_product_id){

                           let lines = selected_sale_order.order_lines;

                           let tab = [];

                           for (let i=0; i<lines.length; i++) {
                               tab[i] = {
                                'product_name': lines[i].product_id[1],
                                'product_uom_qty': lines[i].product_uom_qty,
                                'price_unit': lines[i].price_unit,
                                'total': lines[i].price_total,
                               };
                           }
                           let down_payment_product = this.env.pos.db.get_product_by_id(this.env.pos.config.down_payment_product_id[0]);

                           if (!down_payment_product) {
                                await this.env.pos._addProducts([this.env.pos.config.down_payment_product_id[0]]);
                                down_payment_product = this.env.pos.db.get_product_by_id(this.env.pos.config.down_payment_product_id[0]);
                           }

                           let down_payment_tax = this.env.pos.taxes_by_id[down_payment_product.taxes_id] || false ;
                           let down_payment;
                           if (down_payment_tax) {
                                down_payment = down_payment_tax.price_include ? selected_sale_order.amount_total : selected_sale_order.amount_untaxed;
                           }
                           else{
                                down_payment = selected_sale_order.amount_total;
                           }

                           const { confirmed, payload } = await this.showPopup('NumberPopup', {
                                title: sprintf(this.env._t("Percentage of %s"), this.env.pos.format_currency(selected_sale_order.amount_total)),
                                startingValue: 0,
                           });
                           if (confirmed){
                                down_payment = down_payment * parse.float(payload) / 100;
                           }

                           if (down_payment > selected_sale_order.amount_unpaid) {
                                const errorBody = sprintf(
                                    this.env._t("You have tried to charge a down payment of %s but only %s remains to be paid, %s will be applied to the purchase order line."),
                                    this.env.pos.format_currency(down_payment),
                                    this.env.pos.format_currency(selected_sale_order.amount_unpaid),
                                    selected_sale_order.amount_unpaid > 0 ? this.env.pos.format_currency(selected_sale_order.amount_unpaid) : this.env.pos.format_currency(0),
                                );
                                await this.showPopup('ErrorPopup', { title: 'Error amount too high', body: errorBody });
                                down_payment = selected_sale_order.amount_unpaid > 0 ? selected_sale_order.amount_unpaid : 0;
                           }

                           let new_line = new models.Orderline({}, {
                                pos: this.env.pos,
                                order: this.env.pos.get_order(),
                                product: down_payment_product,
                                price: down_payment,
                                price_automatically_set: true,
                                sale_order_origin_id: clickedOrder,
                                down_payment_details: tab,
                            });
                            new_line.set_unit_price(down_payment);
                            this.env.pos.get_order().add_orderline(new_line);
                       }
                    }

                    // Trigger change event to update UI
                    this.env.pos.get_order().trigger('change');
                    this.showScreen('ProductScreen');
                }
            }
        };

    SaleOrderManagementScreen.template = 'SaleOrderManagementScreen';
    SaleOrderManagementScreen.hideOrderSelector = true;
    Registries.Component.extend(SaleOrderManagementScreen, CustomSaleOrderManagementScreen);
    return CustomSaleOrderManagementScreen;
});



