# Post-process generated image (crop, resize, background removal)
from ..asset_generation_workflow import WorkflowContext


class PostProcessStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        raise NotImplementedError
