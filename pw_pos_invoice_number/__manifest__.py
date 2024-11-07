# -*- coding: utf-8 -*-
{
    "name": "Invoice Number on POS Receipt | POS Invoice on Receipt",
    'version': '15.0',
    'author': 'Preway IT Solutions',
    'category': 'Point of Sale',
    'depends': ['point_of_sale','l10n_sa_pos',],
    'summary': 'This module helps you to show invoice number on pos receipt | Invoice on Receipt | Invoive Number on POS Receipt | POS Invoice Receipt | Invoice number in pos ticket',
    'description': """
- Odoo Invoice number on pos receipt
    """,
    'data': [],
    'assets': {
        'point_of_sale.assets': [
                    'pw_pos_invoice_number/static/src/js/pos_session.js',
                    'pw_pos_invoice_number/static/src/css/receipt.css',
        ],
        'web.assets_qweb': [
            'pw_pos_invoice_number/static/src/xml/pos.xml',
            'pw_pos_invoice_number/static/src/xml/custom_res.xml'
        ],

    },
    'price': 5.0,
    'currency': "EUR",
    'application': True,
    'installable': True,
    "license": "LGPL-3",
    'live_test_url': 'https://youtu.be/svxHGEmeP58',
    "images":["static/description/Banner.png"],
}

