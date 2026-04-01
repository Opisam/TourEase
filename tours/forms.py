from django import forms
from .models import TourPackage, BookingRequest, Review, Message


class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ('title', 'description', 'location', 'price', 'duration_days', 
                  'max_group_size', 'tour_type', 'itinerary', 'image', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500', 'step': '0.01'}),
            'duration_days': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'max_group_size': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'tour_type': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'itinerary': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 6}),
            'image': forms.FileInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded text-emerald-600'}),
        }


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ('travel_date', 'number_of_people', 'special_requests')
        widgets = {
            'travel_date': forms.DateInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500', 'type': 'date'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'special_requests': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 3}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'comment': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 3}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 3, 'placeholder': 'Type your message...'}),
        }
