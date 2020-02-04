================================================
``website_product_sorting_and_shopping`` changelog
================================================

*****
[version:0.2]  Date : 12-03-2018
*[Update]
    -Update templates as per new update in odoo view 

        template(id="inherit_website_sale_products_refine_template" ,inherit_id="website_sale.products")
        template(id="inherit_website_sale_products_shop_by_template" ,inherit_id="website_sale.products")
        template(id="inherit_website_sale_products_brand_category_template" ,inherit_id="website_sale.products")
	Ref:https://github.com/odoo/odoo/blob/11.0/addons/website_sale/views/templates.xml#L173
       -<xpath expr="//div[@class='container oe_website_sale']/div[@class='products_pager']" position="after">
       +<xpath expr="//div[contains(@t-attf-class,'container oe_website_sale')]/div[@class='products_pager']" position="after">


*****

