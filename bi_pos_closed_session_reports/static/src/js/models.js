odoo.define('bi_pos_closed_session_reports.Models', function (require) {
"use strict";

    var models = require('point_of_sale.models');
    models.load_fields('res.company', ['street', 'street2', 'city', 'country_id', 'state_id']);
	models.load_fields('res.users', ['tz']);

    models.load_models({
		model: 'pos.session',
		fields: [],
		domain: null,
		loaded: function(self, sessions_list) {
			self.sessions_list = sessions_list;
		},
	});
});