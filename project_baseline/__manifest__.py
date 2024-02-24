# -*- coding: utf-8 -*-
{
    'name': 'Project Baseline',
    'summary': '''
        - Solución Baseline para proyectos.
    ''',
    'description': '''
        - Pestaña de ingresos y gastos en las tareas de proyecto (Política).
    ''',
    'author': '1-800CLOUD',
    'website': 'https://www.1-800cloud.com',
    'license': 'LGPL-3',
    'category': 'Services/Project',
    'version': '15.0.0.0.2',
    'depends': [
        'project', 
        'sale', 
        'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
}
