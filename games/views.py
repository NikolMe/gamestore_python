from django.contrib.auth import logout
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login


# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Game, Publisher, Category
from .forms import PublisherForm, GameForm, CategoryForm, SignUpForm
from django.views.generic import View, UpdateView, CreateView, DetailView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test


def user_is_manager(user):
    return user.groups.filter(name='manager').exists()


def user_is_admin(user):
    return user.groups.filter(name='admin').exists()


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


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        games = Game.objects.all()
        publishers = Publisher.objects.all()
        return render(request, 'home.html', {'games': games, 'publishers': publishers})


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'game/add_game.html'
    success_url = reverse_lazy('home')


@method_decorator(login_required, name='dispatch')
class GameDetailView(DetailView):
    model = Game
    template_name = 'game/game_detail.html'
    context_object_name = 'game'
    pk_url_kwarg = 'game_id'

    def get_object(self, queryset=None):
        game_id = self.kwargs.get('game_id')
        return get_object_or_404(Game.objects.prefetch_related('categories', 'publisher'), pk=game_id)


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
class GameDeleteView(ObjectDeleteMixin, DeleteView):
    model = Game
    template_name = 'game/delete_game_confirmation.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'game_id'


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
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


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
class PublisherCreateView(CreateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'publisher/add_publisher.html'
    success_url = reverse_lazy('publishers')


@method_decorator(login_required, name='dispatch')
class PublisherDetailView(ObjectDetailMixin, DetailView):
    model = Publisher
    template_name = 'publisher/publisher_detail.html'
    context_object_name = 'publisher'
    pk_url_kwarg = 'publisher_id'


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
class PublisherDeleteView(ObjectDeleteMixin, DeleteView):
    model = Publisher
    template_name = 'publisher/delete_publisher_confirmation.html'
    success_url = reverse_lazy('publishers')
    pk_url_kwarg = 'publisher_id'


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
class PublisherUpdateView(ObjectUpdateMixin, UpdateView):
    model = Publisher
    form_class = PublisherForm
    template_name = 'publisher/update_publisher.html'
    pk_url_kwarg = 'publisher_id'
    success_url = reverse_lazy('publishers')


@method_decorator(login_required, name='dispatch')
class PublisherListView(ListView):
    model = Publisher
    template_name = 'publisher/publishers.html'
    context_object_name = 'publishers'


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/update_category.html'
    success_url = reverse_lazy('categories')


@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'category/categories.html'
    context_object_name = 'categories'


@method_decorator(login_required, name='dispatch')
class CategoryDetailView(ObjectDetailMixin, DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'
    pk_url_kwarg = 'category_id'


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
class CategoryDeleteView(ObjectDeleteMixin, DeleteView):
    model = Category
    template_name = 'category/delete_category_confirmation.html'
    success_url = reverse_lazy('categories')
    pk_url_kwarg = 'category_id'


@method_decorator(user_passes_test(user_is_manager), name='dispatch')
class CategoryUpdateView(ObjectUpdateMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/update_category.html'
    pk_url_kwarg = 'category_id'
    success_url = reverse_lazy('categories')


@method_decorator(user_passes_test(user_is_admin), name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'user/user_detail.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'


@method_decorator(user_passes_test(user_is_admin), name='dispatch')
class UserDeleteView(ObjectDeleteMixin, DeleteView):
    model = User
    template_name = 'user/delete_user.html'
    success_url = reverse_lazy('users')
    pk_url_kwarg = 'user_id'


@method_decorator(user_passes_test(user_is_admin), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = SignUpForm
    template_name = 'user/update_user.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('users')


@method_decorator(user_passes_test(user_is_admin), name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'user/users.html'
    context_object_name = 'users'


def set_admin_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    admin_group, _ = Group.objects.get_or_create(name='admin')
    user.groups.add(admin_group)
    return redirect(reverse('user_detail', kwargs={'user_id': user_id}))


def set_manager_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    manager_group, _ = Group.objects.get_or_create(name='manager')
    user.groups.add(manager_group)
    return redirect(reverse('user_detail', kwargs={'user_id': user_id}))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/logout/')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful sign-up
    else:
        form = SignUpForm()
    return render(request, 'registration/sign_up.html', {'form': form})