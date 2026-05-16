from django.shortcuts import render, redirect
from django.contrib import messages

from adminapp.models import *
from mainapp.models import *
from userapp.models import *



def userdash(request):
    if 'useremail' not in request.session:
        messages.error(request,'Please login first!')
        return redirect('login')
    return render(request,'userdash.html')



def userlogout(request):

    request.session.flush()  

    messages.success(request, "You have been logged out successfully.")

    return redirect('login')

def viewcart(request):

    if 'user_email' not in request.session:
        return redirect('login')

    email = request.session['user_email']
    user = UserInfo.objects.get(email=email)

    cart, created = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.filter(cart=cart)

    total = 0
    for item in items:
        total += item.book.price * item.quantity

    return render(request, 'viewcart.html', {
        'items': items,
        'total': total
    })

def addtocart(request, id):

    if 'user_email' not in request.session:
        messages.error(request, "Please login first")
        return redirect('login')

    email = request.session['user_email']

    user = UserInfo.objects.get(email=email)
    book = Book.objects.get(id=id)

    cart, created = Cart.objects.get_or_create(user=user)

    CartItem.objects.create(
        cart=cart,
        book=book,
        quantity=1
    )

    return redirect('viewcart')
# def removeitem(request, id):
#     if 'userid' not in request.session:
#         messages.error(request,"Please login first")
#         return redirect('login')

#     email = request.session['userid']          # email session से लो
#     user = UserInfo.objects.get(email=email)   # email से user ढूंढो

#     cart = Cart.objects.get(user=user)
#     book = Book.objects.get(id=id)

#     CartItem.objects.filter(cart=cart, book=book).delete()

#     messages.success(request,"Book removed from cart")
#     return redirect('viewcart')
def removeitem(request, id):

    if 'user_email' not in request.session:
        messages.error(request,"Please login first")
        return redirect('login')

    email = request.session['user_email']
    user = UserInfo.objects.get(email=email)

    cart = Cart.objects.get(user=user)
    book = Book.objects.get(id=id)

    CartItem.objects.filter(cart=cart, book=book).delete()

    messages.success(request,"Book removed from cart")
    return redirect('viewcart')