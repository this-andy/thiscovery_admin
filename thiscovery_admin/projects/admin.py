import csv
import django.contrib.admin as admin
import nested_admin
from django.contrib.auth.models import Group, User as DjangoUser
from django.contrib.auth.admin import GroupAdmin, UserAdmin as DjangoUserAdmin
from django.db.models import F
from django.http import HttpResponse

from .models import Project, TaskType, ProjectTask, UserTask, UserProject, ExternalSystem, UserExternalAccount, User, UserGroup, \
    UserGroupMembership, ProjectGroupVisibility, ProjectTaskGroupVisibility, AnonId


class ExportCsvMixin:
    """
    https://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
    """
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export selected"


class MyAdminSite(admin.AdminSite):
    site_header = 'Thiscovery administration'
    site_title = 'Thiscovery site admin'


# region Inlines
class ReadOnlyMixin:
    """
    Use this mixin to make any Inline class readonly.

    Usage example:
        class ProjectTaskNestedReadOnlyInline(ReadOnlyMixin, nested_admin.NestedTabularInline):
            ...
    """
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProjectGroupVisibilityInLine(admin.StackedInline):
    model = ProjectGroupVisibility
    extra = 0
    verbose_name = 'User group'
    verbose_name_plural = 'User groups'
    classes = ['collapse']


class ProjectTaskInline(admin.StackedInline):
    model = ProjectTask
    extra = 0
    classes = ['collapse']


class ProjectTaskNestedReadOnlyInline(ReadOnlyMixin, nested_admin.NestedTabularInline):
    model = ProjectTask
    fields = [
        'description',
        'task_type',
        'status',
        'signup_status',
        'visibility',
        'external_system',
    ]
    classes = ['collapse']


class ProjectNestedReadOnlyInline(ReadOnlyMixin, nested_admin.NestedTabularInline):
    model = Project
    fields = [
        'name',
        'visibility',
        'status'
    ]
    inlines = [ProjectTaskNestedReadOnlyInline]
    classes = ['collapse']


class ProjectTaskGroupVisibilityInline(admin.StackedInline):
    model = ProjectTaskGroupVisibility
    extra = 0
    verbose_name = 'User group'
    verbose_name_plural = 'User groups'
    classes = ['collapse']


class UserGroupMembershipInline(nested_admin.NestedTabularInline):
    model = UserGroupMembership
    extra = 0
    fields = [
        'user',
        'user_name',
        'user_email',
    ]
    readonly_fields = [
        'user_name',
        'user_email',
    ]
    autocomplete_fields = ['user']
    ordering = ['user__last_name']
    verbose_name = 'Member'
    verbose_name_plural = 'Members'
    classes = ['collapse']
# endregion


# region ModelAdmins
class UserAdmin(admin.ModelAdmin):
    search_fields = [
        'id',
        'email',
        'first_name',
        'last_name',
    ]
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
    ]


class ProjectAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'short_name',
        'visibility',
        # 'website_highlight',
        'testing_group',
        'status',
        'user_groups',
    ]
    readonly_fields = [
        'user_groups',
    ]
    inlines = [
        ProjectTaskInline,
        ProjectGroupVisibilityInLine,
    ]
    list_display = [
        'id',
        'name',
        'status',
        'visibility',
        'number_of_tasks',
        'user_groups',
        'testing_group',
    ]
    list_filter = [
        'status',
        'visibility',
        ('testing_group', admin.RelatedOnlyFieldListFilter),
    ]


class ProjectTaskAdmin(admin.ModelAdmin):

    def export_user_group_url_codes_action(self, request, queryset):
        """
        Exports selected Project Tasks to a csv file, including the url_code of each user group
        """
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(
            [
                'user_group_url_code',
                *field_names
            ]
        )
        for obj in queryset:
            writer.writerow(
                [
                    obj.user_group_codes,
                    *[getattr(obj, field) for field in field_names]
                ]
            )
        return response

    export_user_group_url_codes_action.short_description = "Export url_codes for selected"

    actions = [
        'export_user_group_url_codes_action',
    ]
    exclude = [
        'earliest_start_date',
        'closing_date',
        'website_highlight',
    ]
    readonly_fields = [
        'progress_info',
    ]
    inlines = [
        ProjectTaskGroupVisibilityInline,
    ]
    list_display = [
        'id',
        'short_name',
        'user_group_codes',
        'task_type',
        'status',
        'signup_status',
        'visibility',
        'user_groups',
        'testing_group',
        'external_system',
        'project',
        'project_status',
        'project_visibility',
    ]
    list_filter = [
        'project',
        'task_type',
        'status',
        'signup_status',
        'visibility',
        'external_system',
        ('testing_group', admin.RelatedOnlyFieldListFilter),
    ]


class UserTaskAdmin(admin.ModelAdmin, ExportCsvMixin):

    def export_user_ids_action(self, request, queryset):
        """
        Exports selected User Tasks to a csv file, including user_id and anon_project_specific_user_id
        """
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(
            [
                'user_id',
                'anon_project_specific_user_id',
                *field_names
            ]
        )
        for obj in queryset:
            writer.writerow(
                [
                    obj.user_project.user.id,
                    obj.user_project.anon_project_specific_user_id,
                    *[getattr(obj, field) for field in field_names]
                ]
            )
        return response

    export_user_ids_action.short_description = "Export user_ids for Selected"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _user_name=F("user_project__user__first_name"),
        )
        return queryset

    def sortable_short_name(self, obj):
        return obj.short_name

    sortable_short_name.admin_order_field = '_user_name'

    list_display = [
        'id',
        'sortable_short_name',
        'status',
        'project_task',
    ]
    list_display_links = [
        'sortable_short_name',
    ]
    list_filter = [
        'project_task',
        'status',
    ]
    search_fields = [
        'id',
        'user_project__user__email',
        'user_project__user__first_name',
        'user_project__user__last_name',
    ]
    actions = [
        'export_as_csv',
        'export_user_ids_action',
    ]

    raw_id_fields = [
        'user_project',
        'project_task',
    ]
    readonly_fields = [
        'user_project',
        'project_task',
    ]


class UserGroupAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        UserGroupMembershipInline,
        ProjectNestedReadOnlyInline,
    ]
    list_display = [
        'id',
        'short_name',
        'url_code',
        'number_of_users',
    ]


class AnonIdAdmin(admin.ModelAdmin):
    list_display = [
        'anon_user_task_id',
        'anon_project_specific_user_id',
        'user_id',
        'email',
        'project_id',
        'project_name',
        'user_task_id',
        'project_task_id',
        'project_task_description',
    ]
    list_display_links = None
    search_fields = [
        'anon_user_task_id',
        'anon_project_specific_user_id',
        'user_id',
        'email',
        'user_task_id',
        'project_task_id',
    ]
    list_filter = [
        'project_name',
        'project_task_description',
    ]
# endregion


admin_site = MyAdminSite(name="myadmin")

admin_site.register(Group, GroupAdmin)
admin_site.register(DjangoUser, DjangoUserAdmin)
admin_site.register(Project, ProjectAdmin)
admin_site.register(TaskType)
admin_site.register(ProjectTask, ProjectTaskAdmin)
admin_site.register(UserProject)
admin_site.register(UserTask, UserTaskAdmin)
admin_site.register(ExternalSystem)
admin_site.register(UserExternalAccount)
admin_site.register(User, UserAdmin)
admin_site.register(UserGroup, UserGroupAdmin)
admin_site.register(UserGroupMembership)
admin_site.register(ProjectGroupVisibility)
admin_site.register(ProjectTaskGroupVisibility)
admin_site.register(AnonId, AnonIdAdmin)
