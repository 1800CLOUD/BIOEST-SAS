# -*- coding: utf-8 -*-
{
    'name': 'Purchase Report',
    'summary': '''
        reporte de compras
    ''',
    'description': '''
        - 
    ''',
    'author': '1-800CLOUD',
    'website': 'http://www.1-800cloud.com',
    'category': 'Purchase/Purchase',
    'license': 'LGPL-3',
    'version': '15.0.0.0.7',
    'depends': [
        'base_setup',
        'purchase',
        'account',
    ],
    'data': [
         'security/ir.model.access.csv',
         'reports/purchase_report.xml',
         'views/menuitems.xml',
    ],
}
