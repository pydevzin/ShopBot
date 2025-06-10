from .start import router as start_router

def setup_handlers(dp):
    dp.include_router(start_router)