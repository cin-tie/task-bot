from .start import router as start_router
from .auth import router as auth_router
from .tasks import router as tasks_router

__all__ = ['start_router', 'auth_router', 'tasks_router']