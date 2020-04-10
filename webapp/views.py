from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order, billingAddress
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm

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
            order_item.quantity=1
            order.items.remove(order_item)
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                remove_from_cart(request, id)
            messages.info(request, "Qty was updated")
            return redirect("cart")
        else:
            messages.info(request, "Not In your cart")
            return redirect("shop-detail", id=id)
    else:
        messages.info(request, "Not In your cart")
        return redirect("shop-detail", id=id)

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "shop-checkout1.html", context)

    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            form = CheckoutForm(self.request.POST or None)
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                if form.is_valid():
                    add1 = form.cleaned_data.get('add1')
                    add1 = form.cleaned_data.get('add2')
                    country = form.cleaned_data.get('country')
                    zip = form.cleaned_data.get('zip')
                    payment_option = form.cleaned_data.get('payment_option')
                    billing_address = billingAddress(
                        user=self.request.user,
                        add1=add1,
                        add2=add2,
                        country=country,
                        zip=zip
                    )
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()
                    return redirect("checkout-detail")
                # context = {
                #     'object' : order
                # }
                # return render(self.request, "cart.html", context)
            except ObjectDoesNotExist :
                print("Not found")
                return redirect('/')

        # else:
        #     return redirect("shop")

class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "payment.html")