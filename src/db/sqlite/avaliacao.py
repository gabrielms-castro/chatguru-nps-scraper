from dataclasses import astuple
from sqlite3 import Connection, Cursor

from src.dtos.avaliacao_atendimento_dto import AvaliacaoAtendimentoDTO


def get_one(cursor: Cursor, table_name: str, _id: str):
    sql = f"""
        SELECT * FROM {table_name} WHERE id_da_resposta = ?
    """
    cursor.execute(sql, (_id,))
    return cursor.fetchone()


def get_existing_ids(cursor: Cursor, table_name: str, ids: str, chunk_size: int = 900):
    existing = set()

    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i + chunk_size]
        
        placeholders = ",".join("?" * len(chunk))

        sql = f"SELECT id_da_resposta FROM {table_name} WHERE id_da_resposta IN ({placeholders})"

        cursor.execute(sql, chunk)
        existing.update(row[0] for row in cursor.fetchall())

    return existing


def insert_one(connection: Connection, cursor: Cursor, table_name: str, data: AvaliacaoAtendimentoDTO):
    sql = f"""
        INSERT INTO {table_name}
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, data)
    connection.commit()


def insert_batch(connection: Connection, cursor: Cursor, table_name: str, data: list[AvaliacaoAtendimentoDTO]):
    sql = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    rows = [astuple(row) for row in data]
    cursor.executemany(sql, rows)
    connection.commit()


