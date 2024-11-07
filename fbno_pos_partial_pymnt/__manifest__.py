# -*- coding: utf-8 -*-
{
    'name': "fbno_pos_partial_pymnt",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ALI",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale','account','pos_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/accnt_move_views_inh.xml',
        # 'views/res_config_settings_inh.xml',
    ],
'assets': {
        'point_of_sale.assets': [
            # 'fbno_pos_expenses/static/src/css/style.css',
            'fbno_pos_partial_pymnt/static/src/js/customer_credit_amount.js',
            'fbno_pos_partial_pymnt/static/src/js/pos_pymnt.js',
            'fbno_pos_partial_pymnt/static/src/js/popup_button.js',
            # 'fbno_pos_partial_pymnt/static/src/js/demo.js',
            'fbno_pos_partial_pymnt/static/src/js/set_soline_qty.js',
            'fbno_pos_partial_pymnt/static/src/js/auto_pos_invoice.js',
            'fbno_pos_partial_pymnt/static/src/js/pos_invoice_report.js',
            'fbno_pos_partial_pymnt/static/src/js/pos_offline.js',
        ],
        'web.assets_qweb': ['fbno_pos_partial_pymnt/static/src/xml/pos_paymnt_view.xml',
                            'fbno_pos_partial_pymnt/static/src/xml/credit_pymnt.xml',
                            # 'fbno_pos_partial_pymnt/static/src/xml/sale_order_mngmnt.xml',
                            ],
    },

}
