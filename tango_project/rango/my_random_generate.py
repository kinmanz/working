
from .models import Category
import uuid


def generate(n=40):
    gen_str = str(uuid.uuid4().hex.lower()[0:n])
    while True:
        if Category.objects.filter(lock=gen_str).count() == 0:
            break
        gen_str = str(uuid.uuid4().hex.lower()[0:n])
    return gen_str