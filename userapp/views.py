from django.shortcuts import render, redirect
from django.contrib import messages

from adminapp.models import *
from mainapp.models import *
from userapp.models import *


def userdash(request):
    if 'user_email' not in request.session:
        messages.error(request, 'Please login first!')
        return redirect('login')
    return render(request, 'userdash.html')


def userlogout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def viewcart(request):
    if 'user_email' not in request.session:
        return redirect('login')

    try:
        email = request.session['user_email']
        user = UserInfo.objects.get(email=email)
    except:
        return redirect('login')

    cart, _ = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.book.price * item.quantity for item in items)

    return render(request, 'viewcart.html', {
        'items': items,
        'total': total
    })


def addtocart(request, id):
    if 'user_email' not in request.session:
        messages.error(request, "Please login first")
        return redirect('login')

    email = request.session['user_email']

    try:
        user = UserInfo.objects.get(email=email)
        book = Book.objects.get(id=id)
    except:
        messages.error(request, "Invalid request")
        return redirect('login')

    cart, _ = Cart.objects.get_or_create(user=user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('viewcart')


def removeitem(request, id):
    if 'user_email' not in request.session:
        messages.error(request, "Please login first")
        return redirect('login')

    email = request.session['user_email']

    try:
        user = UserInfo.objects.get(email=email)
        cart = Cart.objects.get(user=user)
        book = Book.objects.get(id=id)
    except:
        messages.error(request, "Error removing item")
        return redirect('viewcart')

    CartItem.objects.filter(cart=cart, book=book).delete()

    messages.success(request, "Book removed from cart")
    return redirect('viewcart')