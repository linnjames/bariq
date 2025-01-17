# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Multiple Branch in Odoo',
    'version': '1.0',
    'category': 'Sale',
    'summary': 'multiple shop on Point of Sale branch shops pos multi branch pos branch unit pos screens point of sales Multiple branch pos multiple unit point of sales multiple stores pos multi store pos branch on pos multiple branch pos multi unit pos multi store',
    "description": """
    odoo Multiple Unit operation management for single company Multiple Branch management for single company 
    odoo multiple operation for single company Branch for POS  point of sales multiple branch branch in pos branch on point of sales
    odoo branching in POS multi company pos odoo point of sales Unit Operation For single company
    odoo Branch Operation for POS multiple branch on POS multiple unit operation for POS branch on POS session
    odoo Branch on POS receipt different unit on POS
    odoo POS Unit Operation For single company
    oodoo POS Multiple operating unit management for single company Multiple pos operation management for single company POS multiple operation for single company.
    odoo multiple Branch for POS multiple operating unit for POS odoo
    odoo multiple unit on POS multiple unit operation for POS branch on POS session Branch on POS receipt
    odoo different unit on POS POS Unit Operation For single company odoo operating unit on POS session operating unit on POS receipt
    odoo different unit operation on POS POS multiple Unit Operation For single company
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    "price": 39,
    "currency": 'EUR',
    'depends': ['base'],
    'data': [
                'security/branch_security.xml',
                'security/ir.model.access.csv',
                'views/res_branch_views.xml'
            ],
    'qweb': [
            ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
