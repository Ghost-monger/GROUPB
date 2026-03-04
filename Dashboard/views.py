from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from Dashboard.models import Student, Payment
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient



# Create your views here.
@login_required
def dashboard(request):
    students = Student.objects.all()
    return render(request, 'dashboard.html', {'students': students})
def add_student(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        course = request.POST.get('course')
        age = request.POST.get('age')
        email = request.POST.get('email')
        gender = request.POST.get('gender','').capitalize()
        date = request.POST.get('date')

        Student.objects.create(
            image = image,
            name=name,
            course=course,
            age=age,
            email=email,
            gender=gender,
            date=date
        )
        return redirect('dashboard')
    return render(request, 'add_student.html')

def update_student(request,id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        if request.FILES.get('image'):
            student.image = request.FILES.get('image')
        student.name = request.POST.get('name')
        student.course = request.POST.get('course')
        student.age = request.POST.get('age')
        student.email = request.POST.get('email')
        student.gender = request.POST.get('gender','').capitalize()
        date_value = request.POST.get('date')

        if date_value == "":
            date_value = None

        student.date = date_value
        student.save()

        return redirect('dashboard')
    return render(request, 'update_student.html', {'student': student})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
    return redirect('dashboard')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        login(request,user)
        return redirect('dashboard')
    return render(request, 'sign_up.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username OR password !')
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def payment(request,id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        if not phone or not amount:
            messages.error(request, 'All fields are required!')
            return render(request, 'payment.html',
                                {'student': student})
        try:
            client = MpesaClient()
            response = client.stk_push(
                phone,int(amount),'eMobilis',
                'Payment for fee','https://example.com/callback/'
            ).json()
            Payment.objects.create(user=request.user,
                                   phone=phone,
                                   amount=amount,
                                   checkout_request_id=response.get('checkout_request_id',''),
                                   status = 'pending')
            messages.success(request, 'STK Sent! Check your phone')
        except Exception:
            messages.error(request, 'Payment failed!')

    return render(request, 'payment.html', {'student': student})
