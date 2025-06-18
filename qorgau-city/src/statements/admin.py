from django.contrib import admin

from .models import (
    Statement,
    StatementMedia,
    StatementProvider,
    StatementCategory,
    StatementRequestForCompleted,
    StatementSuggestion,
)


class StatementMediaInline(admin.TabularInline):
    model = StatementMedia
    extra = 1


class StatementCategoryInline(admin.TabularInline):
    model = StatementCategory
    extra = 1


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'service_time', 'min_price', 'max_price', 'is_active', 'is_busy_by_provider')
    list_filter = ('is_active', 'service_time', 'is_busy_by_provider')
    search_fields = ('text', 'author__username', 'author__email')
    inlines = [StatementMediaInline, StatementCategoryInline]
    # readonly_fields = ('created_at',)
    """Создание модели Заявок(Заказов) в админ панели"""

    fieldsets = (
        (None, {
            'fields': ('author', 'text', 'service_time', 'location')
        }),
        ('Price Information', {
            'fields': ('min_price', 'max_price')
        }),
        ('Status', {
            'fields': ('is_active', 'is_busy_by_provider')
        }),
    )


@admin.register(StatementProvider)
class StatementProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'statement', 'provider', 'chat_room_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('statement__text', 'provider__username')
    readonly_fields = ('created_at',)


@admin.register(StatementSuggestion)
class StatementSuggestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'statement',
        'provider',
        'status',
        'chat_room_id',
        'archive_date',
        'created_at'
    )
    list_filter = (
        'status',
        'created_at',
        'archive_date'
    )
    search_fields = (
        'statement__text',
        'provider__username',
        'provider__email'
    )
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('statement', 'provider', 'chat_room_id')
        }),
        ('Status Information', {
            'fields': ('status', 'archive_date')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make created_at read-only"""
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_at',)
        return self.readonly_fields


@admin.register(StatementRequestForCompleted)
class StatementRequestForCompletedAdmin(admin.ModelAdmin):
    list_display = ('id', 'statement', 'provider', 'is_completed', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)