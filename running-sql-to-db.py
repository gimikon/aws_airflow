"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from airflow.decorators import dag, task
from datetime import datetime
import os
from airflow import settings
from sqlalchemy import text

DAG_ID = os.path.basename(__file__).replace(".py", "")

NEW_ROLE = "NEW1"
SOURCE_ROLE = "Viewer"
USER_NAME = "my-role-name"

SQL_QUERY = """
DO $$
DECLARE
    new_role_name CONSTANT VARCHAR(64) := '{0}'; -- new role name
    source_role_name CONSTANT VARCHAR(64) := '{1}'; -- role to copy from
    user_name CONSTANT VARCHAR(64) := '{2}'; -- user to assign role to
    new_role_id integer;
    source_role_id integer;
    new_user_id integer;
BEGIN
    IF NOT EXISTS (SELECT id from ab_role WHERE name = source_role_name) THEN
        RAISE EXCEPTION 'Role "%" does not exist.', source_role_name;
    else
        SELECT * from ab_role ;
        RAISE INFO 'Source role ID is %', source_role_id;
    END IF;
END
$$ LANGUAGE plpgsql;


"""

@task()
def execute_sql_fn(sql):
    try:
        session = settings.Session()
        result = session.execute(text(sql)).all()
        for row in result:
            print(row)
      

        return result
    except Exception as e:
        print(e)
        return None
    
@dag(
    dag_id=DAG_ID,
    schedule_interval=None,     
    start_date=datetime(2022, 1, 1),
    )
def sql_dag():
    # t = execute_sql_fn(SQL_QUERY.format(NEW_ROLE,SOURCE_ROLE,USER_NAME))
    t = execute_sql_fn("SELECT * from ab_view_menu;")
    # print(t)

my_sql_dag = sql_dag()


# ab_view_menu is the table for view list page
# ab_permission_view_role > look for role id (example is 11) then permissions_view_id then you will see permissions_id and view_menu_id permission_id is like action(can_read) then ab_view_menu is where you should see the dag, therefore the dag is not in ab_view_menu table, it wont show when you are trying to give permissions to this dag

