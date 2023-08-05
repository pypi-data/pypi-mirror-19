# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from shop.rest.renderers import CMSPageRenderer
from shop.views.catalog import AddToCartView as AddToCartViewBase
from shop.views.catalog import ProductListView as BaseProductListView
from shop.views.catalog import ProductRetrieveView

from shopit.models.cart import Cart, CartItem
from shopit.models.product import Attribute
from shopit.serializers import (AddToCartSerializer, CartItemSerializer, ProductDetailSerializer,
                                ProductSummarySerializer, WatchItemSerializer)

CATEGORIES_VAR = 'c'
BRANDS_VAR = 'b'
MANUFACTURERS_VAR = 'm'
FLAGS_VAR = 'f'
PRICE_FROM_VAR = 'pf'
PRICE_TO_VAR = 'pt'
SORT_VAR = 's'


class ProductListView(BaseProductListView):
    serializer_class = ProductSummarySerializer
    renderer_classes = [CMSPageRenderer] + api_settings.DEFAULT_RENDERER_CLASSES

    def get_queryset(self):
        return super(ProductListView, self).get_queryset().active().top_level()

    def filter_queryset(self, queryset):
        queryset = super(ProductListView, self).filter_queryset(queryset)

        categories = list(filter(None, self.request.GET.get(CATEGORIES_VAR, '').split(','))) or None
        brands = list(filter(None, self.request.GET.get(BRANDS_VAR, '').split(','))) or None
        manufacturers = list(filter(None, self.request.GET.get(MANUFACTURERS_VAR, '').split(','))) or None
        queryset = queryset.filter_categorization(categories, brands, manufacturers)

        flags = list(filter(None, self.request.GET.get(FLAGS_VAR, '').split(','))) or None
        queryset = queryset.filter_flags(flags)

        price_from = self.request.GET.get(PRICE_FROM_VAR, None)
        price_to = self.request.GET.get(PRICE_TO_VAR, None)
        queryset = queryset.filter_price(price_from, price_to)

        attrs = Attribute.objects.active()
        attr_codes = attrs.values_list('code', flat=True)
        attr_filters = [(x[0], x[1]) for x in self.request.GET.items() if x[0] in attr_codes]

        # Remove null values from attributes that are not nullable.
        for f in [x for x in attr_filters if not x[1]]:
            if not attrs.get(code=f[0]).nullable:
                attr_filters.remove(f)

        queryset = queryset.filter_attributes(attr_filters)

        sort = self.request.GET.get(SORT_VAR, None)
        sort_map = {
            'name': 'translations__name',
            '-name': '-translations__name',
            'price': '_unit_price',
            '-price': '-_unit_price',
        }
        if sort in sort_map:
            queryset = queryset.order_by(sort_map[sort])

        return queryset

    def get_template_names(self):
        return ['shopit/catalog/product_list.html']

    def get_renderer_context(self):
        context = super(ProductListView, self).get_renderer_context()
        if context['request'].accepted_renderer.format == 'html':
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                context.update(self.paginator.get_html_context())
            context['product_list'] = page or queryset
        return context


class ProductDetailView(ProductRetrieveView):
    serializer_class = ProductDetailSerializer
    renderer_classes = [CMSPageRenderer] + api_settings.DEFAULT_RENDERER_CLASSES
    lookup_field = 'translations__slug'

    def get(self, request, *args, **kwargs):
        response = super(ProductDetailView, self).get(request, *args, **kwargs)
        product_id = self.get_object().pk
        menu = request.toolbar.get_or_create_menu('shopit-menu', _('Shopit'))
        menu.add_break()
        menu.add_modal_item(_('Edit Product'), url=reverse('admin:shopit_product_change', args=[product_id]))
        menu.add_sideframe_item(_('Delete Product'), url=reverse('admin:shopit_product_delete', args=[product_id]))
        return response

    def get_queryset(self):
        return super(ProductListView, self).get_queryset().active()

    def get_template_names(self):
        return ['shopit/catalog/product_detail.html']


class AddToCartView(AddToCartViewBase):
    serializer_class = AddToCartSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    lookup_field = 'translations__slug'

    def get_queryset(self):
        return super(ProductListView, self).get_queryset().active()

    def post(self, request, *args, **kwargs):
        """
        Override to add the product to cart.
        """
        errors = {}
        cart = Cart.objects.get_or_create_from_request(request)
        context = self.get_context(request, **kwargs)
        product = context.pop('product')
        quantity = int(request.data.get('quantity', 1))

        if product.is_group:
            errors['variant'] = [_("You can't add a group product to the cart.")]
        else:
            total_quantity = getattr(product.is_in_cart(cart), 'quantity', 0) + quantity
            available, diff = product.is_available(total_quantity)
            if available:
                item, created = CartItem.objects.get_or_create(cart=cart, product=product, quantity=quantity)
                serializer_class = WatchItemSerializer if total_quantity == 0 else CartItemSerializer
                serializer = serializer_class(item, context=context)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            errors['quantity'] = [_('Product not available for given quantity, there is %d left.') % (quantity + diff)]

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
