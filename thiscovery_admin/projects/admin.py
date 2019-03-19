from django.contrib import admin

from .models import Project, TaskType, ProjectTask, UserTask, UserProject, ExternalSystem, UserExternalAccount, User, UserGroup, \
    UserGroupMembership, ProjectGroupVisibility, ProjectTaskGroupVisibility

admin.site.register(Project)
admin.site.register(TaskType)
admin.site.register(ProjectTask)
admin.site.register(UserProject)
admin.site.register(UserTask)
admin.site.register(ExternalSystem)
admin.site.register(UserExternalAccount)
admin.site.register(User)
admin.site.register(UserGroup)
admin.site.register(UserGroupMembership)
admin.site.register(ProjectGroupVisibility)
admin.site.register(ProjectTaskGroupVisibility)
