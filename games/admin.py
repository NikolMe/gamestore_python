from django.contrib import admin
from games.models import Publisher, Category, Game


class GameInstanceInline(admin.TabularInline):
    model = Game


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    inlines = [GameInstanceInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class Game(admin.ModelAdmin):
    list_filter = ['categories', 'publisher']
    pass
