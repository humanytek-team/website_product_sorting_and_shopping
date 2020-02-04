odoo.define('wk_product_brand.editor', function (require) {
"use strict";
     require('website_sale.editor');
    
    var ajax = require('web.ajax');
    var core = require('web.core');
    var options = require('web_editor.snippets.options');

    var _t = core._t;
    options.registry.website_sale = options.registry.website_sale.extend({
        start: function () {     
           var self = this;      
            this.brand_tmpl_id = parseInt(this.$target.find('[data-oe-model="wk.product.brand"]').data('oe-id'));
            this.category_tmpl_id = parseInt(this.$target.find('[data-oe-model="product.public.category"]').data('oe-id'));     
            this._super();
        },
        bind_resize: function () {
        var self = this;
        this.$el.on('mouseenter', 'ul[name="size"] table', function (event) {
            $(event.currentTarget).addClass("oe_hover");
        });
        this.$el.on('mouseleave', 'ul[name="size"] table', function (event) {
            $(event.currentTarget).removeClass("oe_hover");
        });
        this.$el.on('mouseover', 'ul[name="size"] td', function (event) {
            var $td = $(event.currentTarget);
            var $table = $td.closest("table");
            var x = $td.index()+1;
            var y = $td.parent().index()+1;

            var tr = [];
            for (var yi=0; yi<y; yi++) tr.push("tr:eq("+yi+")");
            var $select_tr = $table.find(tr.join(","));
            var td = [];
            for (var xi=0; xi<x; xi++) td.push("td:eq("+xi+")");
            var $select_td = $select_tr.find(td.join(","));

            $table.find("td").removeClass("select");
            $select_td.addClass("select");
        });
        // this.$el.on('click', 'ul[name="size"] td', function (event) {
        //     var $td = $(event.currentTarget);
        //     var x = $td.index()+1;
        //     var y = $td.parent().index()+1;
        //     ajax.jsonRpc('/shop/change_size', 'call', {'id': self.product_tmpl_id, 'x': x, 'y': y})
        //         .then(self.reload);
        // });
          this.$el.on('click', 'ul[name="size"] td', function (event) {

                var $td = $(event.currentTarget);
                var x = $td.index()+1;
                var y = $td.parent().index()+1;
                 if(self.product_tmpl_id){               
                        ajax.jsonRpc('/shop/change_size', 'call', {'id': self.product_tmpl_id, 'x': x, 'y': y})
                    .then(self.reload);
                }   
                 if(self.brand_tmpl_id){
                        ajax.jsonRpc('/brand/change_size', 'call', {'id': self.brand_tmpl_id, 'x': x, 'y': y})
                    .then(self.reload);
                }
                 if(self.category_tmpl_id){
                        ajax.jsonRpc('/category/change_size', 'call', {'id': self.category_tmpl_id, 'x': x, 'y': y})
                    .then(self.reload);

                }        
            });  
    },   
    });



});