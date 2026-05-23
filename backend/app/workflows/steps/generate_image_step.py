# Generate image via AI model client
import logging

from ..context import WorkflowContext

logger = logging.getLogger(__name__)


class GenerateImageStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        if ctx.prompt_package is None:
            ctx.error_message = "no prompt package available"
            return ctx

        size = ctx.task.size if ctx.task and ctx.task.size else "512x512"

        try:
            ctx.generated_image = workflow.image_generator.generate(
                ctx.prompt_package, size
            )
        except Exception as e:
            ctx.error_message = str(e)
            logger.error(f"Image generation failed: {e}")

        return ctx
