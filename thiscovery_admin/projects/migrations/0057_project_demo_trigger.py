from django.db import migrations


trigger_function_name = 'validate_Project_demo_status'


create_func_sql = f"""
CREATE OR REPLACE FUNCTION {trigger_function_name}() RETURNS trigger AS ${trigger_function_name}$
    DECLARE
        user_group_row     public.projects_usergroup%ROWTYPE;
    BEGIN
        FOR user_group_row IN 
            SELECT 
                ug.* 
            FROM 
                public.projects_usergroup ug
            JOIN 
                public.projects_projectgroupvisibility pgv ON ug.id = pgv.user_group_id 
            WHERE pgv.project_id = NEW.id
        LOOP
            IF (user_group_row.demo != NEW.demo) THEN
                RAISE EXCEPTION 'Demo status of this project clashes with one of its user groups (%)',
                user_group_row.short_name; 
            END IF;    
        END LOOP;
        RETURN NEW;
    END;
${trigger_function_name}$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0056_user_group_demo_trigger'),
    ]

    operations = [
        migrations.RunSQL(
            sql=create_func_sql,
            reverse_sql=f'DROP FUNCTION IF EXISTS {trigger_function_name}();',
        ),
        migrations.RunSQL(
            sql=f'CREATE TRIGGER {trigger_function_name} '
                f'BEFORE INSERT OR UPDATE ON public.projects_project '
                f'FOR EACH ROW EXECUTE PROCEDURE {trigger_function_name}();',
            reverse_sql=f'DROP TRIGGER IF EXISTS {trigger_function_name} ON '
                        f'public.projects_project;'
        ),
    ]
