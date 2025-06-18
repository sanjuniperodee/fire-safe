from django import forms
from django.contrib import admin
from objects.models.document import Document, OrganizationType

from objects.models import (
    Building, BuildingCoordinates, Complaint,
    Document, DocumentComment, DocumentKey,
    DocumentKeyFile, DocumentHistory, EvacAddress,
    SubBuilding
)
from objects.models import (
    BuildingRemark,
    DocumentRemark,
)
from objects.models import (
    BuildingImage, SubBuildingImage,
    EscapeLadderImage,
)


@admin.register(BuildingRemark)
class BuildingRemarkAdmin(admin.ModelAdmin):
    list_display = ('building', 'inspector', 'content_preview', 'created_at',)  # 'updated_at'
    list_filter = ('building', 'inspector', 'created_at',)  # 'updated_at'
    search_fields = ('building__organization_name', 'inspector__last_name', 'inspector__first_name', 'content')
    ordering = ('-created_at',)
    list_display_links = ('content_preview',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Примечание'


class BuildingRemarkInline(admin.TabularInline):
    model = BuildingRemark
    extra = 0
    min_num = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'author', 'inspector', 'status', 'expiration_date', 'chat_room_id')
    list_filter = ('status', 'expiration_date')
    search_fields = ('unique_id', 'author__phone', 'inspector__phone')
    readonly_fields = ('unique_id', 'chat_room_id')
    ordering = ('-expiration_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(inspector=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.inspector == request.user


@admin.register(DocumentComment)
class DocumentCommentAdmin(admin.ModelAdmin):
    list_display = (
        'body',
        'document_key',
        'building',
        'updated_at'
    )
    list_filter = (
        'document_key',
        # 'building'
    )
    search_fields = (
        'document_key',
        'building',
    )
    ordering = ('-id',)
    list_display_links = ('body',)


class DocumentKeyFileInline(admin.TabularInline):
    model = DocumentKeyFile
    extra = 0
    min_num = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class DocumentCommentInline(admin.TabularInline):
    model = DocumentComment
    extra = 0
    min_num = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


@admin.register(DocumentRemark)
class DocumentRemarkAdmin(admin.ModelAdmin):
    list_display = ('document_key', 'content_preview', 'created_at') # 'inspector',
    list_filter = ('document_key', 'created_at') # 'inspector',
    search_fields = ('document_key__name', 'inspector__first_name', 'content') # 'inspector__last_name',
    ordering = ('-created_at',)
    list_display_links = ('content_preview',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Примечание'


class DocumentRemarkInline(admin.TabularInline):
    model = DocumentRemark
    extra = 0
    min_num = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class DocumentKeyFileAdmin(admin.ModelAdmin):
    # inlines = [DocumentRemarkInline]
    list_display = ('name', 'document_key', 'building')
    list_filter = ('document_key', 'building')
    search_fields = ('name', 'document_key__title', 'building__organization_name')


# Image inlines
class BuildingImageInline(admin.TabularInline):
    model = BuildingImage
    extra = 1

class SubBuildingImageInline(admin.TabularInline):
    model = SubBuildingImage
    extra = 1

class EscapeLadderImageInline(admin.TabularInline):
    model = EscapeLadderImage
    extra = 1

class BuildingCoordinateInline(admin.StackedInline):  # Changed from TabularInline to StackedInline for better layout
    model = BuildingCoordinates
    can_delete = True
    max_num = 1  # Ensure only one coordinate set can be added
    min_num = 0  # Make it optional
    extra = 1    # Show one empty form when no coordinates exist

@admin.register(BuildingCoordinates)
class BuildingCoordinatesAdmin(admin.ModelAdmin):
    list_display = ('building', 'lat', 'lng')
    search_fields = ('building__organization_name', 'lat', 'lng')
    raw_id_fields = ('building',)

    def has_add_permission(self, request):
        # Check if there are any buildings without coordinates
        buildings_without_coordinates = Building.objects.filter(coordinates__isnull=True).exists()
        return buildings_without_coordinates


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    inlines = [
        EscapeLadderImageInline,
        BuildingCoordinateInline,
        DocumentCommentInline,
        DocumentKeyFileInline,
        BuildingRemarkInline,
        BuildingImageInline,
    ]

    list_display = (
        'organization_name_full',
        'address',
        'owner',
        'inspector',
        'rating',
        'escape_ladder',
        'has_coordinates',
        'updated_at'
    )
    list_filter = (
        'organization_type',
        'rating',
        'owner',
        'inspector',
        'escape_ladder',
        'updated_at'
    )
    search_fields = (
        'organization_name',
        'address',
        'owner',
        'inspector'
    )
    ordering = ('-id',)
    #list_display_links = ('organization_name_full',)

    fieldsets = (
        ('Организационная информация', {
            'fields': (
                'organization_type',
                'organization_sub_type',
                'organization_characteristics',
                'organization_optional_type',
                'organization_name',
                #'full_name',
            ),
            'classes': ('wide',)
        }),
        ('Личные данные', {
            'fields': (
                'iin',
                'address',
            ),
            'classes': ('wide',)
        }),
        ('Ответственные лица', {
            'fields': (
                'owner',
                'inspector',
            ),
            'classes': ('wide',)
        }),
        ('Оценка и безопасность', {
            'fields': (
                'rating',
                'escape_ladder',
            ),
            'classes': ('wide',)
        }),
        ('Документация', {
            'fields': (
                'documents',
            ),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Координаты')
    def has_coordinates(self, obj):
        return bool(hasattr(obj, 'coordinates'))

    has_coordinates.boolean = True

    # @admin.display(description='Название организации')
    # def organization_name_full(self, obj):
    #     return '{display_value} {value}'.format(
    #         value=obj.organization_name,
    #         display_value=obj.get_organization_type_display()
    #     )
    @admin.display(description='Название организации')
    def organization_name_full(self, obj):
        return '{display_value} {value}'.format(
            value=obj.organization_name or '',
            display_value=obj.organization_type or '',
        )


class SubBuildingAdminForm(forms.ModelForm):
    class Meta:
        model = SubBuilding
        fields = '__all__'


@admin.register(SubBuilding)
class SubBuildingAdmin(admin.ModelAdmin):
    inlines = [SubBuildingImageInline]

    list_display = (
        'building',
        'title',
        'subbuilding_type',
        'subbuilding_subtype',
        'subbuilding_optional_subtype_type',
        'floor_string',
        'building_height',
        'area',
        'volume',
        'emergency_lighting',
    )
    list_filter = (
        'building',
        'subbuilding_type',
        'emergency_lighting',
        'fire_resistance_rating',
    )
    search_fields = (
        'title',
        'building__organization_name',
        'functional_purpose',
    )

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'building', 'subbuilding_type', 'subbuilding_subtype', 'subbuilding_optional_subtype_type', 'subbuilding_characteristics',
                'title', 'functional_purpose', 'rating'
            ),
            'classes': ('wide',)
        }),
        ('Даты', {
            'fields': (
                'date_commissioning', 'change_functional_purpose_date',
                'year_construction_reconstruction'
            )
        }),
        ('Характеристики здания', {
            'fields': (
                'floor_number', 'total_floors', 'building_height',
                'area', 'volume', 'building_foundation'
            )
        }),
        ('Пожарная безопасность', {
            'fields': (
                'fire_resistance_rating', 'structural_po_class',
                'functional_po_class'
            )
        }),
        ('Материалы и конструкции', {
            'fields': (
                'external_walls_material',
                'inner_walls_material',
                'roof',
                'stairs_material',
                'stairs_type',
                'stairs_classification'
            ),
            'classes': ('wide',)
        }),
        ('Инженерные системы', {
            'fields': (
                'lighting',
                'emergency_lighting',
                'ventilation',
                'heating',
                'security'
            )
        }),
    )

    ordering = ('id',)
    list_display_links = ('title',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        fields_with_choices = [
            'external_walls_material', 'inner_walls_material', 'roof',
            'stairs_material', 'stairs_type', 'lighting', 'ventilation',
            'heating', 'security'
        ]
        for field in fields_with_choices:
            if field in form.base_fields:
                form.base_fields[field].help_text = (
                    'Для изменения списка значений перейдите в раздел '
                    f'администрирования: <a href="/admin/specifications/'
                    f'{field.lower()}choice/">Управление значениями</a>'
                )
        return form

    @admin.display(description='Этажность')
    def floor_string(self, obj):
        return f'{obj.floor_number} из {obj.total_floors}'

@admin.register(DocumentKey)
class DocumentKeyAdmin(admin.ModelAdmin):
    list_display = ('title', 'document')
    # Показываем в таблице колонки "title" и "document"

    list_filter = ('document', 'supported_organization_types')
    # Добавляем фильтр по полю "document"
    # Если нужно фильтровать по "title", указываем его здесь,
    # но обычно для названий используют поиск (search_fields)

    search_fields = ('title',)
    # Позволяет искать по названию (title) в админке

    ordering = ('-id',)


admin.site.register(Document)
admin.site.register(OrganizationType)
admin.site.register(DocumentHistory)
admin.site.register(EvacAddress)
# admin.site.register(DocumentKeyFile)
admin.site.register(DocumentKeyFile, DocumentKeyFileAdmin)
#admin.site.register(BuildingCoordinates)
