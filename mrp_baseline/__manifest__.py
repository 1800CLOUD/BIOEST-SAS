# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Baseline",
    'summary': "Manufacturing Orders & BOMs",
    'description': "Manufacturing Orders & BOMs",
    'author': '1-800CLOUD',
    'website': 'https://www.1-800cloud.com',
    'category': 'Manufacturing/Manufacturing',
    'version': '15.0.0.0.4',
    'depends': [
        'account_analytic',
        'mrp_account',
        'mrp_account_enterprise'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_workcenter_views.xml',
        'views/mrp_workorder_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/production_account_close_views.xml',
        'reports/mrp_report_2_views.xml',
    ],
    'license': 'LGPL-3',
}
