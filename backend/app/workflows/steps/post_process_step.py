# Post-process generated image (crop, resize, background removal)
import logging

from ...utils.image_utils import ensure_png, normalize_sprite_canvas, open_image, resize_to_target
from ..context import WorkflowContext

logger = logging.getLogger(__name__)


class PostProcessStep:
    def execute(self, ctx: WorkflowContext, workflow) -> WorkflowContext:
        if ctx.generated_image is None:
            ctx.error_message = "no generated image to process"
            return ctx

        img = open_image(ctx.generated_image.image_bytes)
        if img is None:
            ctx.error_message = "cannot open generated image bytes"
            return ctx

        target_size = ctx.task.size if ctx.task and ctx.task.size else None
        if target_size:
            try:
                img = resize_to_target(img, target_size)
            except Exception as e:
                logger.warning(f"Resize failed, using original: {e}")

        try:
            base_bytes = ensure_png(img)
        except Exception as e:
            ctx.error_message = f"PNG conversion failed: {e}"
            return ctx

        output_size = target_size if target_size else "512x512"
        try:
            processed_bytes = normalize_sprite_canvas(base_bytes, output_size)
        except Exception as e:
            logger.warning(f"Sprite normalization failed, using unnormalized PNG: {e}")
            processed_bytes = base_bytes

        processed_img = open_image(processed_bytes)
        final_width = processed_img.width if processed_img else img.width
        final_height = processed_img.height if processed_img else img.height

        from ...ai.image_generator_client import GeneratedImage

        ctx.processed_image = GeneratedImage(
            image_bytes=processed_bytes,
            width=final_width,
            height=final_height,
            format="png",
        )
        return ctx
