from django.shortcuts import render
from django.http import HttpResponse

from .forms import ItemsForm

# Create your views here.

def start(request):
    items_form = ItemsForm()
    return render(request, 'shopcart/index.html', {'items_form' : items_form})


def checkout(request):
    cart_items = request.POST.getlist('store_items')
    itemlist = {}
    sum = 0
    for item in cart_items:
        if item == 'mobile':
            itemlist['mobile'] = 12000
            sum += 12000
        if item == 'pencil':
            itemlist['pencil'] = 100
            sum += 100
        if item == 'textbooks':
            itemlist['textbooks'] = 2000
            sum += 2000
        if item == 'shirts':
            itemlist['shirts'] = 500
            sum += 500
    itemlist['sum'] = sum
    return render(request, 'shopcart/cart.html', {'itemlist' : itemlist})

def invoice(request):
    payable_amt = request.POST['hidden_pay_amt']
    return render(request, 'shopcart/invoice.html', {'payable_amt': payable_amt})

