# -*- coding: utf-8 -*-

{
    'name': 'Translation Helper',
    'version': '15.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """Translate the product name to arabic using 'googletrans'.""",
    'description': """This module will help you to translate product name to arabic.""",
    'depends': ['base','stock'],
    'external_dependencies': {'python': ['googletrans']},
    'data': [
        'views/translation.xml',
            ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
