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

    product_selection_line_ids = fields.One2many(
        'product.selection.line',
        'product_selection_id',
        string='Search Result'
    )

    @api.multi
    def update(self):
        self.write({'product_selection_line_ids': [(5, 0, 0)]})

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

        fleet_spec_ids = self.env['product.fleet.spec'].search(spec_query).ids

        products = self.env['product.product'].search(
            [('product_fleet_spec_ids.id', 'in', fleet_spec_ids)])

        product_dict = {
            product.id: product.product_fleet_spec_ids.filtered(
                lambda spec: spec.id in fleet_spec_ids)
            for product in products
        }

        selection_lines = []
        for product_id in product_dict:
            for spec in product_dict[product_id]:
                selection_lines.append((product_id, spec.id))

        if product_dict:
            self.write({
                'product_selection_line_ids': [
                    (0, 0, {
                        'product_id': line[0],
                        'spec_id': line[1],
                    }) for line in selection_lines]
            })

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
        self._check_product_selected_once()
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

    @api.one
    def _check_product_selected_once(self):
        """
        Check that every product is selected maximum one time
        Otherwise, unselected redundant
        """
        product_ids = set()
        unselect_line_ids = []
        selected_lines = self.product_selection_line_ids.filtered(
            lambda line: line.is_selected)

        for line in selected_lines:
            if line.product_id.id in product_ids:
                unselect_line_ids.append(line.id)
            else:
                product_ids.add(line.product_id.id)

        self.env['product.selection.line'].browse(unselect_line_ids).write(
            {'is_selected': False})
