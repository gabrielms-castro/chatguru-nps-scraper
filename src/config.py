import os

from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
TODAY = datetime.now().strftime("%Y-%m-%d")

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent

TEMP_DIR = BASE_DIR / "tmp"

CONFIGS = {
    "EMAIL" : os.getenv("EMAIL"),
    "PASSWORD" : os.getenv("PASSWORD"),
    "BASE_URL" : os.getenv("BASE_URL"),
    "MYSQL_HOST" : os.getenv("MYSQL_HOST"),
    "MYSQL_USER" : os.getenv("MYSQL_USER"),
    "MYSQL_PASSWORD" : os.getenv("MYSQL_PASSWORD"),
    "MYSQL_DATABASE" : os.getenv("MYSQL_DATABASE"),
}

PREFIX_MAPPER = {
    "sac_avaliacao_atendimento": "ChatGuru__SAC__Avaliacao_de_atendimento",
    "comercial_avaliacao_atendimento": "ChatGuru__COMERCIAL__Avaliacao_de_atendimento",
    "financeiro_avaliacao_atendimento": "ChatGuru__FINANCEIRO__Avaliacao_de_atendimento",
    "sac_tecnico_avaliacao_atendimento": "ChatGuru__SAC_TECNICO__Avaliacao_de_atendimento",
}

SQLITE_BATCH_SIZE = 30000