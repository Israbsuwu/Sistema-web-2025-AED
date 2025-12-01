import os
from django import template
from django.conf import settings
from django.core.files.storage import default_storage

register = template.Library()

@register.filter
def extra_images(prod_id):
    """Return list of File-like objects for extra images of product id."""
    base_dir = os.path.join('productos', 'extra', str(prod_id))
    abs_dir = os.path.join(settings.MEDIA_ROOT, base_dir)
    files = []
    if os.path.isdir(abs_dir):
        for fname in sorted(os.listdir(abs_dir)):
            rel_path = os.path.join(base_dir, fname).replace('\\', '/')
            class Obj:
                name = rel_path
                url = default_storage.url(rel_path)
            files.append(Obj())
    return files
