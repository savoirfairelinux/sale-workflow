Sale Order Revision Sequence
============================

Customization of the name of revision of sale orders.

With taking in consideration the sale.order SO01:
* the first revision will be named SO01-A instead of SO02
* the second revision will be named SO01-B instead of SO03
* the twenty seventh will be name SO01-AA instead of SO27
* etc.

It is assumed the process will have eaten the names.

The sequence of letters is following the pattern, A-Z, then AA-AZ, BA-BZ etc.

The name is based on the original sale.order, meaning the revision of SO01-A
will be SO01-B and not SO01-A-A.

Installation
============

No installation steps required other than installing the module itself.

Configuration
=============

No configuration required.


Credits
=======

Contributors
------------

* Jordi Riera <jordi.riera@savoirfairelinux.com>
* Bruno JOLIVEAU <bruno.joliveau@savoirfairelinux.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

More information
----------------

Module developed and tested with Odoo version 8.0.

For questions, please contact our support services
<support@savoirfairelinux.com>
