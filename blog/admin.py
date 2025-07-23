from django.contrib import admin
from .models import Post, Category, Comment, Message

# Register your models here.


class SearchByTitle(admin.SimpleListFilter):
    title = "جستجو بر اساس کلید پر تکرار"
    parameter_name = "title"

    def lookups(self, request, model_admin):
        return (
            ("c", "سی"),
            ("java", "جاوا"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains=self.value())


# کلاس‌های inline بهت این امکان رو می‌دن که مدل‌های مرتبط رو در همون صفحه‌ی ادمین یک مدل دیگه مدیریت کنی.
class CommentInLine(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("__str__", "title", "body", "show_image")
    list_filter = ("title", "created")
    list_editable = ("title",)
    search_fields = ("title",)
    inlines = [CommentInLine]  # در پایین هر کدوم کامنت نشون میده


admin.site.register(Message)
admin.site.register(Category)
admin.site.register(Comment)
