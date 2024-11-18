"""
This is a boilerplate pipeline 'pipeline_autogluon'
generated using Kedro 0.19.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import train_autogluon, evaluate_model
from .nodes import split_data

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=split_data,
                inputs=["model_input_table", "params:model_options"],
                outputs=["X", "y"],
                name="split_autogluon_data_node",
            ),
            node(
                func=train_autogluon,
                inputs=["X", "y", "params:time_limit"],
                outputs="autogluon_model",
                name="train_autogluon_node",
            ),
            node(
                func=evaluate_model,
                inputs=["autogluon_model", "X", "y"],
                outputs="model_performance",
                name="evaluate_autogluon_model_node",
            ),
        ]
    )
