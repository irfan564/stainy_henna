from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomerProfile


class CustomerRegistrationForm(UserCreationForm):
    """Registration form for new customers (Email as Username)."""
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
            'placeholder': 'First Name',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
            'placeholder': 'Last Name',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
            'placeholder': 'Email Address',
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
            'placeholder': 'Phone Number',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
            'placeholder': 'Confirm Password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Use email as username behind the scenes
        if commit:
            user.save()
        return user


class CustomerLoginForm(AuthenticationForm):
    """Login form for customers (Using Email)."""
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
            'placeholder': 'Email Address',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
            'placeholder': 'Password',
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating customer profile."""
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
        })
    )

    class Meta:
        model = CustomerProfile
        fields = ['phone', 'whatsapp_number', 'address', 'city', 'state', 'pincode', 'profile_image', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
                'rows': 3,
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'w-full px-5 py-3 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm',
                'type': 'date',
            }),
        }
