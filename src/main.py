import argparse
import json
import logging
import os
import requests
import sys
import time

from urllib.parse import quote

from src.config import (
    CONFIGS,
    SQLITE_BATCH_SIZE, 
    TEMP_DIR, 
    PREFIX_MAPPER,
    TODAY
)

from src.etl.transform import Transform
from src.util import (
    clean_and_create_dir,
    generate_browser_session,
    load_exporter_map,
    resolve_files, 
)

from src.db.sqlite.config import sqlite_cursor, sqlite_connection
from src.db.sqlite.db import auto_migrate

from src.etl import load

from src.integrations.google.gmail import (
    get_gmail_service, 
    get_email_messages, 
    wait_for_emails
)


def main():

    # --- Setup dos Logs --- #
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, 'app.log'),
        level=logging.INFO,
        encoding='utf-8',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # --- Setup Geral --- #
    parser = argparse.ArgumentParser(description="CLI do Bot ChatGuru")
    parser.add_argument("--initial-date", type=str, default=TODAY, help="Data início do relatório a ser extraído no formato `yyyy-mm-dd`")
    parser.add_argument("--final-date", type=str, default=TODAY, help="Data final do relatório a ser extraído no formato `yyyy-mm-dd`")
    args = parser.parse_args()

    initial_date = args.initial_date
    final_date = args.final_date

    logging.info("Buscando dados no Chat Guru.")
    logging.info("Data Inicial: %s", initial_date)
    logging.info("Data Final: %s", final_date)

    EXPORT_PAYLOAD = load_exporter_map(
        initial_date=initial_date,
        final_date=final_date
    )

    clean_and_create_dir(TEMP_DIR)
    

    # --- Setup da Banco de Dados --- #
    auto_migrate(sqlite_cursor)   
    

    # --- Setup da sessão --- #
    LOGIN_URL = f"{CONFIGS.get("BASE_URL")}/login"
    LOGOUT_URL = f"{CONFIGS.get("BASE_URL")}/logout"

    # --- Autenticar Gmail --- #
    logging.info("Autenticando com Gmail...")
    gmail_service = get_gmail_service()





    # --- Login --- #
    browser_session = generate_browser_session()

    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": LOGIN_URL
    }

    login_payload = {
        "browser_session": browser_session,
        "email": CONFIGS.get("EMAIL"),
        "password": CONFIGS.get("PASSWORD")
    }

    try:
        logging.info("Realizando login...")
        response = session.post(LOGIN_URL, data=login_payload, headers=headers)

        if response.ok and "logout" in response.text.lower():
            logging.info("Login bem-sucedido!")
        else:
            logging.error("Falha no login.")
            return
        
    except Exception as exc:
        logging.exception("Erro no login: %s", exc)
        return


    # --- Exportar NPS --- #
    logging.info("Preparando exportação de NPS...")

    export_start_time = int(time.time())

    for payload in EXPORT_PAYLOAD:
        encoded_export = quote(json.dumps(payload))
        nps_id = payload["nps"]
        export_url = f"{CONFIGS.get("BASE_URL")}/nps/{nps_id}/export?export={encoded_export}"

        logging.info("Disparando exportação de NPS: %s",nps_id)
        session.get(export_url, headers=headers)


    # --- Aguardar e-mails de notificação --- #
    logging.info("Aguardando e-mails de notificação do chatguru...")
    messages = wait_for_emails(
        gmail_service,
        sender="notifications@zap.guru",
        expected_count=len(EXPORT_PAYLOAD),
        after_timestamp=export_start_time,
        timeout=300,
        interval=15
    )


    # --- Baixar arquivos --- #
    logging.info("%s e-mail(s) recebidos. Baixando arquivos...", len(messages))
    download_links = get_email_messages(gmail_service, messages)
    for item in download_links:
        response = requests.get(item["link"])
        
        filepath = f"tmp/{item['filename']}"
        
        with open(filepath, "wb") as f:
            f.write(response.content)

        logging.info("Arquivo salvo: %s", filepath)


    # --- Limpar Dados e Salvar no Banco de Dados --- #
    transform = Transform()

    file_map = resolve_files(TEMP_DIR, PREFIX_MAPPER)

    for table_name, filepath in file_map.items():
        avaliacoes = transform.execute(filepath)
        load.insert_data_batch(
            cursor=sqlite_cursor,
            connection=sqlite_connection,
            table=table_name,
            data=avaliacoes,
            chunk_size=SQLITE_BATCH_SIZE
        )

    # --- Finalizando Script --- #
    logging.info("Saindo do sistema...")
    session.post(LOGOUT_URL)

    logging.info("Apagando cookies e encerrando sessão...")
    session.close()
    session.cookies.clear_session_cookies()

    logging.info("Limpando tmp/...")
    clean_and_create_dir(TEMP_DIR)

    logging.info("ETL finalizado com sucesso!")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
