from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        # getter function to get the cart id from the session
        cart_id = request.session.get("cart_id", None)
        # get the id from the database
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            # if it is exist then we set the same cart_obj variable to qs
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                # if user logged in then change the previous "None" user to authenticated one
                cart_obj.user = request.user
                cart_obj.save()
        else:
            # create a brand new cart
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            # setter function to set the cart id to the session
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        # if the user isn"t logged in then create a new session for None user
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                # if the user is logged in then create a new session for logged in user
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    """ print(action)
    print(instance.products.all())
    # pre_remove =before removing the item what were in the dictionary
    # post_remove =after removing the item what are in the dictionary
    # post_add =before adding the item what were in the dictionary
    # post_remove =after adding the item what are in the dictionary """
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        # instance here is the cart_obj
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
