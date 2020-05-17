import random
import string
from django.utils.text import slugify
# '''
# SLUG GENERATEOR AND random_string_generator is located here :
# https://www.codingforentrepreneurs.com/blog/a-unique-slug-generator-for-django/ #SLUG FILE
# http://joincfe.com/blog/random-string-generator-in-python/
# '''
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_id_generator_orders(instance):
    order_new_id = random_string_generator(size=5)
    
    klass = instance.__class__
    qs_exists = klass.objects.filter(order_id = order_new_id).exists()
    if qs_exists:
        return unique_id_generator_orders(instance)
    return order_new_id
    


def unique_slug_generator_pages(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    validate_str = """\/:*?<>|"""
    if new_slug is not None:
        slug = new_slug
    else:
        
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator_pages(instance, new_slug=new_slug)
    return slug
