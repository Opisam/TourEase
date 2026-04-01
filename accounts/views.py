from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserUpdateForm, CompanyProfileForm
from .models import User, CompanyProfile


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            
            if user.role == 'provider':
                CompanyProfile.objects.create(
                    user=user,
                    company_name=f"{user.username}'s Company",
                    description="",
                    contact_info=""
                )
            
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser or user.is_staff or user.role == 'admin':
                messages.error(request, 'Administrators must log in via the admin portal.')
                return redirect('login')
            
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    
    context = {
        'user_form': user_form,
    }
    
    if request.user.is_provider():
        try:
            company = request.user.company_profile
            if request.method == 'POST' and 'company_form' in request.POST:
                company_form = CompanyProfileForm(request.POST, request.FILES, instance=company)
                if company_form.is_valid():
                    company_form.save()
                    messages.success(request, 'Company profile updated!')
                    return redirect('profile')
            else:
                company_form = CompanyProfileForm(instance=company)
            context['company_form'] = company_form
            context['company'] = company
        except CompanyProfile.DoesNotExist:
            pass
    
    return render(request, 'accounts/profile.html', context)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(self.request, 'No user found with this email address.')
            return render(self.request, self.template_name, {'form': form})
        
        # 1. Manually generate the link for the on-screen button (fail-safe for dev)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = self.request.build_absolute_uri(
            reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )
        self.request.session['password_reset_link'] = reset_url
        
        # 2. Trigger the standard Django email sending mechanism
        # This will use the SMTP settings in settings.py to send to the registered email
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
        }
        form.save(**opts)
        
        messages.success(self.request, 'A password reset link has been generated and sent to your email.')
        return redirect(self.success_url)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Your password has been set successfully. You can now log in with your new password.')
        return super().form_valid(form)
