"""
Ensures user group demo status constraint is respected if demo status of task is updated.
"""
from django.db import migrations


trigger_function_name = 'validate_ProjectTask_demo_status'


create_func_sql = f"""
CREATE OR REPLACE FUNCTION {trigger_function_name}() RETURNS trigger AS ${trigger_function_name}$
    DECLARE
        user_group_row     public.projects_usergroup%ROWTYPE;
        project_demo_status     boolean;
        testing_group_demo_status     boolean;
    BEGIN
        -- get project demo status
        SELECT p.demo INTO project_demo_status 
            FROM public.projects_project p
            JOIN public.projects_projecttask pt ON pt.project_id = p.id 
            WHERE pt.id = NEW.id;
        
        -- check testing_group demo status matches
        IF NEW.testing_group_id IS NOT NULL THEN 
            SELECT g.demo INTO testing_group_demo_status 
                FROM public.projects_usergroup g 
                WHERE g.id = NEW.testing_group_id;
            IF (project_demo_status != testing_group_demo_status) THEN 
                RAISE EXCEPTION 'Demo status of project this task belongs to and its testing group do not match (project: %, testing group: %)', 
                project_demo_status, testing_group_demo_status; 
            END IF;
        END IF;
            
        -- check each linked user group
        FOR user_group_row IN 
            SELECT 
                ug.* 
            FROM 
                public.projects_usergroup ug
            JOIN 
                public.projects_projecttaskgroupvisibility ptgv ON ug.id = ptgv.user_group_id 
            WHERE ptgv.project_task_id = NEW.id
        LOOP
            IF (user_group_row.demo != project_demo_status) THEN
                RAISE EXCEPTION 'Demo status of the project this task belongs to clashes with one of its user groups (%)',
                user_group_row.short_name; 
            END IF;    
        END LOOP;
        RETURN NEW;
    END;
${trigger_function_name}$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0062_task_demo_status_trigger'),
    ]

    operations = [
        migrations.RunSQL(
            sql=create_func_sql,
            reverse_sql=f'DROP FUNCTION IF EXISTS {trigger_function_name}();',
        ),
        migrations.RunSQL(
            sql=f'CREATE TRIGGER {trigger_function_name} '
                f'BEFORE INSERT OR UPDATE ON public.projects_projecttask '
                f'FOR EACH ROW EXECUTE PROCEDURE {trigger_function_name}();',
            reverse_sql=f'DROP TRIGGER IF EXISTS {trigger_function_name} ON '
                        f'public.projects_projecttask;'
        ),
    ]
