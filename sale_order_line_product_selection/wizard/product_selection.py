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

    engine_code = fields.Char(string='Engine Code', size=154)
    default_code = fields.Char(string='Internal Reference')

    a_t = fields.Boolean('A/T')
    m_t = fields.Boolean('M/T')

    direct_fit_radiator_side_precat_left_side = fields.Boolean(
        'Direct fit radiator side precat LEFT side')
    direct_fit_radiator_side_precat_right_side = fields.Boolean(
        'Direct fit radiator side precat RIGHT side')

    dohc = fields.Boolean('DOHC')
    shoc = fields.Boolean('SHOC')

    converter_wmanifold = fields.Boolean('Converter W/Manifold')

    super_duty = fields.Boolean('Super Duty')
    b2x4 = fields.Boolean('2X4')
    b4x4 = fields.Boolean('4X4')

    awd = fields.Boolean('AWD')
    fwd = fields.Boolean('FWD')

    b2doors = fields.Boolean('2 doors')
    b4doors = fields.Boolean('4 doors')

    emission_federal = fields.Boolean('Emission Federal')
    emission_californien = fields.Boolean('Emission Californien')

    product_selection_line_ids = fields.One2many(
        'product.selection.line',
        'product_selection_id',
        string='Search Result'
    )

    @api.multi
    def update(self):
        self.write({'product_selection_line_ids': [(5, 0, 0)]})

        query = []
        if (self.model_id or self.brand_id or self.year or self.cylinder_id or
                self.litre_id):

            query0 = []
            if self.model_id:
                query0.append(('model_id', '=', self.model_id.id))

            if self.brand_id:
                query0.append(('brand_id', '=', self.brand_id.id))

            if self.year:
                # either between year_start and year_end or equal to one if the
                # other is not filled in
                query0 += [
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
                query0.append(('cylinder_id', '=', self.cylinder_id.id))

            if self.litre_id:
                query0.append(('litre_id', '=', self.litre_id.id))

            stage_1_ids = self.env['product.fleet.spec'].search(query0)
            query.append(
                ('product_fleet_spec_ids.id', 'in', stage_1_ids.ids))

        if self.engine_code:
            query.append(('engine_code.name', 'ilike', self.engine_code))

        if self.default_code:
            query.append(('default_code', 'ilike', self.default_code))

        if self.a_t:
            query.append(('a_t', '=', self.a_t))

        if self.m_t:
            query.append(('m_t', '=', self.m_t))

        if (self.direct_fit_radiator_side_precat_left_side or
                self.direct_fit_radiator_side_precat_right_side):
            query.append(
                ('direct_fit_radiator_side_precat_right_side', '=',
                 self.direct_fit_radiator_side_precat_right_side)
            )
            query.append((
                'direct_fit_radiator_side_precat_right_side', '=',
                self.direct_fit_radiator_side_precat_right_side)
            )

        if self.dohc:
            query.append(('dohc', '=', self.dohc))
        if self.shoc:
            query.append(('shoc', '=', self.shoc))

        if self.converter_wmanifold:
            query.append(
                ('converter_wmanifold', '=', self.converter_wmanifold))

        if self.super_duty:
            query.append(('super_duty', '=', self.super_duty))
        if self.b2x4:
            query.append(('b2x4', '=', self.b2x4))
        if self.b4x4:
            query.append(('b4x4', '=', self.b4x4))

        if self.awd:
            query.append(('awd', '=', self.awd))
        if self.fwd:
            query.append(('fwd', '=', self.fwd))

        if self.b2doors:
            query.append(('b2doors', '=', self.b2doors))
        if self.b4doors:
            query.append(('b4doors', '=', self.b4doors))

        if self.emission_federal:
            query.append(('emission_federal', '=', self.emission_federal))
        if self.emission_californien:
            query.append(
                ('emission_californien', '=', self.emission_californien)
            )

        product_ids = self.env['product.product'].search(query)

        if product_ids:
            vals = {
                'product_selection_line_ids': [
                    (0, 0, {'product_id': p}) for p in product_ids.ids]
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
