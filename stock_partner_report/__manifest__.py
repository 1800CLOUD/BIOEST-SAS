# -*- coding: utf-8 -*-
{
    'name': 'Reporte Inventario',
    'summary': '''
        Reporte de inventario con costos por propietario.
    ''',
    'description': '''
        - Reporte de inventario con costos por propietario
    ''',
    'author': 'My Company',
    'website': 'http://www.yourcompany.com',
    'category': 'Inventory/Inventory',
    'version': '15.0.0.0.2',
    'license': 'LGPL-3',
    'depends': [
        'stock_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_cost_owner_views.xml',
        'views/stock_quant_views.xml',
    ],
}
