import os
import environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

BOT_TOKEN = env.str('BOT_TOKEN')
REDIS_URL = env.str('REDIS_URL')
DB_DSN = env.str('DB_DSN')
