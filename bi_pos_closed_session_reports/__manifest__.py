# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "POS Cash register Z-Report in Odoo ",
    "version" : "15.0.1.0",
    "category": "Point of Sale",
    "depends": ['base', 'sale', 'point_of_sale'],
    "author": "BrowseInfo",
    'summary': 'Using apps POS Closed Session Report generate pos session report pos Closed sessions report POS-BOX Compatible pos day summer report pos daily reports pos session report pos z reports for POS Cash register pos session report pos sales report pos report',
    "description": """
	POS Closed Session Report in Odoo,
	Posted Session Report in odoo,
	Posted Session Report in PDF odoo apps,
	Closed Session Report in odoo,
	POS Session Report in odoo,
	PDF Report for Closed Session in odoo,
	POS Closed Session Report in Odoo End-of-Day Cheat Sheet Cash register reports pos Cash register reports
	Shift Report with Sales Summary at the POS 
	pos Shift Report with Sales Summary at the POS  Cash register right Daily report
	Daily session report End of day service POS Reporting shift POS Reporting
	pos shift reports Daily Z reports CASIO Standard Daily Z Reports
	pos end Shift Report with Sales Summary at the POS POS Cash register Z-Report POS Cash register Z-Report
	pos session ended reports pos closed session report pos session reports
	pos end of Shift Report with Sales Summary at the POS
	Posted Session Report in odoo POS Z Report Cash Register Closing Report Closed Session Report
	Z-Report - End of Day Report print z-report from Odoo point of sale
	Z Report End of Day Report closed session report Cash Register Closing Report
	Posted Session Report in PDF odoo apps,
	Closed Session Report in odoo,
	pos sales summery reports
	POS Cash register End Of Session Z-Report Odoo Apps support both community as well as enterprise version. This Point of sales module will allow user to print POS Closed Session Reports which consist total tranasaction and sales summery report at End of shift and total sales summery of session. You can generate report for Closed sessions in PDF format and This odoo apps is POS-BOX Compatible. 
	POS Session Report in odoo,
	PDF Report for Closed Session in odoo balancing the cash drawer 
	Generate POS Closed Session report in odoo,
	Generate POS Closed Session report in odoo,
	""",
    "website": "https://www.browseinfo.com",
    "price": 12,
    "currency": "EUR",
    "data": [
        'security/ir.model.access.csv',
        'data/pos_session_receipt_email_template.xml',
        'views/pos_config.xml',
        'wizard/close_session_report_view.xml',
        'views/pos_session_report.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'bi_pos_closed_session_reports/static/src/js/models.js',
            'bi_pos_closed_session_reports/static/src/js/Popup/SelectionReportTypePopup.js',
            'bi_pos_closed_session_reports/static/src/js/Popup/SelectionSessionPopup.js',
            'bi_pos_closed_session_reports/static/src/js/Screens/ProductScreen/ControlButtons/SessionReport.js',
            'bi_pos_closed_session_reports/static/src/js/Screens/ProductScreen/ControlButtons/ZReport.js',
            'bi_pos_closed_session_reports/static/src/js/Screens/TicketScreen/TicketScreen.js',
            'bi_pos_closed_session_reports/static/src/js/Screens/BiReceiptScreen/BiOrderReceipt.js',
            'bi_pos_closed_session_reports/static/src/js/Screens/BiReceiptScreen/BiReceiptScreen.js',
        ],
        'web.assets_qweb': [
            'bi_pos_closed_session_reports/static/src/xml/Popup/SelectionReportTypePopup.xml',
            'bi_pos_closed_session_reports/static/src/xml/Popup/SelectionSessionPopup.xml',
            'bi_pos_closed_session_reports/static/src/xml/Screens/ProductScreen/ControlButtons/SessionReport.xml',
            'bi_pos_closed_session_reports/static/src/xml/Screens/BiReceiptScreen/BiOrderReceipt.xml',
            'bi_pos_closed_session_reports/static/src/xml/Screens/BiReceiptScreen/BiReceiptScreen.xml',
        ],
    },
    "auto_install": False,
    "installable": True,
    "images": ['static/description/Banner.gif'],
    "live_test_url": 'https://youtu.be/INvzMNG3foo',
    'license': 'OPL-1',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
