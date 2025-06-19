from .start import router as start_router
from .register import router as register_router
from .category_menu import router as category_menu_router
from .products_handlers import router as product_handler_router
from .cart_handler import router as cart_router
from .back_handler import router as back_router

def setup_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(category_menu_router)
    dp.include_router(product_handler_router)
    dp.include_router(cart_router)
    dp.include_router(back_router)
