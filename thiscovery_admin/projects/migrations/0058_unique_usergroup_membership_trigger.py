from django.db import migrations


trigger_function_name = 'check_usergroupmembership_duplicate'


create_func_sql = f"""
CREATE OR REPLACE FUNCTION {trigger_function_name}() RETURNS trigger AS ${trigger_function_name}$
    BEGIN
        IF EXISTS ( 
            SELECT 
                1 
            FROM 
                public.projects_usergroupmembership ugm 
            WHERE ugm.user_id = NEW.user_id AND ugm.user_group_id = NEW.user_group_id
        ) THEN RAISE EXCEPTION 'User % is already a member of group %',
            NEW.user_id, NEW.user_group_id;    
        ELSE
            RETURN NEW;
        END IF;
    END;
${trigger_function_name}$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0057_project_demo_trigger'),
    ]

    operations = [
        migrations.RunSQL(
            sql=create_func_sql,
            reverse_sql=f'DROP FUNCTION IF EXISTS {trigger_function_name}();',
        ),
        migrations.RunSQL(
            sql=f'CREATE TRIGGER {trigger_function_name} '
                f'BEFORE INSERT OR UPDATE ON public.projects_usergroupmembership '
                f'FOR EACH ROW EXECUTE PROCEDURE {trigger_function_name}();',
            reverse_sql=f'DROP TRIGGER IF EXISTS {trigger_function_name} ON '
                        f'public.projects_usergroupmembership;'
        ),
    ]
