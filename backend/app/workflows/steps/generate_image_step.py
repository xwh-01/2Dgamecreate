# Generate image via AI model client
from ..asset_generation_workflow import WorkflowContext


class GenerateImageStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        raise NotImplementedError
