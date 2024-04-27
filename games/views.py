from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Game, Publisher, Category
from .forms import PublisherForm, GameForm, CategoryForm
from django.views.generic import View, UpdateView, CreateView, DetailView, DeleteView, ListView


class ObjectDetailMixin:
    def get_object(self, queryset=None):
        obj_id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(self.model.objects.prefetch_related('game_set'), pk=obj_id)


class ObjectDeleteMixin:
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return redirect(self.success_url)


class ObjectUpdateMixin:
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return redirect(self.success_url)


class HomeView(View):
    def get(self, request):
        games = Game.objects.all()
        publishers = Publisher.objects.all()
        return render(request, 'home.html', {'games': games, 'publishers': publishers})


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'game/add_game.html'
    success_url = reverse_lazy('home')


class GameDetailView(DetailView):
    model = Game
    template_name = 'game/game_detail.html'
    context_object_name = 'game'
    pk_url_kwarg = 'game_id'
    def get_object(self, queryset=None):
        game_id = self.kwargs.get('game_id')
        return get_object_or_404(Game.objects.prefetch_related('categories', 'publisher'), pk=game_id)


class GameDeleteView(ObjectDeleteMixin, DeleteView):
    model = Game
    template_name = 'game/delete_game_confirmation.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'game_id'


class GameUpdateView(ObjectUpdateMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'game/update_game.html'
    pk_url_kwarg = 'game_id'
    success_url = reverse_lazy('game_detail')

    def form_valid(self, form):
        game = form.save(commit=False)
        game.save()
        return redirect('game_detail', game_id=game.id)

    def get_object(self, queryset=None):
        game_id = self.kwargs.get('game_id')
        return get_object_or_404(Game, pk=game_id)


class PublisherCreateView(CreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'publisher/add_publisher.html'
    success_url = reverse_lazy('publishers')


class PublisherDetailView(ObjectDetailMixin, DetailView):
    model = Publisher
    template_name = 'publisher/publisher_detail.html'
    context_object_name = 'publisher'
    pk_url_kwarg = 'publisher_id'


class PublisherDeleteView(ObjectDeleteMixin, DeleteView):
    model = Publisher
    template_name = 'publisher/delete_publisher_confirmation.html'
    success_url = reverse_lazy('publishers')
    pk_url_kwarg = 'publisher_id'


class PublisherUpdateView(ObjectUpdateMixin, UpdateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'publisher/update_publisher.html'
    pk_url_kwarg = 'publisher_id'
    success_url = reverse_lazy('publishers')


class PublisherListView(ListView):
    model = Publisher
    template_name = 'publisher/publishers.html'
    context_object_name = 'publishers'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/update_category.html'
    success_url = reverse_lazy('categories')


class CategoryListView(ListView):
    model = Category
    template_name = 'category/categories.html'
    context_object_name = 'categories'


class CategoryDetailView(ObjectDetailMixin, DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'


class CategoryDeleteView(ObjectDeleteMixin, DeleteView):
    model = Category
    template_name = 'category/delete_category_confirmation.html'
    success_url = reverse_lazy('categories')
    pk_url_kwarg = 'category_id'


class CategoryUpdateView(ObjectUpdateMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/update_category.html'
    pk_url_kwarg = 'category_id'
    success_url = reverse_lazy('categories')