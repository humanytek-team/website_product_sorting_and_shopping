# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields , models
from odoo.exceptions import Warning, ValidationError
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

Order = [
    ('asc','Ascending Order '),
    ('desc','Descending Order')
]


class Website(models.Model):
    _inherit = "website"

    def get_refine_action(self, keep, slug, brand=0, category=0, search=0, order=None,page=None):
        res = '/shop'
        if brand :
            if type(brand)==str:
                brand = self.env['wk.product.brand'].browse(int(brand))
            res+= ('/brand/'+slug(brand))
        elif category:
            res+= ('/category/'+slug(category))
        # ,page=page
        return keep(res,search=search,brand=0,category=0)

    def get_sorting_attribute(self, sorting, keep, slug, brand=0, category=0, search=0, page=None):
        result = []
        for sort in sorting:
            result.append((sort.name, "%s %s" % (sort.fields_name, sort.order)))
        return result


class WkSortAttribute(models.Model):
    _name = "wk.sort.attribute"
    _description = 'Sort Attributes'

    def _get_models(self):
        return [('product.template','Product Template')]
    name = fields.Char(
        string='Name',
        required=1
    )
    model_name = fields.Selection(
        selection=_get_models,
        string='Model',
        default = 'product.template',
        required=1
    )
    fields_name = fields.Char(
        string='Field',
        required=1,
        help='Enter the technical name field you want to use for Sorting'
    )
    by_default = fields.Boolean(
        string='Default',
        help='Use It For Default Sorting'
    )
    active = fields.Boolean(
        string='Active',
        help='Use It For Default Sorting',
        default=True
    )
    order = fields.Selection(
        selection=Order,
        default='asc',
        required=True
    )
    @api.multi
    @api.constrains('by_default','active')
    def _check_by_default(self):
        for rec in self:
            domain = [
                ('by_default','=',True),
                ('active','=',True),
            ]
            if len(self.search(domain))>1 :
                raise ValidationError("Only one attribute  can be set default at once !")


class WkWebsiteSorting(models.Model):
    _name = "wk.website.sorting"
    _description = 'website attribute sorting'

    @api.onchange('model_name')
    def compute_attribute_name(self):
        if self.model_name=='product.template':	self.name = 'Product Sorting'
        elif self.model_name=='wk.product.brand':self.name='Brand Sorting'
        else:self.name='Category Sorting'
    def _get_models(self):
        return [('product.template','Product Template')]

    name = fields.Char(
        string="Name" ,
        default = "Website Sorting Product"
    )
    model_name = fields.Selection(
        selection=_get_models,
        string='Model',
        default = 'product.template',
        required=1
    )
    wk_sort_attribute_ids = fields.Many2many(
        "wk.sort.attribute",
        "wk_website_sorting_sort_attribute_relation",
        "wk_website_sorting",
        "wk_sort_attribute",
        "Add Attribute"
    )


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"
    category_description = fields.Text(
        string = "Description (About this category)"
    )
    website_published =fields.Boolean(
        string='Available in the website',
        copy=False,
        default=True
    )
    website_size_x = fields.Integer(
        string='Size X',
        default=1
    )
    website_size_y = fields.Integer(
        string='Size Y',
        default=1
    )
    website_style_ids= fields.Many2many(
        'product.style',
        string='Styles'
    )


class WkProductBrand(models.Model):
    _inherit='wk.product.brand'
    website_published =fields.Boolean(
        string='Available in the website',
        copy=False,
        default=True
    )
    website_size_x = fields.Integer(
        string='Size X',
        default=1
    )
    website_size_y = fields.Integer(
        string='Size Y',
        default=1
        )
    website_style_ids= fields.Many2many(
        'product.style',
        string='Styles'
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def update_wk_sales_data(self):
        for record in self.mapped('product_variant_ids'):
            record.wk_sales_count = record.sales_count
            # record.wk_qty_available = record.qty_available
    wk_sales_count = fields.Integer(
        string='Sales Count',
        readonly=1
    )
    # wk_qty_available = fields.Integer(
    # 	string='Qty Available',
    # 	readonly=1
    # )
