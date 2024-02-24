# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	'name': "Advance Project Stage Organiser/Set Default Project Stages",
	'version': "15.0.0.0",
	'category': "Project",
	'summary': "Default Project Stages set stages on project stage Organiser Assign default stages on project stage sharing share stage on project assign stages on project sharing on stages share stage on multiple project sharing advance project stage share task stage",
	'description':	"""
             In default odoo we don't have functionality to select and use same stages on multiple project. This odoo app helps user to set only selected stages for project, user can select multiple stages and only this selected stages will appear to related project, if user removes stages from project, project will also removed from stages, User can also share same stages on multiple projects. 
					""",
	'author': "BrowseInfo",
	"website" : "https://www.browseinfo.in",
	"price": 15,
	"currency": 'EUR',
	'depends': ['base', 'project'],
	'data': [
		'views/project_view.xml'
	],
	'installable': True,
	'auto_install': False,
	'application': False,
	"live_test_url":'https://youtu.be/8lZA2wuIWsc',
	"images":['static/description/Banner.png'],
	'license': 'OPL-1',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
