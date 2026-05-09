from django import forms
from django.contrib.auth.models import User
from shop.models import Product, ProductCategory
from services.models import Service, ServiceCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'description', 'short_description',
            'price', 'discount_price', 'stock', 'image', 'image_2', 'image_3',
            'is_active', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Product Name'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Full Description',
                'rows': 4
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Short Description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Price (e.g. 500.00)'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Discount Price (Optional)'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Stock Quantity'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm'
            }),
            'image_2': forms.FileInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm'
            }),
            'image_3': forms.FileInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-maroon-600 bg-white border-gray-300 rounded focus:ring-maroon-500 focus:ring-2'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-maroon-600 bg-white border-gray-300 rounded focus:ring-maroon-500 focus:ring-2'
            }),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Email Address'
            }),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'name', 'category', 'description', 'short_description',
            'duration', 'price', 'discount_price', 'image',
            'is_active', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Service Name'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Full Description',
                'rows': 4
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Short Description'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Duration (e.g., 2-3 hours)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Price (e.g. 1500.00)'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Discount Price (Optional)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-maroon-600 bg-white border-gray-300 rounded focus:ring-maroon-500 focus:ring-2'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-maroon-600 bg-white border-gray-300 rounded focus:ring-maroon-500 focus:ring-2'
            }),
        }

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'slug', 'description', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Category Name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'URL slug (e.g. skin-care)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Category Description',
                'rows': 3
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-maroon-600 bg-white border-gray-300 rounded focus:ring-maroon-500 focus:ring-2'
            }),
        }

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['name', 'description', 'image', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Category Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm placeholder-gray-500',
                'placeholder': 'Category Description',
                'rows': 3
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-5 py-4 bg-white/50 backdrop-blur-md rounded-xl border border-white/40 focus:ring-2 focus:ring-maroon-500 focus:border-transparent transition-all shadow-sm'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-maroon-600 bg-white border-gray-300 rounded focus:ring-maroon-500 focus:ring-2'
            }),
        }
