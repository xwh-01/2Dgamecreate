# Parse user requirement into structured generation parameters
from ...ai.requirement_parser import ParseRequirementInput
from ..context import WorkflowContext


class ParseRequirementStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        if ctx.task is None:
            ctx.error_message = "task not loaded"
            return ctx

        input_data = ParseRequirementInput(
            user_input=ctx.task.user_input,
            extra_params=ctx.task.parsed_requirement or {},
            asset_type=ctx.task.asset_type,
            size=ctx.task.size,
        )
        ctx.parsed_requirement = workflow.requirement_parser.parse(input_data)
        return ctx
