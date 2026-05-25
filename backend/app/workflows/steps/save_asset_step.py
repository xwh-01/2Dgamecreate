# Persist generated asset to storage and database
import uuid

from ...domain.entities.asset import Asset
from ...domain.enums.asset_type import AssetType
from ...utils.naming import generate_asset_name
from ...utils.time import utcnow
from ..context import WorkflowContext


class SaveAssetStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        if ctx.processed_image is None:
            ctx.error_message = "no processed image to save"
            return ctx

        asset_id = str(uuid.uuid4())
        description = ctx.task.user_input if ctx.task else "untitled"
        asset_type = ctx.task.asset_type if ctx.task else AssetType.CHARACTER
        project_id = ctx.task.project_id if ctx.task else "unknown"
        task_id = ctx.task_id

        name = generate_asset_name(description, asset_type.value)
        filename = f"{name}_{asset_id[:8]}.png"

        file_path = workflow.path_builder.build_asset_path(
            project_id, asset_type, filename
        )

        try:
            workflow.file_storage.ensure_type_dirs(project_id)
            workflow.file_storage.save(file_path, ctx.processed_image.image_bytes)
        except Exception as e:
            ctx.error_message = f"File save failed: {e}"
            return ctx

        now = utcnow()
        asset = Asset(
            id=asset_id,
            project_id=project_id,
            task_id=task_id,
            name=name,
            asset_type=asset_type,
            file_path=file_path,
            preview_url=workflow.file_storage.get_url(file_path),
            width=ctx.processed_image.width,
            height=ctx.processed_image.height,
            format="png",
            transparent=True,
            metadata={
                "description": description,
                "final_prompt": ctx.prompt_package.to_full_prompt() if ctx.prompt_package else "",
                "parsed_requirement": ctx.parsed_requirement.to_dict() if ctx.parsed_requirement else {},
                "art_style": ctx.style_profile.art_style.value if ctx.style_profile else "",
                "size": ctx.task.size if ctx.task else "",
                "created_at": now.isoformat(),
            },
            created_at=now,
            updated_at=now,
        )

        try:
            workflow.asset_repo.create(asset)
        except Exception as e:
            ctx.error_message = f"Metadata save failed: {e}"
            return ctx

        ctx.saved_path = file_path
        ctx.asset_record = asset
        return ctx
