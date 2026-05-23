# Build optimized prompts from parsed parameters
from ..asset_generation_workflow import WorkflowContext


class BuildPromptStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        raise NotImplementedError
