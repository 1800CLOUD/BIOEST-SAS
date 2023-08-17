# -*- coding: utf-8 -*-
{
    'name': 'Stock Bioest',
    'summary': '''
        Stock Bioest
    ''',
    'description': '''
        - Modulo extendido para modificar, agregar funcionalidades, campos del modulo stock.
    ''',
    'author': '1-800CLOUD',
    'website': 'http://www.1-800cloud.com',
    'category': 'Inventory/Inventory',
    'license': 'LGPL-3',
    'version': '15.0.0.0.6',
    'depends': [
        'stock',
        'stock_report',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        #'views/stock_picking_views.xml',
        'views/stock_inventory_views.xml',
        'views/view_stock_move.xml',
        'views/template_stock_move.xml',
    ],
}
