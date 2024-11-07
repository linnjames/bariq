odoo.define('bi_pos_closed_session_reports.SelectionSession', function(require) {
	'use strict';

	const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require('web.custom_hooks');
	const rpc = require('web.rpc');
	let core = require('web.core');
	let _t = core._t;

	class SelectionSession extends AbstractAwaitablePopup {
		constructor() {
			super(...arguments);
		}

		confirm_session(){
            var list_of_data = $('.table-data');
            var self = this;
            $.each(list_of_data, function(index, value) {
                var SelectedSession = $(value).find('select').val();
                if(!SelectedSession){
                    alert("Please Select Session");
                } else {
                    self.props.resolve({ confirmed: true, payload: SelectedSession });
			        self.trigger('close-popup');
                }
            });
		}

        cancel() {
			this.props.resolve({ confirmed: false, payload: null });
			this.trigger('close-popup');
		}
	}

	SelectionSession.template = 'SelectionSession';
	SelectionSession.defaultProps = {
		confirmText: 'Print',
		cancelText: 'Close',
		body: '',
	};
	Registries.Component.add(SelectionSession);
	return SelectionSession;
});
