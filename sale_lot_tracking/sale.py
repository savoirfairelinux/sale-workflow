# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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

from openerp.osv import orm, fields
import logging

class sale_order(orm.Model):

    _inherit = 'sale.order'
    _logger = logging.Logger(__name__)

    def _create_pickings(self, cr, uid, order, context=None):

        sale_order_lines = order.order_line
        stock_move_obj = self.pool.get('stock.move')
        stock_move_line_ids = stock_move_obj.search(cr, uid, [('origin', '=', order.name)])
        stock_move_lines = stock_move_obj.browse(cr, uid, stock_move_line_ids)



        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        journal_obj = self.pool.get('account.journal')
        journal_ids = journal_obj.search(cr, uid, [('type', '=', 'purchase'),
                                                   ('company_id', '=', order.company_id.id)],
                                         limit=1)

        total_pallets = 0.0

        for so_line in order.order_line:
            total_pallets += so_line.nb_pallets


        for order_cost in order.landed_cost_line_ids:
            vals_inv = {
                'partner_id': order_cost.partner_id.id,
                'currency_id': order_cost.currency_id.id or order.company_id.currency_id.id,
                'account_id': order_cost.partner_id.property_account_payable.id,
                'type': 'in_invoice',
                'origin': order.name,
                'fiscal_position':  (order.partner_id.property_account_position and
                                     order.partner_id.property_account_position.id or
                                     False),
                'company_id': order.company_id.id,
                'journal_id': len(journal_ids) and journal_ids[0] or False
            }

            inv_id = invoice_obj.create(cr, uid, vals_inv, context=None)

            for sale_order_line in sale_order_lines:

                factor = 0.0

                if order_cost.price_type == 'per_unit':
                    factor = float(sale_order_line.product_uom_qty) / sale_order_line.order_id.quantity_total
                    
                elif order_cost.price_type == 'value':
                    factor = float(sale_order_line.price_subtotal) / sale_order_line.order_id.amount_total

                elif order_cost.price_type == 'per_pallet':
                    #FIXME: total_pallets
                    factor = float(sale_order_line.nb_pallets) / total_pallets

                else:
                    raise ValueError('Unknown price type (neither "per_unit", "value" nor "per_pallet")')

                amount = order_cost.amount * factor                

                # trouver le compte analytique
                # FIXME: ne pas uniquement regarder la quantité



                # répercuter sur l'ensemble des lots 

                matching_lines = [
                    line
                    for line in stock_move_lines
                    if line.product_id.id == sale_order_line.product_id.id
                ]

                import pdb; pdb.set_trace()

                for line in matching_lines:
                    total_product = sum(l.product_qty for l in matching_lines)
                    amount_line = amount * (line.product_qty / total_product)
                    
                    # fractionner les coûts

                    vals_line = {
                        'product_id': order_cost.product_id.id,
                        'name': order_cost.product_id.name,
                        'account_id': self._get_product_account_expense_id(order_cost.product_id),
                        'partner_id': order_cost.partner_id.id,
                        'invoice_id': inv_id,
                        'price_unit': amount,
                        'account_analytic_id': line.prodlot_id.account_analytic_id.id,
                        'invoice_line_tax_id': [(6, 0, [x.id for x in order_cost.product_id.supplier_taxes_id])]
                    }

                    invoice_line_obj.create(cr, uid, vals_line, context=None)






