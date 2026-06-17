from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import timedelta, date
from store.models import Product, Category
from orders.models import Order, OrderItem
from django.contrib.auth.models import User
import json

@staff_member_required
def dashboard(request):
    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    last_30_days = today - timedelta(days=30)

    # ── KEY METRICS ──
    total_revenue    = Order.objects.filter(paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders     = Order.objects.count()
    total_customers  = User.objects.filter(is_staff=False).count()
    total_products   = Product.objects.filter(available=True).count()
    pending_orders   = Order.objects.filter(status='pending').count()
    today_revenue    = Order.objects.filter(paid=True, created__date=today).aggregate(Sum('total_price'))['total_price__sum'] or 0
    this_month_rev   = Order.objects.filter(paid=True, created__date__gte=this_month_start).aggregate(Sum('total_price'))['total_price__sum'] or 0
    avg_order_value  = Order.objects.filter(paid=True).aggregate(Avg('total_price'))['total_price__avg'] or 0

    # ── ORDER STATUS BREAKDOWN ──
    status_counts = {
        'pending':    Order.objects.filter(status='pending').count(),
        'processing': Order.objects.filter(status='processing').count(),
        'shipped':    Order.objects.filter(status='shipped').count(),
        'delivered':  Order.objects.filter(status='delivered').count(),
        'cancelled':  Order.objects.filter(status='cancelled').count(),
    }

    # ── MONTHLY SALES (last 12 months) ──
    monthly_sales = []
    monthly_labels = []
    for i in range(11, -1, -1):
        d = today.replace(day=1) - timedelta(days=i*30)
        month_start = d.replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year+1, month=1, day=1)
        else:
            month_end = month_start.replace(month=month_start.month+1, day=1)
        rev = Order.objects.filter(
            paid=True,
            created__date__gte=month_start,
            created__date__lt=month_end
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0
        monthly_sales.append(float(rev))
        monthly_labels.append(month_start.strftime('%b %Y'))

    # ── DAILY ORDERS (last 30 days) ──
    daily_orders = []
    daily_labels = []
    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        count = Order.objects.filter(created__date=d).count()
        daily_orders.append(count)
        daily_labels.append(d.strftime('%d %b'))

    # ── SALES BY CATEGORY ──
    category_sales = []
    category_labels = []
    for cat in Category.objects.all():
        total = OrderItem.objects.filter(
            product__category=cat,
            order__paid=True
        ).aggregate(
            total=Sum('price')
        )['total'] or 0
        if total > 0:
            category_sales.append(float(total))
            category_labels.append(cat.name)

    # ── TOP SELLING PRODUCTS ──
    top_products = OrderItem.objects.values(
        'product__name'
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:8]

    top_product_labels = [p['product__name'][:20] for p in top_products]
    top_product_values = [p['total_sold'] for p in top_products]

    # ── RECENT ORDERS ──
    recent_orders = Order.objects.select_related('user').order_by('-created')[:10]

    # ── NEW CUSTOMERS (last 30 days) ──
    new_customers = User.objects.filter(
        is_staff=False,
        date_joined__date__gte=last_30_days
    ).order_by('-date_joined')[:8]

    # ── LOW STOCK PRODUCTS ──
    low_stock = Product.objects.filter(stock__lte=5, available=True).order_by('stock')[:10]

    # ── RECENT CUSTOMERS ──
    recent_customers = User.objects.filter(
        is_staff=False
    ).order_by('-date_joined')[:8]

    context = {
        # Metrics
        'total_revenue':   total_revenue,
        'total_orders':    total_orders,
        'total_customers': total_customers,
        'total_products':  total_products,
        'pending_orders':  pending_orders,
        'today_revenue':   today_revenue,
        'this_month_rev':  this_month_rev,
        'avg_order_value': round(avg_order_value, 2),
        'status_counts':   status_counts,

        # Charts
        'monthly_labels':      json.dumps(monthly_labels),
        'monthly_sales':       json.dumps(monthly_sales),
        'daily_labels':        json.dumps(daily_labels),
        'daily_orders':        json.dumps(daily_orders),
        'category_labels':     json.dumps(category_labels),
        'category_sales':      json.dumps(category_sales),
        'top_product_labels':  json.dumps(top_product_labels),
        'top_product_values':  json.dumps(top_product_values),

        # Tables
        'recent_orders':    recent_orders,
        'low_stock':        low_stock,
        'recent_customers': recent_customers,
        'new_customers':    new_customers,
    }
    return render(request, 'dashboard/dashboard.html', context)