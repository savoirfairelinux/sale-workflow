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
from openerp import models, fields, api, _


class product_selection(models.TransientModel):

    _name = 'product.selection'

    partner_id = fields.Many2one('res.partner', string="Partner")
    pricelist_id = fields.Many2one('product.pricelist', string="Pricelist")

    brand_id = fields.Many2one('fleet.vehicle.model.brand', string='Brand')
    model_id = fields.Many2one('fleet.vehicle.model', string='Model')
    year = fields.Char('Year', size=12)
    cylinder_id = fields.Many2one('fleet.vehicle.cylinder', string='Cylinders')
    litre_id = fields.Many2one('fleet.vehicle.litre', string='Litre')

    engine_code_id = fields.Many2one(
        'fleet.vehicle.enginecode',
        string='Engine Code'
    )
    default_code = fields.Char(string='Internal Reference')

    spec_ids = fields.Many2many(
        'fleet.vehicle.spec',
        string='Specifications')

    product_selection_line_ids = fields.One2many(
        'product.selection.line',
        'product_selection_id',
        string='Search Result'
    )

    @api.multi
    def update(self):
        self.write({'product_selection_line_ids': [(5, 0, 0)]})

        fleet_spec_ids = []

        spec_query = []

        if self.model_id:
            spec_query.append(('model_id', '=', self.model_id.id))

        if self.brand_id:
            spec_query.append(('brand_id', '=', self.brand_id.id))

        if self.year:
            # either between year_start and year_end or equal to one if the
            # other is not filled in
            spec_query += [
                '|',
                '&',
                ('year_start', '<=', self.year),
                ('year_end', '>=', self.year),
                '|',
                '&',
                ('year_start', '=', self.year),
                ('year_end', '=', False),
                '&',
                ('year_start', '=', False),
                ('year_end', '=', self.year),
            ]

        if self.cylinder_id:
            spec_query.append(('cylinder_id', '=', self.cylinder_id.id))

        if self.litre_id:
            spec_query.append(('litre_id', '=', self.litre_id.id))

        if self.engine_code_id:
            spec_query.append(
                ('engine_code_id', 'in', [self.engine_code_id.id, False]))
        else:
            spec_query.append(
                ('engine_code_id', '=', False))

        fleet_spec_ids += {
            spec.id for spec
            in self.env['product.fleet.spec'].search(spec_query)
            if (spec.spec_ids | spec.product_id.global_spec_ids)
            & self.spec_ids == self.spec_ids
        }

        products = self.env['product.product'].search(
            [('product_fleet_spec_ids.id', 'in', fleet_spec_ids)])

        if products:
            vals = {
                'product_selection_line_ids': [
                    (0, 0, {'product_id': p}) for p in products.ids]
            }
            self.write(vals)

        return {
            'name': _('Select products from the result list'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.selection',
            'res_id': self.ids[0],
            'target': 'new',
            'context': self.env.context,
        }

    @api.one
    def confirm(self):
        vals = [
            (0, 0, {
                'product_id': line.product_id.id,
                'price_unit': line.product_id.list_price,
            })
            for line in self.product_selection_line_ids
            if line.is_selected
        ]
        so = self.env['sale.order'].browse(self._context.get('active_id'))
        so.write({'order_line': vals})

        return {'type': 'ir.actions.act_window_close'}
