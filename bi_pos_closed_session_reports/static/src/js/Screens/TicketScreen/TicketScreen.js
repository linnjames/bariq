odoo.define('bi_pos_closed_session_reports.BiTicketScreen', function(require) {
	'use strict';

	const TicketScreen = require('point_of_sale.TicketScreen');
	const Registries = require('point_of_sale.Registries');
	let check_do = true;

	const BiTicketScreen = (TicketScreen) => class extends TicketScreen {
        constructor() {
            super(...arguments);
        }
        _getScreenToStatusMap() {
            return {
                ProductScreen: 'ONGOING',
                PaymentScreen: 'PAYMENT',
                ReceiptScreen: 'RECEIPT',
                BiReceiptScreen: 'BIRECEIPT',
            };
        }
        _getOrderStates() {
            const states = new Map();
            states.set('ACTIVE_ORDERS', {
                text: this.env._t('All active orders'),
            });
            states.set('ONGOING', {
                text: this.env._t('Ongoing'),
                indented: true,
            });
            states.set('PAYMENT', {
                text: this.env._t('Payment'),
                indented: true,
            });
            states.set('RECEIPT', {
                text: this.env._t('Receipt'),
                indented: true,
            });
            states.set('BIRECEIPT', {
                text: this.env._t('Session Receipt'),
                indented: true,
            });
            return states;
        }
    }
	Registries.Component.extend(TicketScreen, BiTicketScreen);
	return TicketScreen;
});