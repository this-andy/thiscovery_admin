from django.contrib.postgres.fields import JSONField
from django.db import models
import uuid
from ..models import TimeStampedModel


def get_display_name(self):
    short_name_length = self.__class__._meta.get_field('short_name').max_length
    if self.short_name == '':
        if len(self.name) > short_name_length:
            return self.name[:short_name_length - 2] + '...'
        else:
            return self.name
    else:
        return self.short_name + '{' + str(self.id) + '}'


class User(TimeStampedModel):
    email = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    country_code = models.CharField(max_length=6, blank=True, null=True)
    auth0_id = models.CharField(max_length=50, blank=True, null=True)
    crm_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        # return self.email + ' (' + self.full_name + ') {' + str(self.id) + '}'
        return f"{self.email} ({self.full_name})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserGroup(TimeStampedModel):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20, blank=True)
    url_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        # return get_display_name(self)
        return self.short_name

    def number_of_users(self):
        return len([User.objects.get(id=x.user_id) for x in UserGroupMembership.objects.filter(user_group=self)])


class ExternalSystem(TimeStampedModel):
    DISPLAY_METHOD_CHOICES = (
        ('redirect', 'Redirect'),
        ('iframe', 'iFrame'),
    )

    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20, blank=True)
    external_user_id_type = models.CharField(max_length=10, blank=True, null=True)  # uuid, integer, string
    display_method = models.CharField(max_length=12, choices=DISPLAY_METHOD_CHOICES, blank=True, null=True)

    def __str__(self):
        # return get_display_name(self)
        return self.short_name

class Project(TimeStampedModel):
    STATUS_CHOICES = (
        ('planned', 'Planned'),
        ('testing', 'Testing'),
        ('active', 'Active'),
        ('complete', 'Complete')
    )
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20, blank=True)
    visibility = models.CharField(max_length=12, choices=VISIBILITY_CHOICES)
    website_highlight = models.BooleanField(default=False)
    testing_group = models.ForeignKey(UserGroup, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)

    def __str__(self):
        # return get_display_name(self) + ' (' + str(self.status) + ')'
        return self.short_name

    def number_of_tasks(self):
        return ProjectTask.objects.filter(project=self.id).count()

    def user_groups(self):
        return ", ".join([UserGroup.objects.get(id=x.user_group_id).short_name for x in ProjectGroupVisibility.objects.filter(project=self.id)])


class TaskType(TimeStampedModel):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20, blank=True)

    def __str__(self):
        # return get_display_name(self)
        return self.short_name


class ProjectTask(TimeStampedModel):
    STATUS_CHOICES = (
        ('planned', 'Planned'),
        ('testing', 'Testing'),
        ('active', 'Active'),
        ('complete', 'Complete')
    )
    SIGNUP_STATUS_CHOICES = (
        ('not-open', 'Not yet open'),
        ('open', 'Open'),
        ('closed', 'Closed')
    )
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, default='')
    earliest_start_date = models.DateTimeField(null=True, blank=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    signup_status = models.CharField(max_length=12, choices=SIGNUP_STATUS_CHOICES)
    visibility = models.CharField(max_length=12, choices=VISIBILITY_CHOICES)
    website_highlight = models.BooleanField(default=False)
    testing_group = models.ForeignKey(UserGroup, null=True, blank=True, on_delete=models.SET_NULL)
    external_system = models.ForeignKey(ExternalSystem, null=True, blank=True, on_delete=models.SET_NULL)
    external_task_id = models.CharField(max_length=50, null=True, blank=True)
    base_url = models.CharField(max_length=100, null=True, blank=True)
    user_specific_url = models.BooleanField(default=False)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    progress_info = JSONField(null=True, blank=True)
    progress_info_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def short_name(self):
        if self.description == '':
            display_name = '-'.join([self.project.short_name, self.task_type.short_name])
        else:
            display_name = self.description
        return display_name

    def __str__(self):
        return self.short_name + ' (' + str(self.status) + ') {' + str(self.id) + '}'

    def project_visibility(self):
        return self.project.visibility

    def project_status(self):
        return self.project.status

    def user_groups(self):
        return ", ".join([UserGroup.objects.get(id=x.user_group_id).short_name for x in ProjectTaskGroupVisibility.objects.filter(project_task=self.id)])


class UserProject(TimeStampedModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('complete', 'Complete'),
        ('withdrawn', 'Withdrawn')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, blank=True, null=True, choices=STATUS_CHOICES)
    ext_user_project_id = models.UUIDField(blank=True, null=True)

    @property
    def short_name(self):
        return '-'.join([self.user.full_name, self.project.short_name])

    def __str__(self):
        return self.short_name + ' {' + str(self.id) + '}'


class UserTask(TimeStampedModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('complete', 'Complete'),
        ('withdrawn', 'Withdrawn')
    )
    # user = models.ForeignKey(settings.AUTH_USER_MODEL)
    user_project = models.ForeignKey(UserProject, on_delete=models.CASCADE)
    # task = models.ForeignKey(Task)
    project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, blank=True, null=True, choices=STATUS_CHOICES)
    consented = models.DateTimeField(null=True)
    progress_info = JSONField(null=True, blank=True)
    ext_user_task_id = models.UUIDField(blank=True, null=True)
    url = models.CharField(max_length=500, null=True, blank=True)

    @property
    def short_name(self):
        return '-'.join([self.user_project.short_name, self.project_task.short_name])

    def __str__(self):
        return self.short_name + ' {' + str(self.id) + '}'


class UserExternalAccount(TimeStampedModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed')
    )
    external_system = models.ForeignKey(ExternalSystem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    external_user_id = models.CharField(max_length=50, null=True, blank=True, choices=STATUS_CHOICES)
    status = models.CharField(max_length=12, blank=True, null=True)

    @property
    def short_name(self):
        return '-'.join([self.external_system.short_name, self.user.full_name])

    def __str__(self):
        return self.short_name + ' {' + str(self.id) + '}'


class EntityUpdate(TimeStampedModel):
    entity_name = models.CharField(max_length=50)
    entity_id = models.UUIDField(editable=False)
    json_patch = models.CharField(max_length=2000, editable=False)
    json_reverse_patch = models.CharField(max_length=2000, editable=False)


class UserGroupMembership(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    @property
    def short_name(self):
        return '-'.join([self.user.full_name, self.user_group.short_name])

    @property
    def user_name(self):
        return self.user.full_name

    @property
    def user_email(self):
        return self.user.email

    def __str__(self):
        return self.short_name + ' {' + str(self.id) + '}'


class ProjectGroupVisibility(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    @property
    def short_name(self):
        return '-'.join([self.project.short_name, self.user_group.short_name])

    def __str__(self):
        return self.short_name + ' {' + str(self.id) + '}'

    class Meta:
        verbose_name_plural = "Project group visibilities"


class ProjectTaskGroupVisibility(TimeStampedModel):
    project_task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    @property
    def short_name(self):
        return '-'.join([self.project_task.short_name, self.user_group.short_name])

    def __str__(self):
        return self.short_name + ' {' + str(self.id) + '}'

    class Meta:
        verbose_name_plural = "Project task group visibilities"
