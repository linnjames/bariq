odoo.define('fbno_pos_partial_pymnt.SaleOrderManagementScreeninh', function (require) {
    'use strict';

    const { sprintf } = require('web.utils');
    const { parse } = require('web.field_utils');
    const { useContext } = owl.hooks;
    const { useListener } = require('web.custom_hooks');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const Registries = require('point_of_sale.Registries');
    const SaleOrderFetcher = require('pos_sale.SaleOrderFetcher');
    const IndependentToOrderScreen = require('point_of_sale.IndependentToOrderScreen');
    const contexts = require('point_of_sale.PosContext');
    const models = require('point_of_sale.models');

    class SaleOrderManagementScreen extends ControlButtonsMixin(IndependentToOrderScreen) {
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

            // calculate how many can fit in the screen.
            const flexContainer = this.el.querySelector('.flex-container');
            const cpEl = this.el.querySelector('.control-panel');
            const headerEl = this.el.querySelector('.header-row');
            const val = Math.trunc(
                (flexContainer.offsetHeight - cpEl.offsetHeight - headerEl.offsetHeight) /
                    headerEl.offsetHeight
            );
            SaleOrderFetcher.setNPerPage(val);

            // Fetch the order after mounting so that order management screen
            // is shown while fetching.
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
                    { id: "1", label: this.env._t("Settle the order"), item: true },
                    { id: "2", label: this.env._t("PRINT PRO-FORMA INVOICE"), item: false }
                ],
            });

            if (confirmed) {
                let currentPOSOrder = this.env.pos.db.get_sale_orders();
                let selected_sale_order = currentPOSOrder.find(order => order.id === clickedOrder.id);
                if (selected_sale_order) {
                    currentPOSOrder = this.env.pos.get_order();
                    let order_partner = this.env.pos.db.get_partner_by_id(selected_sale_order.partner_id[0]);
                    if (order_partner) {
                        currentPOSOrder.set_client(order_partner);
                    } else {
                        console.error("Partner not found in local database");
                    }

                    let orderFiscalPos = selected_sale_order.fiscal_position_id ? this.env.pos.fiscal_positions.find(
                        (position) => position.id === selected_sale_order.fiscal_position_id[0]
                    ) : false;
                    if (orderFiscalPos) {
                        this.env.pos.get_order().fiscal_position = orderFiscalPos;
                    }

                    let orderPricelist = selected_sale_order.pricelist_id ? this.env.pos.pricelists.find(
                        (pricelist) => pricelist.id === selected_sale_order.pricelist_id[0]
                    ) : false;
                    if (orderPricelist) {
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
                    // print proforma
                        let sale_order = await this._getSaleOrder(clickedOrder.id);
                        await this.env.pos.do_action("base_customisation.action_report_pro_forma_invoice_custom_pdf", {
                            additional_context: { active_ids: [sale_order.id] },
                        });
                    }

                    this.env.pos.get_order().trigger('change');
                    this.showScreen('ProductScreen');
                    this.close();
                }
            }
        }

        async _getSaleOrder(id) {
            const sale_order = await this.rpc({
                model: 'sale.order',
                method: 'read',
                args: [[id], ['order_line', 'partner_id', 'pricelist_id', 'fiscal_position_id', 'amount_total', 'amount_untaxed']],
                context: this.env.session.user_context,
            });

            const saleOrdersAmountUnpaid = await this.rpc({
                model: 'sale.order',
                method: 'get_order_amount_unpaid',
                args: [[id]],
                context: this.env.session.user_context,
            });
            sale_order[0].amount_unpaid = saleOrdersAmountUnpaid[sale_order[0].id];

            const sale_lines = await this._getSOLines(sale_order[0].order_line);
            const promo_products_to_remove = this.env.pos.promo_programs ? this.env.pos.promo_programs.flatMap(program => program.promo_code_usage === 'no_code_needed' ? program.discount_line_product_id[0] : []) : [];
            sale_order[0].order_line = sale_lines.filter(line => !promo_products_to_remove.includes(line.product_id[0]));

            return sale_order[0];
        }

        async _getSOLines(ids) {
            let so_lines = await this.rpc({
                model: 'sale.order.line',
                method: 'read_converted',
                args: [ids],
                context: this.env.session.user_context,
            });
            return so_lines;
        }
    }

    SaleOrderManagementScreen.template = 'SaleOrderManagementScreen';
    SaleOrderManagementScreen.hideOrderSelector = true;

    Registries.Component.add(SaleOrderManagementScreen);

    return SaleOrderManagementScreen;
});
