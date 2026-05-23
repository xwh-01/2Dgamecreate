# Main API router aggregating all route modules
from fastapi import APIRouter

from .routes import asset_routes, export_routes, generation_routes, project_routes, style_routes

router = APIRouter()
router.include_router(project_routes.router)
router.include_router(style_routes.router)
router.include_router(generation_routes.router)
router.include_router(asset_routes.router)
router.include_router(export_routes.router)
