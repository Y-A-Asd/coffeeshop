from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from foodmenu.models import Food
from utils import Cart
from .forms import CartAddProductForm, OrderCreateForm
from order.models import OrderItem


# Create your views here.



class CreateCartView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Food, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])
        return redirect('order:detail-cart')



class DeleteCartView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Food, id=product_id)
        cart.remove(product)
        return redirect('order:detail-cart')

class DetailCartView(View):
    template_name = 'Order_DetailCart.html'
    def get(self, request):
            cart = Cart(request)
            for item in cart:
                item['update_quantity_form'] = CartAddProductForm(initial={
                    'quantity': item['quantity'],
                    'override': True})
            return render(request, self.template_name, {'cart': cart})

class MakeOrderView(View):
    template_name = 'Order_CreateOrder.html'
    def get (self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request, self.template_name, {'cart': cart, 'form': form})
    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():

            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
        return render(request, self.template_name, {'order': order})