odoo.define('bi_pos_closed_session_reports.ZReport', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    const { useState, useRef } = owl.hooks;

    class ZReport extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this._onClick);
        }
        async _onClick() {
            var self = this;
            const { confirmed, payload } = await this.showPopup('SelectionSession', {
                title: this.env._t("Posted Session Report"),
            });
            if(confirmed){
                await this.env.pos.do_action('bi_pos_closed_session_reports.action_report_session_z', {
                    additional_context: {
                        active_ids: [payload],
                    },
                });
            }
        }
    }
    ZReport.template = 'ZReport';
    ProductScreen.addControlButton({
        component: ZReport,
        condition: function() {
            return this.env.pos.config.allow_posted_session_report;
        },
    });
    Registries.Component.add(ZReport);
    return ZReport;
});
