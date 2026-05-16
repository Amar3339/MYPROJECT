from django.shortcuts import render, redirect
from django.contrib import messages
from adminapp.models import Category, Book
from mainapp.models import Enquiry, LoginInfo


# ---------------- Dashboard ----------------
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first!")
        return redirect('adminlogin')

    return render(request, 'admindash.html')


# ---------------- Logout ----------------
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, "Logged out successfully!")
    else:
        messages.error(request, "You are not logged in!")

    return redirect('adminlogin')


# ---------------- View Enquiry ----------------
def viewenquiry(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    enquiries = Enquiry.objects.all()
    return render(request, 'viewenquiry.html', {'enqs': enquiries})


# ---------------- Delete Enquiry ----------------
def delenquiry(request, id):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    try:
        enquiry = Enquiry.objects.get(id=id)
        enquiry.delete()
        messages.success(request, "Enquiry deleted successfully!")
    except Enquiry.DoesNotExist:
        messages.error(request, "Enquiry not found!")

    return redirect('viewenquiry')


# ---------------- Change Password ----------------
def adminchangepwd(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    if request.method == "POST":
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        cpwd = request.POST.get('cpwd')

        adminid = request.session['adminid']

        try:
            admin = LoginInfo.objects.get(username=adminid)

            if admin.password != oldpwd:
                messages.error(request, "Old password does not match!")
            elif newpwd != cpwd:
                messages.error(request, "New passwords do not match!")
            else:
                admin.password = newpwd
                admin.save()
                messages.success(request, "Password changed successfully!")
                return redirect('admindash')

        except LoginInfo.DoesNotExist:
            messages.error(request, "Admin not found!")

    return render(request, 'adminchangepwd.html')


# ---------------- Add Category ----------------
def addcat(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        category = Category(name=name, description=description)
        category.save()

        messages.success(request, "Category added successfully!")
        return redirect('addcat')

    return render(request, 'addcat.html')


# ---------------- View Category ----------------
def viewcat(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    categories = Category.objects.all()
    return render(request, 'viewcat.html', {'cats': categories})


# ---------------- Add Book ----------------
def addbook(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        original_price = request.POST.get('original_price')
        price = request.POST.get('price')
        published_date = request.POST.get('published_date')
        language = request.POST.get('language')
        stock = request.POST.get('stock')
        cover_image = request.FILES.get('cover_image')

        try:
            category = Category.objects.get(id=category_id)

            book = Book(
                title=title,
                author=author,
                category=category,
                description=description,
                original_price=original_price,
                price=price,
                published_date=published_date,
                language=language,
                stock=stock,
                cover_image=cover_image
            )
            book.save()

            messages.success(request, "Book added successfully!")
            return redirect('addbook')

        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected!")

    return render(request, 'addbook.html', {'categories': categories})


# ---------------- View Book ----------------
def viewbook(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    books = Book.objects.all()
    return render(request, 'viewbook.html', {'books': books})


# _________________deletecateogry____________
def delcat(request, id):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('viewcat')


# ____________editcateogy________________
def editcat(request, id):
    if 'adminid' not in request.session:
        return redirect('adminlogin')

    category = Category.objects.get(id=id)

    if request.method == "POST":
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect('viewcat')

    return render(request, 'editcat.html', {'cat': category})

# Delete Book
def delbook(request, id):
    if 'adminid' not in request.session:
        return redirect('adminlogin')
    
    book = Book.objects.get(id=id)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('viewbook')


# Edit Book
def editbook(request, id):
    if 'adminid' not in request.session:
        return redirect('adminlogin')
    
    book = Book.objects.get(id=id)
    categories = Category.objects.all()

    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        category_id = request.POST.get('category')
        book.category = Category.objects.get(id=category_id)
        book.description = request.POST.get('description')
        book.original_price = request.POST.get('original_price')
        book.price = request.POST.get('price')
        book.published_date = request.POST.get('published_date')
        book.language = request.POST.get('language')
        book.stock = request.POST.get('stock')
        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES.get('cover_image')
        book.save()
        messages.success(request, "Book updated successfully!")
        return redirect('viewbook')

    return render(request, 'editbook.html', {'book': book, 'categories': categories})