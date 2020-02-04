# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
import werkzeug
import logging

from odoo import http
from odoo import SUPERUSER_ID
from odoo.exceptions import Warning
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL
_logger = logging.getLogger(__name__)
PPG = 20
PPR = 4

class WebsiteSale(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False,wk_brand=None, **post):
        response= super(WebsiteSale, self).shop(page, category, search,ppg,**post)
        if wk_brand:
            response.qcontext['wk_brand'] =wk_brand
        brand = request.httprequest.args.getlist('brand')
        if post and post.get('order'):
            products=response.qcontext['products']
            products.sudo().update_wk_sales_data()
            if  'wk_sales_count' in post.get('order'):
                sales_products = products.sorted('wk_sales_count')
                p_data = sales_products.mapped(lambda p:(p.id,p.name,p.wk_sales_count))
                sort_domain=[('fields_name','=','wk_sales_count'),('model_name','=','product.template')]
                sort=request.env['wk.sort.attribute'].search(sort_domain,limit=1)
                if sort.order!='desc':
                    sales_products = sales_products[::-1]
                response.qcontext['products'] = sales_products
        order = self._get_search_order(post)
        response.qcontext['order'] =order
        keep = QueryURL('/shop',
            category=category and int(category),
            brand=brand,
            # wk_brand = wk_brand and wk_brand.id,
            search=search,
            attrib= request.httprequest.args.getlist('attrib'),
            attrib_brand=request.httprequest.args.getlist('attrib_brand'),
            order=post.get('order')
        )
        response.qcontext['keep'] =keep

        return response

    def _get_search_order(self,post):
        default_order = super(WebsiteSale,self)._get_search_order(post)
        if post.get('order') and 'wk_sales_count' in post.get('order'):
            pass
        if not post.get('order'):
            sort_domain=[('model_name','=','product.template'),('by_default','=',True)]
            sort=request.env['wk.sort.attribute'].search(sort_domain,limit=1)
            if sort:
                default_order= '%s %s,%s'%(sort.fields_name,sort.order,default_order)
                request.params.update({'order': '%s %s' % (
                    sort.fields_name, sort.order)})
        else:
            return post.get('order')
        return  default_order

    ####################################################################################
    @http.route(['/product/brands','/product/brands/page/<int:page>',], type='http', auth='public', website=True)
    def wk_website_product_brands(self,page=0, search='', **post):
        cr, context, pool = (request.cr, request.context, request.registry)
        domain = []
        values={}
        if search:
            domain += ['|', '|', '|','|',
                           ('name', 'ilike', search),
                           ('description', 'ilike', search),
                           ('products.name', 'ilike', search),
                            ('products.description_sale', 'ilike', search),
                             ('products.description', 'ilike', search),
                           ]
            post['search'] =search
        url='/product/brands'

        keep = QueryURL('/product/brands', brand_id=[])
        count =   request.env['wk.product.brand'].search_count( domain)
        pager = request.website.pager(url=url, total=count, page=page, step=PPG, scope=7, url_args=post)
        brands = request.env['wk.product.brand'].search( domain,limit=PPG, offset=pager['offset'])
        values.update({
            'brand_rec': brands,
            'bins': TableCompute().process(brands),
            'rows': PPR,
            'keep': keep,
            'search': search,
            'pager': pager,
            'search_count': count})
        return request.render('website_product_sorting_and_shopping.wk_website_shop_by_product_brands', values)

    @http.route(['/brand/change_size'], type='json', auth="public")
    def brand_change_size(self, id, x, y):
        product_obj = request.registry.get('wk.product.brand')
        product = product_obj.browse(request.cr, request.uid, id, context=request.context)
        return product.write({'website_size_x': x, 'website_size_y': y})

    ##########################################################################################

    @http.route(['/product/categories','/product/categories/page/<int:page>'], type='http', auth='public', website=True)
    def wk_website_product_category(self, page=0, search='', **post):
        cr, context, pool = (request.cr, request.context, request.registry)
        domain = []
        values={}
        if search:
            domain += ['|',  ('name', 'ilike', search), ('category_description', 'ilike', search),]
            post['search'] =search
        url='/product/categories'

        keep = QueryURL('/product/categories', category_id=[])
        count =   request.env['product.public.category'].search_count( domain)
        pager = request.website.pager(url=url, total=count, page=page, step=PPG, scope=7, url_args=post)
        categories = request.env['product.public.category'].search( domain, limit=PPG, offset=pager['offset'])
        values.update ({'cat_rec': categories,
                'bins': TableCompute().process(categories),
                'rows': PPR,
                'keep': keep,
                'search': search,
                'pager':pager,
                'search_count': count})
        return request.render('website_product_sorting_and_shopping.wk_website_shop_by_product_categories', values)

    @http.route(['/category/change_size'], type='json', auth="public")
    def category_change_size(self, id, x, y):
        product_obj = request.registry.get('product.public.category')
        product = product_obj.browse(request.cr, request.uid, id, context=request.context)
        return product.write({'website_size_x': x, 'website_size_y': y})
