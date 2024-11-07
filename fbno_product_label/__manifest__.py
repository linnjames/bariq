# -*- coding: utf-8 -*-
{
    'name': "Ingredients in Product Label",
    'summary': """Ingredients in Product Label""",
    'description': """ Ingredients in Product Label""",
    'author': "Akbar Ali",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['product', 'account', 'mrp', 'stock', 'resource', 'mail', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'report/product_label_common.xml',
        'report/product_label_custom.xml',
        'report/report_menu.xml',
        'report/product_label_80*50.xml',
        'report/product_label_38*28.xml',
        'views/product_inherit_views.xml',
        'views/bom_inh_view.xml',
        'wizard/product_label_view.xml'
    ],
}
