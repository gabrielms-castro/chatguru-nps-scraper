import logging
from sqlite3 import Connection, Cursor

from src.db.sqlite.avaliacao import get_existing_ids, get_one, insert_batch, insert_one
from src.dtos.avaliacao_atendimento_dto import AvaliacaoAtendimentoDTO



def insert_data(connection, cursor, table, data: list[str]):
    for d in data:
        result = get_one(cursor, table, d[0])

        if result:
            logging.info("Dado já existe | table=%s | id_resposta=%s", table, d[0])
            continue

        logging.info("Salvando dados | table=%s | id_resposta=%s", table, d[0])
        insert_one(connection, cursor, table, d)


def insert_data_batch(
    connection: Connection, 
    cursor: Cursor, 
    table: str, 
    data: list[AvaliacaoAtendimentoDTO], 
    chunk_size: int
):  
    ids = [d.id_da_resposta for d in data]
    existing_ids = get_existing_ids(cursor, table, ids, chunk_size)

    rows_to_insert = []
    for row in data:
        if row.id_da_resposta in existing_ids:
            logging.info("Dado já existe | table=%s | id_resposta=%s", table, row.id_da_resposta)
            continue

        logging.info("Salvando dados | table=%s | id_resposta=%s", table, row.id_da_resposta)
        rows_to_insert.append(row)

    if rows_to_insert:
        insert_batch(connection, cursor, table, rows_to_insert)