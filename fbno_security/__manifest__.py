# -*- coding: utf-8 -*-
{
    'name': "Module access",
    'summary': """
        Visibillity of modules""",
    'description': """
        Set Visibillity of modules
    """,
    'author': "Akbar",
    'website': "",
    'category': 'Security',
    'version': '13.1',
    'depends': ['base', 'account', 'hr', 'stock', 'contacts', 'purchase', 'hr_holidays', 'calendar', 'mail','hr_payroll_community'],
    'data': [
        'security/security.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
