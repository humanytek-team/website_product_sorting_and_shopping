# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Website Product Sortby & Shopby",
  "summary"              :  "The module provides the customers to sort out the product according to date, brands, category, etc.",
  "category"             :  "Website",
  "version"              :  "0.3",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Website-Product-SortBy-ShopBy.html",
  "description"          :  """Odoo Website Product Sortby & Shopby
Odoo website product filters
Filter products using brands in Odoo
Add product brands in odoo
Filter products with brands
Add product filter to Odoo website
Odoo website product filters
Odoo sort by date
Odoo shop by brand
Odoo website sort products
Odoo sort products by category
Odoo sort by size

  """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_product_sorting_and_shopping",
  "depends"              :  ['website_product_brands'],
  "data"                 :  [
                             'views/template.xml',
                             'views/brands_template.xml',
                             'views/category_template.xml',
                             'views/sort_by_shop_by.xml',
                             'security/ir.model.access.csv',
                             'data/data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  24,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}