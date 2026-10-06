"""
ETL Workflow DAG using Object-Oriented Programming

This DAG implements a simple ETL (Extract, Transform, Load) workflow
that runs daily to process data using OOP principles.

The workflow is implemented using custom classes for better organization,
reusability, and maintainability.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, Optional

try:
    from airflow import DAG
    from airflow.models.baseoperator import BaseOperator
    from airflow.exceptions import AirflowException
except ImportError:
    # Lightweight fallback for environments where full apache-airflow is not installed
    class AirflowException(Exception):
        pass

    class BaseOperator:
        def __init__(self, task_id: str = "", dag: Any = None, **kwargs) -> None:
            self.task_id = task_id
            self.dag = dag
            self.upstream_task_ids = set()
            self.downstream_task_ids = set()
            if dag and hasattr(dag, "_add_task"):
                dag._add_task(self)

        def __rshift__(self, other):
            self.downstream_task_ids.add(other.task_id)
            other.upstream_task_ids.add(self.task_id)
            return other

    class DAG:
        def __init__(self, dag_id: str, **kwargs) -> None:
            self.dag_id = dag_id
            self.tasks = []
            self.task_dict = {}

        def _add_task(self, task):
            self.tasks.append(task)
            self.task_dict[task.task_id] = task

# Configure logging
logger = logging.getLogger(__name__)

class ETLBaseOperator(BaseOperator, ABC):
    """
    Abstract base class for ETL operators.
    Provides common functionality for all ETL tasks.
    """
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data: Optional[Dict[str, Any]] = None

    def execute(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Template method that defines the workflow for each ETL operation.
        """
        try:
            self.pre_execute(context)
            result = self.process(context)
            self.post_execute(context)
            return result
        except Exception as e:
            self.handle_error(e)

    @abstractmethod
    def process(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Abstract method to be implemented by concrete operators."""
        pass

    def pre_execute(self, context: Dict[str, Any]) -> None:
        """Hook for pre-execution setup."""
        logger.info(f"Starting {self.task_id} operation")

    def post_execute(self, context: Dict[str, Any]) -> None:
        """Hook for post-execution cleanup."""
        logger.info(f"Completed {self.task_id} operation")

    def handle_error(self, error: Exception) -> None:
        """Common error handling logic."""
        logger.error(f"{self.task_id} failed: {str(error)}")
        raise AirflowException(f"{self.task_id} task failed: {str(error)}")

class ExtractOperator(ETLBaseOperator):
    """Operator for extracting data from source systems."""

    def __init__(self, source_system: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.source_system = source_system

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Implement the data extraction logic."""
        logger.info(f"Extracting data from {self.source_system}")
        # Add your extraction logic here
        return {"source": self.source_system, "data": "sample_data"}

class TransformOperator(ETLBaseOperator):
    """Operator for transforming extracted data."""

    def __init__(self, transformation_type: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.transformation_type = transformation_type

    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Implement the data transformation logic."""
        upstream_ids = context['task'].upstream_task_ids
        upstream_id = next(iter(upstream_ids)) if upstream_ids else None
        input_data = context['task_instance'].xcom_pull(task_ids=upstream_id) if upstream_id else {}
        logger.info(f"Transforming data using {self.transformation_type}")
        # Add your transformation logic here
        return {**(input_data or {}), "transformed": True}

class LoadOperator(ETLBaseOperator):
    """Operator for loading transformed data into target systems."""

    def __init__(self, target_system: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.target_system = target_system

    def process(self, context: Dict[str, Any]) -> None:
        """Implement the data loading logic."""
        upstream_ids = context['task'].upstream_task_ids
        upstream_id = next(iter(upstream_ids)) if upstream_ids else None
        input_data = context['task_instance'].xcom_pull(task_ids=upstream_id) if upstream_id else {}
        logger.info(f"Loading data into {self.target_system}")
        # Add your loading logic here

class ETLDag:
    """
    A class to encapsulate DAG configuration and creation.
    """

    def __init__(
        self,
        dag_id: str,
        schedule_interval: str,
        start_date: datetime,
        default_args: Dict[str, Any],
        description: str
    ):
        self.dag_id = dag_id
        self.schedule_interval = schedule_interval
        self.start_date = start_date
        self.default_args = default_args
        self.description = description
        self.dag = self._create_dag()

    def _create_dag(self) -> DAG:
        """Create and configure the DAG."""
        return DAG(
            dag_id=self.dag_id,
            default_args=self.default_args,
            description=self.description,
            schedule=self.schedule_interval,
            start_date=self.start_date,
            catchup=False,
            max_active_runs=1,
            doc_md=__doc__
        )

    def get_dag(self) -> DAG:
        """Return the configured DAG."""
        return self.dag

# DAG Configuration
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 3),  # yesterday's date
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': False,
    'queue': 'default',
    'pool': 'default_pool',
    'tags': ['etl', 'daily'],
}

# Create ETL DAG instance
etl_dag = ETLDag(
    dag_id='etl_workflow_oop',
    schedule_interval='0 0 * * *',
    start_date=datetime(2025, 9, 3),  # yesterday's date
    default_args=default_args,
    description='ETL workflow using OOP principles'
)

# Get DAG instance
dag = etl_dag.get_dag()

# Create task instances
extract_task = ExtractOperator(
    task_id='extract',
    source_system='example_source',
    dag=dag,
)

transform_task = TransformOperator(
    task_id='transform',
    transformation_type='example_transformation',
    dag=dag,
)

load_task = LoadOperator(
    task_id='load',
    target_system='example_target',
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task
