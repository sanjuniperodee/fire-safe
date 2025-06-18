from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from auths import models


class UserRoleInline(admin.TabularInline):
    model = models.UserRole
    extra = 1


class UserCategoryInline(admin.TabularInline):
    model = models.UserCategory
    extra = 1
    fields = ('category', 'role')
    autocomplete_fields = ['category']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = models.Category.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EducationInline(admin.StackedInline):
    model = models.Education
    extra = 0
    readonly_fields = ('college_name', 'year_start', 'year_end', 'degree', 'media')


class ExperienceInline(admin.StackedInline):
    model = models.Experience
    extra = 0
    readonly_fields = ('company_name', 'year_start', 'year_end', 'media')


class AchievementInline(admin.TabularInline):
    model = models.Achievement
    extra = 0
    readonly_fields = ('certificate_name', 'year_received', 'media')


class OtherAchievementInline(admin.TabularInline):
    model = models.OtherAchievement
    extra = 0
    readonly_fields = ('name', 'year_start', 'year_end', 'media')


class CustomUserAdmin(UserAdmin):
    inlines = (
        UserRoleInline, UserCategoryInline, EducationInline, ExperienceInline, AchievementInline,
        OtherAchievementInline)
    """Регистрация модели CustomUser в админ панели"""

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'middle_name', 'birthdate', 'iin')}),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

    list_display = ('phone', 'last_name', 'first_name', 'middle_name',)

    list_filter = ('phone', 'last_name', 'first_name', 'middle_name',)

    search_fields = ('phone', 'last_name', 'first_name', 'middle_name',)

    filter_horizontal = ()

    ordering = ('id',)

    def get_roles(self, obj):
        return ", ".join([user_role.role.role for user_role in obj.user_roles.all()])

    get_roles.short_description = 'Roles'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        common_fields = (
            (None, {'fields': ('phone', 'password')}),
            ('Personal info', {'fields': ('last_name', 'first_name', 'middle_name', 'email', 'birthdate', 'iin')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login',)}),
        )

        if obj.is_provider:
            provider_fields = (
                ('Provider info', {'fields': ('about_myself', 'main_organization_type', 'organization_type',
                                              'organization_sub_type', 'organization_name', 'bin_field')}),
            )
            return common_fields + provider_fields
        elif obj.is_inspector:
            inspector_fields = (
                ('Инфо Инспектора', {'fields': ('rank', 'position', 'certificate_number')}),
                ('Регион юрисдикции', {'fields': ('inspector_jurisdiction_city', 'inspector_jurisdiction_district')}),
            )
            return common_fields + inspector_fields
        elif obj.is_object_owner:
            object_owner_fields = (
                ('Инфо Собственника(как гражданина)', {'fields': ('actual_residence_address', 'residence_address')}),
            )
            return common_fields + object_owner_fields
        elif obj.is_citizen:
            citizen_fields = (
                ('Инфо Гражданина', {'fields': ('actual_residence_address', 'residence_address')}),
            )
            return common_fields + citizen_fields

        return common_fields

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []

        inline_instances = [UserRoleInline(self.model, self.admin_site)]

        if obj.is_provider:
            inline_instances.extend([
                UserCategoryInline(self.model, self.admin_site),
                EducationInline(self.model, self.admin_site),
                ExperienceInline(self.model, self.admin_site),
                AchievementInline(self.model, self.admin_site),
                OtherAchievementInline(self.model, self.admin_site)
            ])
        elif obj.is_inspector:
            pass
        elif obj.is_object_owner:
            pass

        return inline_instances

    add_fieldsets = (
        ("User Details",
         {'fields': (
             'phone', 'last_name', 'first_name', 'middle_name', 'email', 'birthdate', 'iin', 'password1',
             'password2')}),
    )


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'status')
    list_filter = ('role', 'status')
    search_fields = ('user__phone', 'user__last_name', 'user__first_name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ['name']
    # ordering = ['name']


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.CustomUserRole)
admin.site.register(models.UserRole, UserRoleAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.unregister(Group)
