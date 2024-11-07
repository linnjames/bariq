# -*- coding: utf-8 -*-
{
    'name': "fbno_offline_pos",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale.assets': [
            'fbno_offline_pos/static/src/js/pos_offline.js',
            # 'fbno_offline_pos/static/src/js/product_screen.js'
        ],},
    'images': ['static/description/icon.png'],

}
