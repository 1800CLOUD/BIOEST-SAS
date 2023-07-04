# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'


    def write(self, vals):
        if vals.get('quota_limit_initial') and not self.env.user.has_group('account_voucher.group_block_credit_limit'):
            raise UserError(_("Lo sentimos. No esta autorizado para modificar el campo 'Cuota de límite inicial' Contacte a Soporte si cree que deberia tener el permiso"))

        return super(ResPartner, self).write(vals)