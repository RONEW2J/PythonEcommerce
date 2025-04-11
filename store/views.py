from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .models import Product, Category
from .forms import RegisterForm, LoginForm, VerifyForm, ProductForm

# ---------------------------
# Authentication Views
# ---------------------------

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('product_list')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы вошли в систему!')
            return redirect('product_list')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')

def verify(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == "123456":  # Improve with actual verification logic if needed
                messages.success(request, 'Код подтвержден!')
                return redirect('product_list')
            else:
                messages.error(request, 'Неверный код!')
    else:
        form = VerifyForm()
    return render(request, 'store/verify.html', {'form': form})

# ---------------------------
# Product CRUD with Class‑Based Views
# ---------------------------

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"
    permission_required = "store.view_product"
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = str(self.get_object().id)
        
        # Track recently viewed products
        recent = self.request.session.get("recent_products", [])
        if product_id not in recent:
            recent.append(product_id)
            self.request.session["recent_products"] = recent
        context["recent_products"] = recent
        
        # Track visited products
        visited = self.request.session.get("visited_products", [])
        if product_id not in visited:
            visited.append(product_id)
            self.request.session["visited_products"] = visited
        context["visited_products"] = visited
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_create.html"
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):
        # Optional: add additional custom processing here
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_update.html"
    success_url = reverse_lazy('product_list')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "store/product_confirm_delete.html"
    success_url = reverse_lazy('product_list')

# ---------------------------
# Custom Product View Example
# ---------------------------
# This view shows an example of advanced customization with session data processing

class CustomProductView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "store/product_detail.html"
    permission_required = 'store.view_product'
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        # Update visited list in session
        visited = self.request.session.get('visited_products', [])
        if product_id and product_id not in visited:
            visited.append(product_id)
            self.request.session['visited_products'] = visited
        context['product_id'] = product_id
        return context

# ---------------------------
# View Aliases for URL configuration backward compatibility
# ---------------------------
product_list = ProductListView.as_view()
product_detail = ProductDetailView.as_view()
product_create = ProductCreateView.as_view()
product_update = ProductUpdateView.as_view()
product_delete = ProductDeleteView.as_view()
custom_product = CustomProductView.as_view()

# Alias for logout: Some URL configurations may import 'user_logout'
user_logout = logout_view