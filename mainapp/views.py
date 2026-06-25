from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Enquiry, LoginInfo, UserInfo
from adminapp.models import Book ,Category



def index(request):
    books = Book.objects.all().order_by('-created_at')

    context = {
        'books': books,
        'new_arrivals': books[:8]
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')

# search book section
def search_book(request):
    query = request.GET.get('q')

    books = Book.objects.none()

    if query:
        books = Book.objects.filter(title__icontains=query)

    return render(request, 'search_results.html', {
        'books': books,
        'query': query
    })
    

def contact(request):
    if request.method == 'POST':
        Enquiry.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            contact=request.POST.get('contact'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        messages.success(request, "Your enquiry has been submitted!")
        return redirect('contact')

    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            messages.error(request, "Password mismatch")
            return redirect('register')

        if LoginInfo.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        login_obj = LoginInfo.objects.create(
            usertype='user',
            username=email,
            password=password
        )

        UserInfo.objects.create(
            name=name,
            email=email,
            contact=contact,
            password=password,
            login=login_obj
        )

        messages.success(request, "Registration successful")
        return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        usertype = request.POST.get("usertype")

        user = LoginInfo.objects.filter(
            username=email,
            password=password,
            usertype=usertype
        ).first()

        if user:
            if user.usertype == "admin":
                request.session["adminid"] = user.username
                return redirect("admindash")
            else:
                try:
                    userinfo = UserInfo.objects.get(email=user.username)
                except UserInfo.DoesNotExist:
                    messages.error(request, "User profile not found")
                    return redirect("login")

                request.session["user_email"] = userinfo.email
                request.session["user_name"] = userinfo.name
                return redirect("/")

        messages.error(request, "Invalid credentials")
        return redirect("login")

    return render(request, "login.html")

def book_details(request, id):
    try:
        book = Book.objects.get(id=id)
        return render(request, "book_details.html", {"book": book})
    except Book.DoesNotExist:
        messages.error(request, "Book not found")
        return redirect("index")
    
def category_list(request):

    categories = Category.objects.all()

    return render(request, 'category_list.html', {

        'categories': categories

    })

def category_books(request, category_id):

    category = get_object_or_404(Category, id=category_id)

    books = Book.objects.filter(category=category)

    return render(request, 'category_books.html', {

        'category': category,

        'books': books

    })