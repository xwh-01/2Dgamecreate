# Persist generated asset to storage and database
from ..asset_generation_workflow import WorkflowContext


class SaveAssetStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        raise NotImplementedError
