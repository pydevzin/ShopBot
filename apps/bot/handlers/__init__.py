from .start import router as start_router
from .register import router as register_router
from .category_menu import router as category_menu_router


def setup_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(category_menu_router)
