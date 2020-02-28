from django.contrib.admin import AdminSite

from .models import Project, TaskType, ProjectTask, UserTask, UserProject, ExternalSystem, UserExternalAccount, User, UserGroup, \
    UserGroupMembership, ProjectGroupVisibility, ProjectTaskGroupVisibility


class MyAdminSite(AdminSite):
    site_header = 'Thiscovery administration'
    site_title = 'Thiscovery site admin'


admin_site = MyAdminSite(name="myadmin")


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
