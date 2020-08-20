from django.shortcuts import render, redirect


from products.models import Product
from .models import Cart


def cart_home(request):
    # print(request.session)
    # print(request.session.session_key) #output: inn3oycr35dkxqg81lz7a2lkz23vktnx
    # request.session.set_expiry(300) # 5 minutes
    """ request.session['first_name'] = "Sumnan" #setter(can't set object)
    print(request.session.get("first_name", "Unknown")) #getter """

    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    # get the product id from update-cart form name "product_id"
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            # grab the product
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("wrong product_id")
            return redirect("cart:home")
        # grab the current instance or, create a new one
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            # stay in the product page
            # return redirect(product_obj.get_absolute_url())
        else:
            # add the product itself into the instances many to many field(in this case product field).
            cart_obj.products.add(product_obj)
        # get the total Item
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")
