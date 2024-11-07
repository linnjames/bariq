odoo.define('bi_pos_closed_session_reports.BiOrderReceipt', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class BiOrderReceipt extends PosComponent {
        constructor() {
            super(...arguments);
            this.user_tz = this.env.pos.user.tz;
        }
    }
    BiOrderReceipt.template = 'BiOrderReceipt';

    Registries.Component.add(BiOrderReceipt);

    return BiOrderReceipt;
});