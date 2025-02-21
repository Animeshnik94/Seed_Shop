from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Review
from .forms import ReviewForm
from goods.models import Product

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/add_review.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        form.instance.product = product
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product', kwargs={'product_slug': self.kwargs['product_slug']})

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/edit_review.html'
    context_object_name = 'review'

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('catalog:product', kwargs={'product_slug': self.object.product.slug})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/delete_review.html'
    context_object_name = 'review'

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('catalog:product', kwargs={'product_slug': self.object.product.slug})
