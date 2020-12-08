from django.db import migrations


trigger_function_name = 'validate_UserGroup_demo_status'


create_func_sql = f"""
CREATE OR REPLACE FUNCTION {trigger_function_name}() RETURNS trigger AS ${trigger_function_name}$
    DECLARE
        project_row     public.projects_project%ROWTYPE;
    BEGIN
        FOR project_row IN 
            SELECT 
                p.* 
            FROM 
                public.projects_project p
            JOIN 
                public.projects_projectgroupvisibility pgv ON p.id = pgv.project_id 
            WHERE pgv.user_group_id = NEW.id
        LOOP
            IF (project_row.demo != NEW.demo) THEN
                RAISE EXCEPTION 'Demo status of this user group clashes with one of its associated projects (%)',
                project_row.short_name; 
            END IF;    
        END LOOP;
        RETURN NEW;
    END;
${trigger_function_name}$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0055_demo_status_trigger'),
    ]

    operations = [
        migrations.RunSQL(
            sql=create_func_sql,
            reverse_sql=f'DROP FUNCTION IF EXISTS {trigger_function_name}();',
        ),
        migrations.RunSQL(
            sql=f'CREATE TRIGGER {trigger_function_name} '
                f'BEFORE INSERT OR UPDATE ON public.projects_usergroup '
                f'FOR EACH ROW EXECUTE PROCEDURE {trigger_function_name}();',
            reverse_sql=f'DROP TRIGGER IF EXISTS {trigger_function_name} ON '
                        f'public.projects_usergroup;'
        ),
    ]
