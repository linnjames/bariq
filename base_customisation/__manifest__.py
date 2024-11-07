
{
    'name': 'Base Customisation',
    'version': '1.0',
    'category': 'base',
    'description': """
        Base Customisation
    """,
    'depends': ['fbno_product_arabic', 'sale_management', 'sale_stock', 'pos_branch', 'web', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/base_security.xml',
        'data/ir_sequence_data.xml',
        'views/account_move_inh_views.xml',
        'views/kitchen_views.xml',
        'views/kitchen_chef_views.xml',
        'views/sale_order_views.xml',
        'wizard/kitchen_order_process_views.xml',
        'wizard/ko_internal_transfer_views.xml',
        'views/stock_views.xml',
        'report/account_report.xml',
        'report/kitchen_print_template.xml',
        'report/vat_report_invoice.xml',
        'wizard/sale_make_invoice_advance_views.xml',
        'wizard/order_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'applications': True
}
