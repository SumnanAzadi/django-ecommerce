from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product

from carts.models import Cart  # for Add to cart and remove from cart option


class ProductListView(ListView):
    template_name = "products/list.html"

    # default one
    """ queryset = Product.objects.all()
    #no need for this get_context_data(). it is just for see the data in the console
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(
            *args, **kwargs)
        print(context)
        return context """
    # below one is default get_queryset method for list view

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


class ProductDetailView(DetailView):
    template_name = "products/detail.html"

    # Below All method will return extact sme thing. they are different way fo doing

    # default one
    """ queryset = Product.objects.all()
    #no need for this get_context_data(). it is just for see the data in the console
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(
            *args, **kwargs)
        print(context)
        return context """

    # below one is default get_queryset method for detail  view

    """ def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        return Product.objects.filter(pk=pk) """

    # Here we call our custom model manager objects = ProductManager()
    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance


def product_detail_view(request, pk=None, *args, **kwargs):
    # It's either get_object_or_404 or try-except block
    """ instance = get_object_or_404(Product, pk=pk) """

    """ try:
        instance = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        print('no product here')
        raise Http404("Product doesn't exist")
    except:
        print("huh?") """

    # Below one do the exact same thing as above

    """ qs  = Product.objects.filter(id=pk)
    print(qs)
    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product doesn't exist") """

    # filter is model manager method. It makes easier to lookup in DB.
    # We can introduce our own custom model manager.It will do it in our Model

    # Here we call our custom model manager objects = ProductManager()
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")

    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    template_name = "products/featured-detail.html"

    # it's either one from below,same thing, get_queryset is just overriding default method
    queryset = Product.objects.all().featured()
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()


class ProductDetailSlugView(DetailView):
    template_name = "products/detail.html"

    queryset = Product.objects.all()

    # for Add to cart and remove from cart option
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView,
                        self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            print('No product here')
            raise Http404("Product doesn't exist")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("huh? ")
        return instance
