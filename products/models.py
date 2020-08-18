import random
import os
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator

# filepath is actually the file itself


def get_filename_ext(filepath):
    # get the full file
    base_name = os.path.basename(filepath)
    # split the file into name and file extension(extension return .jpg ....)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    # change the actual file name to random number with the file extension
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    # so it will be like "products/2014304463/2014304463.jpeg"
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

# overriding querysets


class ProductQuerySet(models.query.QuerySet):
    # we can define our business logic here, what field return what
    # so, here our active field return when a product ios active
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    # for search app
    def search(self, query):
        lookups = ( Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(price__icontains=query) |
                    Q(tag__title__icontains=query)
                    )
                    # tshirt, t-shirt, t shirt, red, green, blue,
        
        # distinct() => if title and description both have the same keyword, without it it will return same result twice.
        return self.filter(lookups).distinct()


# our own custom model manager
class ProductManager(models.Manager):
    # overriding get_queryset method
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    # can call it like that => Product.objects.featured()
    def featured(self):
        # this return is in chain. it will call get_queryset() => ProductQuerySet() => featured()
        return self.get_queryset().featured()

    # all() will return all the active ones
    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        # we can do Product.objects.get_queryset() or, self.get_queryset(). Same thing
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    # for search app

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True) #Note:blank true is important for generator 
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # callling custom model manager
    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

# we need django signal to produce a slug if not given before saving the object

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
