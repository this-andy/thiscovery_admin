from django.db import migrations

trigger_function_name = 'validate_ProjectTaskGroupVisibility_demo_status'


create_func_sql = f"""
CREATE OR REPLACE FUNCTION {trigger_function_name}() RETURNS trigger AS ${trigger_function_name}$
    DECLARE
        project_demo_status     boolean;
        group_demo_status       boolean;
    BEGIN
        SELECT p.demo INTO project_demo_status 
            FROM public.projects_project p
            JOIN public.projects_projecttask pt ON pt.project_id = p.id 
            WHERE pt.id = NEW.project_task_id;
        SELECT g.demo INTO group_demo_status FROM public.projects_usergroup g WHERE g.id = NEW.user_group_id;
        IF (project_demo_status = group_demo_status) THEN
            RETURN NEW;
        ELSE 
            RAISE EXCEPTION 'Demo status of project and group do not match (task: %, group: %)', 
            project_demo_status, group_demo_status; 
        END IF;
    END;
${trigger_function_name}$ LANGUAGE plpgsql;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0061_project_demo_testgroup_trigger'),
    ]

    operations = [
        migrations.RunSQL(
            sql=create_func_sql,
            reverse_sql=f'DROP FUNCTION IF EXISTS {trigger_function_name}();',
        ),
        migrations.RunSQL(
            sql=f'CREATE TRIGGER {trigger_function_name} '
                f'BEFORE INSERT OR UPDATE ON public.projects_projecttaskgroupvisibility '
                f'FOR EACH ROW EXECUTE PROCEDURE {trigger_function_name}();',
            reverse_sql=f'DROP TRIGGER IF EXISTS {trigger_function_name} ON '
                        'public.projects_projecttaskgroupvisibility;'
        ),
    ]
