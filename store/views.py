from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Review


def home(request):
    categories  = Category.objects.all()[:8]
    featured    = Product.objects.filter(is_featured=True,   available=True)[:8]
    bestsellers = Product.objects.filter(is_bestseller=True, available=True)[:8]
    new_arrivals= Product.objects.filter(available=True).order_by('-created')[:8]
    deals       = Product.objects.filter(available=True).exclude(original_price=None)[:8]
    return render(request, 'store/home.html', {
        'categories':  categories,
        'featured':    featured,
        'bestsellers': bestsellers,
        'new_arrivals':new_arrivals,
        'deals':       deals,
    })


def product_list(request, category_slug=None):
    category  = None
    products  = Product.objects.filter(available=True)
    sort      = request.GET.get('sort', 'newest')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brand     = request.GET.get('brand')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if brand:
        products = products.filter(brand__icontains=brand)

    sort_map = {
        'newest':     '-created',
        'price_low':  'price',
        'price_high': '-price',
        'rating':     '-rating',
    }
    products = products.order_by(sort_map.get(sort, '-created'))
    brands   = Product.objects.values_list('brand', flat=True).distinct().exclude(brand='')

    return render(request, 'store/product_list.html', {
        'category':   category,
        'categories': Category.objects.all(),
        'products':   products,
        'sort':       sort,
        'brands':     brands,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    reviews = product.reviews.all()

    if request.method == 'POST' and request.user.is_authenticated:
        rating = int(request.POST.get('rating', 5))
        title  = request.POST.get('title', '')
        body   = request.POST.get('body', '')
        Review.objects.update_or_create(
            product=product, user=request.user,
            defaults={'rating': rating, 'title': title, 'body': body}
        )
        messages.success(request, 'Review submitted!')
        return redirect(product.get_absolute_url())

    wishlist_ids = []
    if request.user.is_authenticated:
        from accounts.models import Wishlist
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'store/product_detail.html', {
        'product':  product,
        'related':  related,
        'reviews':  reviews,
        'wishlist': wishlist_ids,
    })


def search(request):
    query    = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'store/product_list.html', {
        'products':   products,
        'query':      query,
        'categories': Category.objects.all(),
        'brands':     [],
        'sort':       'newest',
    })


@login_required
def wishlist(request):
    from accounts.models import Wishlist
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'items': items})


@login_required
def wishlist_toggle(request, product_id):
    from accounts.models import Wishlist
    product = get_object_or_404(Product, id=product_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        messages.info(request, f'Removed {product.name} from wishlist.')
    else:
        messages.success(request, f'Added {product.name} to wishlist.')
    return redirect(request.META.get('HTTP_REFERER', '/'))