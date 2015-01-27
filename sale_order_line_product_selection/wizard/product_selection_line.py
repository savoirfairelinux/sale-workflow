# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Savoir-faire Linux (<www.savoirfairelinux.com>).
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
from openerp import models, fields, api

class product_selection_line(models.TransientModel):

    _name = 'product.selection.line'

    @api.one
    @api.depends('product_id.list_price', 'pricelist_id')
    def _list_price(self):
        pricelist = self.env['product.pricelist'].browse(
            [self.product_selection_id.pricelist_id.id])
        self.list_price = pricelist.price_get(
            self.product_id.id, 1.0,
            partner=self.product_selection_id.partner_id.id)[pricelist.id]

    product_selection_id = fields.Many2one('product.selection')
    is_selected = fields.Boolean('Selected')
    product_id = fields.Many2one('product.product', string='Product')
    pricelist_id = fields.Many2one('product.pricelist')
    default_code = fields.Char(related='product_id.default_code', store=True)
    standard_price = fields.Float(
        related='product_id.standard_price', store=True)
    list_price = fields.Float(
        compute=_list_price, string="Sale Price")
