from category.models import Category
from store.models import Product


def menu_links(request):
    links = Category.objects.all()
    prod = Product.objects.all()
    cat_list=[]
    for cat in Category.objects.all():
        cate = Product.objects.all().filter(category=cat)
        cat_count = cate.count()
        cat_list.append(cat_count)
    return dict(links=links,prod=prod)