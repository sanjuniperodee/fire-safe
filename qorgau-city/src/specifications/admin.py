from django.contrib import admin
from specifications import StairsClassificationType

from .models import (
    ExternalWallMaterialChoice,
    InnerWallMaterialChoice,
    RoofChoice,
    StairsMaterialChoice,
    StairsTypeChoice,
    LightingTypeChoice,
    VentilationTypeChoice,
    HeatingChoice,
    SecurityChoice,
    StairsClassificationChoice,
)


class BaseChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ExternalWallMaterialChoice)
class ExternalWallMaterialChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(InnerWallMaterialChoice)
class InnerWallMaterialChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(RoofChoice)
class RoofChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(StairsMaterialChoice)
class StairsMaterialChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(StairsTypeChoice)
class StairsTypeChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(LightingTypeChoice)
class LightingTypeChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(VentilationTypeChoice)
class VentilationTypeChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(HeatingChoice)
class HeatingChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(SecurityChoice)
class SecurityChoiceAdmin(BaseChoiceAdmin):
    pass


@admin.register(StairsClassificationChoice)
class StairsClassificationChoiceAdmin(admin.ModelAdmin):
    # list_display = ('name', 'get_description')
    readonly_fields = ('description',)

    def get_description(self, obj):
        return obj.description

    get_description.short_description = 'Описание'

    def has_add_permission(self, request):
        # Prevent adding new classifications if all choices are already created
        count = StairsClassificationChoice.objects.count()
        return count < len(StairsClassificationType.choices)