odoo.define('bi_pos_closed_session_reports.SelectionReportType', function(require) {
	'use strict';

	const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require('web.custom_hooks');
	const rpc = require('web.rpc');
	let core = require('web.core');
	let _t = core._t;

	class SelectionReportType extends AbstractAwaitablePopup {
		constructor() {
			super(...arguments);
		}

		confirm_report_type(){
		    var value_type = ''
            var ele = document.getElementsByName('type');
            for (var i = 0; i < ele.length; i++) {
                if (ele[i].checked){
                    value_type = ele[i].value
                }
            }
            if (value_type == "pdf" || value_type == "receipt"){
                this.props.resolve({ confirmed: true, payload: value_type });
                this.trigger('close-popup');
            } else{
                alert("please select type")
            }
		}

        cancel() {
			this.props.resolve({ confirmed: false, payload: null });
			this.trigger('close-popup');
		}
	}

	SelectionReportType.template = 'SelectionReportType';
	SelectionReportType.defaultProps = {
		confirmText: 'Print',
		cancelText: 'Close',
		body: '',
	};
	Registries.Component.add(SelectionReportType);
	return SelectionReportType;
});
