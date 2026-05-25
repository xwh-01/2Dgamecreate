# Quality check against thresholds and style consistency
from ..context import WorkflowContext


class QualityCheckStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        if ctx.processed_image is None:
            ctx.error_message = "no processed image to check"
            return ctx

        size = ctx.task.size if ctx.task and ctx.task.size else "512x512"
        style_dict = None
        if ctx.style_profile:
            style_dict = {
                "art_style": ctx.style_profile.art_style.value,
                "prompt_rules": ctx.style_profile.prompt_rules,
                "negative_prompt_rules": ctx.style_profile.negative_prompt_rules,
                "default_size": ctx.style_profile.default_size,
            }

        ctx.quality_result = workflow.quality_checker.check(
            ctx.processed_image,
            size,
            parsed_requirement=ctx.parsed_requirement,
            prompt_package=ctx.prompt_package,
            style_profile=style_dict,
        )

        if not ctx.quality_result.passed:
            ctx.error_message = f"Quality check failed: {ctx.quality_result.overall_message}"

        return ctx
