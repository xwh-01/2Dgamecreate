# Quality check against thresholds and style consistency
from ..context import WorkflowContext


class QualityCheckStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        if ctx.processed_image is None:
            ctx.error_message = "no processed image to check"
            return ctx

        size = ctx.task.size if ctx.task and ctx.task.size else "512x512"
        ctx.quality_result = workflow.quality_checker.check(ctx.processed_image, size)

        if not ctx.quality_result.passed:
            ctx.error_message = f"Quality check failed: {ctx.quality_result.overall_message}"

        return ctx
