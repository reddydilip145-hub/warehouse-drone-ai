"""Kubeflow pipeline definition.

This file is intentionally lightweight: it documents the production DAG shape
and can be compiled once Kubeflow Pipelines is installed in the ML environment.
"""

try:
    from kfp import dsl
except ImportError:  # Keeps repository tests usable without Kubeflow installed.
    dsl = None


if dsl:

    @dsl.pipeline(name="warehouse-drone-ai-phase-0-1-2")
    def warehouse_drone_ai_pipeline(dataset_uri: str, model_output_uri: str) -> None:
        phase0_validate_master_data = dsl.ContainerOp(
            name="phase-0-validate-master-data",
            image="warehouse-drone-ai/ml-pipeline:latest",
            command=["python", "-m", "ml.src.dataset"],
            arguments=["--output", dataset_uri],
        )

        phase1_train_model = dsl.ContainerOp(
            name="phase-1-train-rack-model",
            image="warehouse-drone-ai/ml-pipeline:latest",
            command=["python", "-m", "ml.src.train"],
            arguments=["--dataset", dataset_uri, "--model", model_output_uri],
        ).after(phase0_validate_master_data)

        dsl.ContainerOp(
            name="phase-2-generate-recommendations",
            image="warehouse-drone-ai/replenishment-api:latest",
            command=["python", "-m", "ml.pipelines.local_phase_0_1_2_pipeline"],
        ).after(phase1_train_model)

