# -*- coding: utf-8 -*-
{
    'name': 'Helpdesk Baseline',
    'summary': '''
        - Income and expense tab.
    ''',
    'description': '''
        - Income and expense tab.
    ''',
    'author': '1-800CLOUD',
    'website': 'https://www.1-800cloud.com',
    'license': 'LGPL-3',
    'category': 'Services/Helpdesk',
    'version': '15.0.0.0.4',
    'depends': [
        'helpdesk', 
        'sale', 
        'purchase',
        'helpdesk_timesheet'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_ticket_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
}
