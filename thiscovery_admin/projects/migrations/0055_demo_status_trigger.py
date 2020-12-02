from django.db import migrations


create_func_sql = """
CREATE OR REPLACE FUNCTION validate_ProjectGroupVisibility_demo_status() RETURNS trigger AS $validate_ProjectGroupVisibility_demo_status$
    DECLARE
        project_demo_status     boolean;
        group_demo_status       boolean;
    BEGIN
        SELECT p.demo INTO project_demo_status FROM public.projects_project p WHERE p.id = NEW.project_id;
        SELECT g.demo INTO group_demo_status FROM public.projects_usergroup g WHERE g.id = NEW.user_group_id;
        IF (project_demo_status = group_demo_status) THEN
            RETURN NEW;
        ELSE 
            RAISE EXCEPTION 'Demo status of project and group do not match (project: %, group: %)', 
            project_demo_status, group_demo_status; 
        END IF;
    END;
$validate_ProjectGroupVisibility_demo_status$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0054_auto_20201202_1710'),
    ]

    operations = [
        migrations.RunSQL(
            sql=create_func_sql,
            reverse_sql='DROP FUNCTION IF EXISTS validate_ProjectGroupVisibility_demo_status();',
        ),
        migrations.RunSQL(
            sql='CREATE TRIGGER validate_ProjectGroupVisibility_demo_status '
                'BEFORE INSERT OR UPDATE ON public.projects_projectgroupvisibility '
                'FOR EACH ROW EXECUTE PROCEDURE validate_ProjectGroupVisibility_demo_status();',
            reverse_sql='DROP TRIGGER IF EXISTS validate_ProjectGroupVisibility_demo_status ON '
                        'public.projects_projectgroupvisibility;'
        ),
    ]
