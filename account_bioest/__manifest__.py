# -*- coding: utf-8 -*-
{
    'name': 'Account Bioest',
    'summary': '''
        Account Bioest
    ''',
    'description': '''
        - Cuenta de gastos en categoría de producto permite seleccionar cuentas tipo gastos y otros.
    ''',
    'author': '1-800CLOUD',
    'website': 'http://www.1-800cloud.com',
    'category': 'Accounting/Accounting',
    'license': 'LGPL-3',
    'version': '15.0.0.0.9',
    'depends': [
        'account_baseline',
        'purchase',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_category_views.xml',
        # 'views/templates.xml',
    ],
}
