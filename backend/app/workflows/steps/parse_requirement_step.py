# Parse user requirement into structured generation parameters
from ..asset_generation_workflow import WorkflowContext


class ParseRequirementStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        raise NotImplementedError
