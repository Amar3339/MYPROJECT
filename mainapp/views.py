from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Enquiry, LoginInfo, UserInfo
from adminapp.models import Book


# ---------------- HOME ----------------
def index(request):
    books = Book.objects.all().order_by('-created_at')

    context = {
        'books': books,
        'new_arrivals': books[:8]
    }
    return render(request, 'index.html', context)


# ---------------- ABOUT ----------------
def about(request):
    return render(request, 'about.html')

# search book sectiom
def search_book(request):
    query = request.GET.get('q')

    books = Book.objects.none()

    if query:
        books = Book.objects.filter(title__icontains=query)

    return render(request, 'search_results.html', {
        'books': books,
        'query': query
    })
    


# ---------------- CONTACT ----------------
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


# ---------------- ADMIN LOGIN (KEEP THIS) ----------------
# def adminlogin(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         try:
#             admin = LoginInfo.objects.get(
#                 username=username,
#                 password=password,
#                 usertype="admin"
#             )

#             request.session["adminid"] = admin.username
#             return redirect("admindash")

#         except LoginInfo.DoesNotExist:
#             messages.error(request, "Invalid admin credentials")
#             return redirect("adminlogin")

#     return render(request, "adminlogin.html")


# ---------------- USER REGISTER ----------------
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


# ---------------- COMMON LOGIN ----------------
# def login(request):
#     if request.method == "POST":

#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         usertype = request.POST.get("usertype")

#         # -------- ADMIN LOGIN --------
#         if usertype == "admin":
#             try:
#                 admin = LoginInfo.objects.get(
#                     username=email,
#                     password=password,
#                     usertype="admin"
#                 )

#                 request.session["adminid"] = admin.username
#                 return redirect("admindash")

#             except LoginInfo.DoesNotExist:
#                 messages.error(request, "Invalid admin credentials")
#                 return redirect("login")

#         # -------- USER LOGIN --------
#         try:
#             user = UserInfo.objects.get(email=email, password=password)

#             request.session["user_email"] = user.email
#             request.session["user_name"] = user.name

#             return redirect("/")

#         except UserInfo.DoesNotExist:
#             messages.error(request, "Invalid user credentials")
#             return redirect("login")

#     return render(request, "login.html")

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
# ---------------- BOOK DETAILS ----------------
def book_details(request, id):
    try:
        book = Book.objects.get(id=id)
        return render(request, "book_details.html", {"book": book})
    except Book.DoesNotExist:
        messages.error(request, "Book not found")
        return redirect("index")