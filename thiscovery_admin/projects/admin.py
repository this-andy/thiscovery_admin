import django.contrib.admin as admin
from django.contrib.auth.models import Group, User as DjangoUser
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from .models import Project, TaskType, ProjectTask, UserTask, UserProject, ExternalSystem, UserExternalAccount, User, UserGroup, \
    UserGroupMembership, ProjectGroupVisibility, ProjectTaskGroupVisibility


class MyAdminSite(admin.AdminSite):
    site_header = 'Thiscovery administration'
    site_title = 'Thiscovery site admin'


admin_site = MyAdminSite(name="myadmin")

admin_site.register(Group, GroupAdmin)
admin_site.register(DjangoUser, UserAdmin)
admin_site.register(Project)
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
