import django.contrib.admin as admin
import nested_admin
from django.contrib.auth.models import Group, User as DjangoUser
from django.contrib.auth.admin import GroupAdmin, UserAdmin as DjangoUserAdmin

from .models import Project, TaskType, ProjectTask, UserTask, UserProject, ExternalSystem, UserExternalAccount, User, UserGroup, \
    UserGroupMembership, ProjectGroupVisibility, ProjectTaskGroupVisibility


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
        'short_name',
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


class UserTaskAdmin(admin.ModelAdmin):
    list_display = [
        'short_name',
        'status',
        'project_task',
    ]
    list_filter = [
        'project_task',
        'status',
        # 'signup_status',
        # 'visibility',
        # 'external_system',
        # ('testing_group', admin.RelatedOnlyFieldListFilter),
    ]
    pass


class UserGroupAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        UserGroupMembershipInline,
        ProjectNestedReadOnlyInline,
    ]
    list_display = [
        'short_name',
        'url_code',
        'number_of_users',
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
