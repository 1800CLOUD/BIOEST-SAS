# -*- coding: utf-8 -*-
{
    'name': 'Stock Bioest',
    'summary': '''
        Stock Bioest
    ''',
    'description': '''
        - Quitar botones ANULAR RESERVA y COMPROBAR DISPONIBILIDAD en vista lista de transferencias.
    ''',
    'author': '1-800CLOUD',
    'website': 'http://www.1-800cloud.com',
    'category': 'Inventory/Inventory',
    'license': 'LGPL-3',
    'version': '15.0.0.0.2',
    'depends': [
        'stock'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
    ],
}
