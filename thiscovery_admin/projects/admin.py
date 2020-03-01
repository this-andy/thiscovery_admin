import django.contrib.admin as admin
from django.contrib.auth.models import Group, User as DjangoUser
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from .models import Project, TaskType, ProjectTask, UserTask, UserProject, ExternalSystem, UserExternalAccount, User, UserGroup, \
    UserGroupMembership, ProjectGroupVisibility, ProjectTaskGroupVisibility


class MyAdminSite(admin.AdminSite):
    site_header = 'Thiscovery administration'
    site_title = 'Thiscovery site admin'


class ProjectTaskInline(admin.TabularInline):
    model = ProjectTask
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'status',
        'visibility',
        'number_of_tasks',
        'visible_to_user_groups',
        'testing_group',
    ]
    list_filter = [
        'status',
        'visibility',
        ('testing_group', admin.RelatedOnlyFieldListFilter),
    ]
    inlines = [
        ProjectTaskInline,
    ]


admin_site = MyAdminSite(name="myadmin")

admin_site.register(Group, GroupAdmin)
admin_site.register(DjangoUser, UserAdmin)
admin_site.register(Project, ProjectAdmin)
admin_site.register(TaskType)
admin_site.register(ProjectTask)
admin_site.register(UserProject)
admin_site.register(UserTask)
admin_site.register(ExternalSystem)
admin_site.register(UserExternalAccount)
admin_site.register(User)
admin_site.register(UserGroup)
admin_site.register(UserGroupMembership)
admin_site.register(ProjectGroupVisibility)
admin_site.register(ProjectTaskGroupVisibility)
