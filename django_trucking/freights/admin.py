from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Type, Freight, Details, Worker, Rating, RatingStar, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id",  "name", "url")
    list_display_links = ("name",)

class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")

class DetailsInline(admin.TabularInline):
    model = Details
    extra = 1
   
    
@admin.register(Freight)
class FreightAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [ DetailsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premiere"),)
        }),
        ("Workers", {
            "classes": ("collapse",),
            "fields": (("workers", "directors", "types", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "freight", "id")
    readonly_fields = ("name", "email")
    

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """Типы"""
    list_display = ("name", "url")


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    """Водители"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')
        get_image.short_description = "Изображение" 

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("freight", "star", "ip")


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    """Детали из фильма"""
    list_display = ("title", "freight")


admin.site.register(RatingStar)
admin.site.site_title = "Грузоперевозки"
admin.site.site_header = "Грузоперевозки"