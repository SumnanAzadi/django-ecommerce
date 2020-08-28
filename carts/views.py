from django.shortcuts import render, redirect
from django.http import JsonResponse

# For order App start here
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
# For order App end here

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
            added = False
            # stay in the product page
            # return redirect(product_obj.get_absolute_url())
        else:
            # add the product itself into the instances many to many field(in this case product field).
            cart_obj.products.add(product_obj)
            added = True
        # get the total Item
        request.session['cart_items'] = cart_obj.products.count()

        # For ajaxifying add to cart
        if request.is_ajax():
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200)  # HttpResponse
            # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework

    return redirect("cart:home")


# order app (checkout)
def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(
                billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(
                id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(
                id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        "check that order is done"
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
    }
    return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
