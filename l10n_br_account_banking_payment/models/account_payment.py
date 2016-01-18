# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 - KMEE INFORMATICA LTDA (<http://kmee.com.br>).
#              Luis Felipe Miléo - mileo@kmee.com.br
#
#    All other contributions are (C) by their respective contributors
#
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, exceptions, workflow, _



class PaymentOrder(models.Model):
    _inherit = 'payment.order'

    mode_type = fields.Many2one('payment.mode.type', related='mode.type',
                                string='Payment Type')
    total = fields.Float(compute='_compute_total', store=True)

    # TODO: Implementar total de juros e outras despesas acessórias.
    @api.depends('line_ids', 'line_ids.amount')
    @api.one
    def _compute_total(self):
        self.total = sum(self.mapped('line_ids.amount') or [0.0])


class PaymentLine(models.Model):
    _inherit = 'payment.line'

    def _get_info_partner(self,cr, uid, partner_record, context=None):
        if not partner_record:
            return False
        st = partner_record.street or ''
        n = partner_record.number or ''
        st1 = partner_record.street2 or ''
        zip = partner_record.zip or ''
        city = partner_record.l10n_br_city_id.name or  ''
        uf = partner_record.state_id.code or  ''
        zip_city = city + '-' + uf + '\n' + zip
        cntry = partner_record.country_id and partner_record.country_id.name or ''
        cnpj = partner_record.cnpj_cpf or ''
        return partner_record.legal_name + "\n" + cnpj + "\n" + st + ", " + n + "  " + st1 + "\n" + zip_city + "\n" +cntry

    linha_digitavel = fields.Char(string=u"Linha Digitável")
    #
    # # TODO: Implementar total de juros e outras despesas acessórias.
    # @api.depends('line_ids', 'line_ids.amount')
    # @api.one
    # def _compute_total(self):
    #     self.total = sum(self.mapped('line_ids.amount') or [0.0])


