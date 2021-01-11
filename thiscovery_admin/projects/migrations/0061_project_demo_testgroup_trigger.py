from django.db import migrations


trigger_function_name = 'validate_testing_group_demo_status'


create_func_sql = f"""
CREATE OR REPLACE FUNCTION {trigger_function_name}() RETURNS trigger AS ${trigger_function_name}$
    DECLARE
        group_demo_status       boolean;
    BEGIN
        -- Don't do anything if testing_group is NULL
        IF NEW.testing_group_id IS NULL THEN 
            RETURN NEW;
        END IF;
        
        SELECT g.demo INTO group_demo_status FROM public.projects_usergroup g WHERE g.id = NEW.testing_group_id;
        IF (NEW.demo = group_demo_status) THEN
            RETURN NEW;
        ELSE 
            RAISE EXCEPTION 'Demo status of project and testing group do not match (project: %, testing group: %)', 
            NEW.demo, group_demo_status; 
        END IF;
    END;
${trigger_function_name}$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0060_auto_20210106_1638'),
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
                        'public.projects_project;'
        ),
    ]
