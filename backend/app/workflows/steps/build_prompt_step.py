# Build optimized prompts from parsed parameters
from ..context import WorkflowContext


class BuildPromptStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        if ctx.parsed_requirement is None:
            ctx.error_message = "no parsed requirement available"
            return ctx

        style_dict = None
        if ctx.style_profile:
            style_dict = {
                "art_style": ctx.style_profile.art_style.value,
                "prompt_rules": ctx.style_profile.prompt_rules,
                "negative_prompt_rules": ctx.style_profile.negative_prompt_rules,
                "default_size": ctx.style_profile.default_size,
                "view_type": ctx.style_profile.view_type.value,
            }

        ctx.prompt_package = workflow.prompt_builder.build(
            ctx.parsed_requirement, style_dict
        )
        return ctx
