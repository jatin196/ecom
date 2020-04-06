from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "index3.html", {})

# def acc_profile(request):
#     return redirect('home')


@login_required()
def shopping_page(request):
    all_pdt = Item.objects.all()
    paginator = Paginator(all_pdt, 2)
    page_req_var = 'page'
    page = request.GET.get(page_req_var)
    try:
        paginated_query_set = paginator.page(page)
    except PageNotAnInteger:
        paginated_query_set =  paginator.page(1)

    except EmptyPage:
        paginatedQuerySet = paginator.page(paginator.num_pages)

    context = {
        'all_pdt' : paginated_query_set,
        'page_req_var' : page_req_var
    }
    return render(request, "shop-category-left.html", context)


def shopping_detail(request, id):
    print("going to shopping detial")
    print(id)
    item = get_object_or_404(Item, id=id)
    context = {
        'pdt': item
    }
    return render(request, "shop-detail.html", context)

@login_required()
def add_to_cart(request, id):
    print("adding to cart clicked")
    print(id)
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added one more ")
            print("adding to cart clicked")
            print(id)
            return redirect("cart")
        else:
            order.items.add(order_item)
            messages.info(request, "Item Added ")
            print("adding to cart clicked")
            print(id)
            return redirect("shop-detail", id=id)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        print("adding to cart clicked")
        print(id)
        return redirect("shop-detail", id=id)

def cart(requset):
    order = Order.objects.get(user=requset.user, ordered=False)
    context = {
        'order' : order
    }
    return render(requset, "shop-basket.html", context)


@login_required()
def remove_from_cart(request, id):
    print("adding to cart clicked")
    print(id)
    item = get_object_or_404(Item, id=id)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]

            order.items.entry_set.remove(order_item)
            order_item.save()
            messages.info(request, "This Item was removed")
            return redirect("shop-detail", id=id)
        else:
            messages.info(request, "Not In your cart")
            return redirect("shop-detail", id=id)
    else:
        messages.info(request, "Not In your cart")
        return redirect("shop-detail", id=id)


@login_required()
def remove_single_from_cart(request, id):
    print("adding to cart clicked")
    print(id)
    item = get_object_or_404(Item, id=id)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=id).exists():

            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity -= 1
            order_item.save()

            messages.info(request, "Qty was updated")
            return redirect("cart")
        else:
            messages.info(request, "Not In your cart")
            return redirect("shop-detail", id=id)
    else:
        messages.info(request, "Not In your cart")
        return redirect("shop-detail", id=id)
