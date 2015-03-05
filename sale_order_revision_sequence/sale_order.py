# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
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

import logging

_logger = logging.getLogger(__name__)
from openerp.osv import orm
from openerp import api

class SaleOrder(orm.Model):
    """Custom sequence for the revision."""
    _inherit = 'sale.order'

    def create_revision(self, cr, uid, id_, default=None, context=None):
        """Overcharge of the method to set a custom name to revisions.

        :return: View descriptor
        """
        # Getting the return value of create_revision to
        # find back the newly created sale.order which is in the view
        # descriptor.
        ret = super(SaleOrder, self).create_revision(
            cr, uid, id_, default=default, context=context
        )
        revision = self.browse(cr, uid, ret['res_id'])

        # Updating the revision with the new name.
        revision.write(
            {
                'name': '{}-{}'.format(
                    revision.revision_original_id.name,
                    # The index has to start at 0 for
                    # revision_number_to_number but number_revision starts
                    # at 1.
                    revision_number_to_letter(revision.number_revisions - 1)
                )
            }
        )
        # No need to update the view descriptor as it uses the id of the
        # sale.order directly.
        return ret


def to_letters(num):
    """Transform a number to the letter with the index as num in the
    alphabet.

    :param num: integer
    :return: iterator in the form of [first_letter, [second_letter, [...]]]
    """
    # A is used as the reference. We then are looking for its code to
    # work with.
    letter_a = ord('A')
    num_letters = 26

    while num >= num_letters:

        yield chr((num % num_letters) + letter_a)
        num = num // num_letters - 1

    yield chr(num + letter_a)


def revision_number_to_letter(number_revision):
    """Transform a number into a set of letter following the sequence:
        - 0 = A
        - 1 = B
        - 25 = Z
        - 26 = AA
        - 27 = AB
        - etc.

    :param number_revision: integer
    :return: string
    """
    return "".join(list(to_letters(number_revision))[::-1])
