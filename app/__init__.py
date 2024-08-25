from .telegram_module import TelegramModule
from .llm_module import LLMModule
from .database_module import DatabaseModule
from .web_interface import app
from .main import MainApplication

__all__ = ['TelegramModule', 'LLMModule', 'DatabaseModule', 'app', 'MainApplication']

# Initialize the main application
main_app = MainApplication()