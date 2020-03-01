import django.contrib.admin as admin
from django.contrib.auth.models import Group, User as DjangoUser
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from .models import Project, TaskType, ProjectTask, UserTask, UserProject, ExternalSystem, UserExternalAccount, User, UserGroup, \
    UserGroupMembership, ProjectGroupVisibility, ProjectTaskGroupVisibility


class MyAdminSite(admin.AdminSite):
    site_header = 'Thiscovery administration'
    site_title = 'Thiscovery site admin'


class ProjectGroupVisibilityInLine(admin.StackedInline):
    model = ProjectGroupVisibility
    extra = 0


class ProjectTaskInline(admin.StackedInline):
    model = ProjectTask
    extra = 0


class ProjectTaskGroupVisibilityInLine(admin.StackedInline):
    model = ProjectTaskGroupVisibility
    extra = 0


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
        ProjectTaskGroupVisibilityInLine,
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


admin_site = MyAdminSite(name="myadmin")

admin_site.register(Group, GroupAdmin)
admin_site.register(DjangoUser, UserAdmin)
admin_site.register(Project, ProjectAdmin)
admin_site.register(TaskType)
admin_site.register(ProjectTask, ProjectTaskAdmin)
admin_site.register(UserProject)
admin_site.register(UserTask)
admin_site.register(ExternalSystem)
admin_site.register(UserExternalAccount)
admin_site.register(User)
admin_site.register(UserGroup)
admin_site.register(UserGroupMembership)
admin_site.register(ProjectGroupVisibility)
admin_site.register(ProjectTaskGroupVisibility)
