# -*- coding: utf-8 -*-
{
    'name': 'mrp production',
    'summary': '''
        Production Bioest
    ''',
    'description': '''
        - Mrp production in Bioest
    ''',
    'author': '1-800CLOUD',
    'website': 'http://www.1-800cloud.com',
    'category': 'Manufacturing/Manufacturing',
    'license': 'LGPL-3',
    'version': '15.0.0.0.4',
    'depends': [
        'base',
        'mrp',
        'product'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template_views.xml',
        # 'views/templates.xml',
    ],
}
