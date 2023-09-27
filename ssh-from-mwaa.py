from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

with DAG(dag_id="any_bash_command_dag", schedule_interval=None, catchup=False, start_date=days_ago(1)) as dag:
      cli_command = BashOperator(
          task_id="bash_command",
          bash_command="ping ec2-xxxxx.compute-1.amazonaws.com"
      )
