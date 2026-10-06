import unittest
from datetime import datetime
try:
    from airflow.utils.context import Context
except ImportError:
    class Context(dict):
        pass
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.first_airflow import ExtractOperator, TransformOperator, LoadOperator

class TestETLOperators(unittest.TestCase):
    def setUp(self):
        self.context = Context({
            'task_instance': None,
            'execution_date': datetime.now()
        })

    def test_extract_operator(self):
        extract = ExtractOperator(
            task_id='test_extract',
            source_system='test_source'
        )
        result = extract.process(self.context)
        self.assertEqual(result['source'], 'test_source')
        self.assertEqual(result['data'], 'sample_data')

    def test_transform_operator(self):
        transform = TransformOperator(
            task_id='test_transform',
            transformation_type='test_transformation'
        )
        # Mock the context with input data
        self.context['task_instance'] = type('obj', (object,), {
            'xcom_pull': lambda task_ids: {'source': 'test', 'data': 'test_data'}
        })
        self.context['task'] = type('obj', (object,), {'upstream_task_ids': {'test_extract'}})
        
        result = transform.process(self.context)
        self.assertTrue(result['transformed'])

    def test_load_operator(self):
        load = LoadOperator(
            task_id='test_load',
            target_system='test_target'
        )
        # Mock the context with input data
        self.context['task_instance'] = type('obj', (object,), {
            'xcom_pull': lambda task_ids: {'source': 'test', 'data': 'test_data', 'transformed': True}
        })
        self.context['task'] = type('obj', (object,), {'upstream_task_ids': {'test_transform'}})
        
        # Should not raise any exceptions
        load.process(self.context)

    def test_dag_structure(self):
        from src.first_airflow import dag
        self.assertEqual(dag.dag_id, "etl_workflow_oop")
        self.assertEqual(len(dag.tasks), 3)
        self.assertEqual(dag.task_dict["extract"].downstream_task_ids, {"transform"})
        self.assertEqual(dag.task_dict["transform"].downstream_task_ids, {"load"})
        self.assertEqual(dag.task_dict["load"].upstream_task_ids, {"transform"})

if __name__ == '__main__':
    unittest.main()