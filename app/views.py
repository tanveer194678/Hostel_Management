from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Students
from .forms import studentForm
from .serializers import StudentSerializer
from .models import GuestBooking
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date

# Authentication Views
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'auth/register.html')

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'auth/login.html')

@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect('home')

# Web Views
@login_required(login_url='login')
def home(request):
    return render(request, "home.html")

@login_required(login_url='login')
def dashboard(request):
    students_count = Students.objects.count()
    # include guest booking stats for dashboard
    guest_count = GuestBooking.objects.count()
    recent_guest_bookings = GuestBooking.objects.order_by('-created_at')[:5]
    return render(request, "dashboard.html", {
        'students_count': students_count,
        'guest_count': guest_count,
        'recent_guest_bookings': recent_guest_bookings,
    })

@login_required(login_url='login')
def add_students(request):
    form = studentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/view-students/')
    return render(request, 'form.html', {'form': form})

@login_required(login_url='login')
def view_students(request):
    students = Students.objects.all()
    return render(request, 'list.html', {'students': students})

@login_required(login_url='login')
def delete_students(request, id):
    Students.objects.get(id=id).delete()
    return redirect('/view-students/')


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def guest_booking(request):
    """Guest booking page. Saves bookings to DB and redirects to bookings list on success."""
    message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        room = request.POST.get('room')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # Basic validation
        if not name or not email or not room:
            message = {'type': 'error', 'text': 'Please fill name, email and room.'}
        else:
            # parse optional dates (expects YYYY-MM-DD from date input)
            ci = parse_date(check_in) if check_in else None
            co = parse_date(check_out) if check_out else None
            GuestBooking.objects.create(
                name=name,
                email=email,
                room_requested=room,
                check_in=ci,
                check_out=co,
            )
            return redirect('guest_booking_list')

    return render(request, 'guest_booking.html', {'message': message})

# REST API Views
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])

@login_required(login_url='login')
def guest_booking_list(request):
    bookings = GuestBooking.objects.order_by('-created_at')
    return render(request, 'guest_list.html', {'bookings': bookings})


@login_required(login_url='login')
def guest_booking_detail(request, pk):
    try:
        booking = GuestBooking.objects.get(pk=pk)
    except GuestBooking.DoesNotExist:
        return redirect('guest_booking')
    return render(request, 'guest_detail.html', {'booking': booking})
@permission_classes([IsAuthenticated])
def api_student_list(request):
    if request.method == 'GET':
        students = Students.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_student_create(request):
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_student_detail(request, pk):
    try:
        student = Students.objects.get(pk=pk)
    except Students.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)