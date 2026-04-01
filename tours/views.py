from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from accounts.models import User
from .models import TourPackage, BookingRequest, Review, Message
from .forms import TourPackageForm, BookingRequestForm, ReviewForm, MessageForm


def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'provider':
            return redirect('provider_dashboard')
        else:
            return redirect('tour_list')
            
    featured_tours = TourPackage.objects.filter(is_approved=True, is_active=True)[:6]
    return render(request, 'tours/home.html', {'featured_tours': featured_tours})


def tour_list(request):
    tours = TourPackage.objects.filter(is_approved=True, is_active=True)
    
    location = request.GET.get('location')
    tour_type = request.GET.get('tour_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    duration = request.GET.get('duration')
    
    if location:
        tours = tours.filter(location__icontains=location)
    if tour_type:
        tours = tours.filter(tour_type=tour_type)
    if min_price:
        tours = tours.filter(price__gte=min_price)
    if max_price:
        tours = tours.filter(price__lte=max_price)
    if duration:
        tours = tours.filter(duration_days__lte=duration)
    
    paginator = Paginator(tours, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tours/tour_list.html', {
        'page_obj': page_obj,
        'tours': page_obj.object_list,
    })


def tour_detail(request, tour_id):
    tour = get_object_or_404(TourPackage, id=tour_id)
    reviews = tour.reviews.all()[:5]

    # Check if user is a customer
    is_customer = request.user.is_authenticated and request.user.role == 'customer'

    if request.method == 'POST' and is_customer:
        booking_form = BookingRequestForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.save()
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('tour_detail', tour_id=tour.id)
    else:
        booking_form = BookingRequestForm() if is_customer else None
    
    context = {
        'tour': tour,
        'reviews': reviews,
        'booking_form': booking_form,
        'is_customer': is_customer,
    }
    return render(request, 'tours/tour_detail.html', context)


@login_required
def create_tour(request):
    if not request.user.is_provider():
        messages.error(request, 'Only tour providers can create tours')
        return redirect('home')
    
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                tour = form.save(commit=False)
                tour.company = request.user
                tour.save()
                messages.success(request, 'Tour created successfully! Waiting for approval.')
                return redirect('provider_dashboard')
            except Exception as e:
                messages.error(request, f'Error creating tour: {str(e)}')
        else:
            if 'image' in form.errors:
                messages.error(request, 'Invalid image file. Please upload a valid image file (JPG, PNG, GIF).')
    else:
        form = TourPackageForm()
    
    return render(request, 'tours/create_tour.html', {'form': form})


@login_required
def edit_tour(request, tour_id):
    if not request.user.is_provider():
        messages.error(request, 'Only tour providers can edit tours')
        return redirect('home')
    
    tour = get_object_or_404(TourPackage, id=tour_id, company=request.user)
    
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tour updated successfully!')
            return redirect('provider_dashboard')
    else:
        form = TourPackageForm(instance=tour)
    
    return render(request, 'tours/edit_tour.html', {'form': form, 'tour': tour})


@login_required
def delete_tour(request, tour_id):
    if not request.user.is_provider():
        messages.error(request, 'Only tour providers can delete tours')
        return redirect('home')
    
    tour = get_object_or_404(TourPackage, id=tour_id, company=request.user)
    tour.delete()
    messages.success(request, 'Tour deleted successfully!')
    return redirect('provider_dashboard')


@login_required
def provider_dashboard(request):
    if not request.user.is_provider():
        messages.error(request, 'Access denied')
        return redirect('home')
    
    tours = TourPackage.objects.filter(company=request.user)
    bookings = BookingRequest.objects.filter(tour__company=request.user).order_by('-created_at')
    
    pending_bookings = bookings.filter(status='pending')
    total_bookings = bookings.count()
    approved_tours = tours.filter(is_approved=True).count()
    total_users = User.objects.count()
    
    popular_tours = tours.annotate(num_bookings=Count('bookings')).filter(num_bookings__gt=0).order_by('-num_bookings')[:5]
    total_revenue = bookings.filter(status='completed').aggregate(total=Sum('tour__price'))['total'] or 0
    recent_reviews = Review.objects.filter(tour__company=request.user).order_by('-created_at')[:5]
    
    context = {
        'tours': tours,
        'bookings': bookings[:10],
        'pending_bookings': pending_bookings,
        'total_bookings': total_bookings,
        'approved_tours': approved_tours,
        'total_users': total_users,
        'popular_tours': popular_tours,
        'total_revenue': total_revenue,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'tours/provider_dashboard.html', context)


@login_required
def manage_bookings(request):
    if not request.user.is_provider():
        messages.error(request, 'Access denied')
        return redirect('home')
    
    bookings = BookingRequest.objects.filter(tour__company=request.user).order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tours/manage_bookings.html', {'page_obj': page_obj})


@login_required
def update_booking_status(request, booking_id, status):
    if not request.user.is_provider():
        messages.error(request, 'Access denied')
        return redirect('home')
    
    booking = get_object_or_404(BookingRequest, id=booking_id, tour__company=request.user)
    booking.status = status
    booking.save()
    messages.success(request, f'Booking {status} successfully!')
    return redirect('manage_bookings')


@login_required
def my_bookings(request):
    bookings = BookingRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tours/my_bookings.html', {'bookings': bookings})


@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(TourPackage, id=tour_id, is_approved=True)
    
    has_booked = BookingRequest.objects.filter(
        user=request.user, 
        tour=tour, 
        status='completed'
    ).exists()
    
    if not has_booked:
        messages.error(request, 'You can only review tours you have completed')
        return redirect('tour_detail', tour_id=tour.id)
    
    if Review.objects.filter(user=request.user, tour=tour).exists():
        messages.error(request, 'You have already reviewed this tour')
        return redirect('tour_detail', tour_id=tour.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('tour_detail', tour_id=tour.id)
    else:
        form = ReviewForm()
    
    return render(request, 'tours/add_review.html', {'form': form, 'tour': tour})


@login_required
def respond_to_review(request, review_id):
    if not request.user.is_provider():
        messages.error(request, 'Access denied')
        return redirect('home')
        
    review = get_object_or_404(Review, id=review_id, tour__company=request.user)
    
    if request.method == 'POST':
        response_text = request.POST.get('provider_response')
        if response_text:
            review.provider_response = response_text
            review.save()
            messages.success(request, 'Response submitted successfully!')
        else:
            messages.error(request, 'Response cannot be empty.')
            
    return redirect('provider_dashboard')


@login_required
def messages_view(request):
    sent_messages = Message.objects.filter(sender=request.user)
    received_messages = Message.objects.filter(receiver=request.user)
    
    # Only show users we chatted with to keep the inbox clean
    chatted_user_ids = set(sent_messages.values_list('receiver_id', flat=True)) | \
                       set(received_messages.values_list('sender_id', flat=True))
    
    selected_user_id = request.GET.get('user')
    conversation = None
    receiver = None
    
    if selected_user_id:
        receiver = get_object_or_404(User, id=selected_user_id)
        # Ensure the selected receiver appears in the inbox list even if no messages exist yet
        chatted_user_ids.add(receiver.id)
        
        if request.method == 'POST':
            content = request.POST.get('content')
            if content:
                Message.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    content=content
                )
                return redirect(f'/messages/?user={selected_user_id}')
                
        conversation = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=receiver)) |
            (Q(sender=receiver) & Q(receiver=request.user))
        ).order_by('created_at')
        
        Message.objects.filter(sender=receiver, receiver=request.user, is_read=False).update(is_read=True)
    
    all_users = User.objects.filter(id__in=chatted_user_ids).exclude(id=request.user.id)
    
    return render(request, 'tours/messages.html', {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
        'all_users': all_users,
        'conversation': conversation,
        'receiver': receiver,
        'selected_user_id': selected_user_id,
    })


@login_required
def send_message(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, 'Message sent!')
            return redirect(f'/messages/?user={user_id}')
    else:
        form = MessageForm()
    
    return render(request, 'tours/send_message.html', {'form': form, 'receiver': receiver})


@login_required
def admin_dashboard(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied')
        return redirect('home')
    
    total_users = User.objects.count()
    total_providers = User.objects.filter(role='provider').count()
    
    context = {
        'total_users': total_users,
        'total_providers': total_providers,
    }
    return render(request, 'tours/admin_dashboard.html', context)
