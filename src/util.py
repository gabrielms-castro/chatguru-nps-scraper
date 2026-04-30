import os
import shutil
import uuid
import logging


def generate_browser_session():
    return uuid.uuid4()


def load_exporter_map(initial_date, final_date):
    return [
        {
            "nps": "6556196d7299f6abd79c2d68",
            "created__gte": f"{initial_date} 00:00:00 ",
            "created__lte": f"{final_date} 23:59:00 "
        },
        {
            "nps": "65535ccb9eed2178da4fbbbd",
            "created__gte": f"{initial_date} 00:00:00 ",
            "created__lte": f"{final_date} 23:59:00 "
        },
        {
            "nps": "6556190ce37fe4a26f92f9b6",
            "created__gte": f"{initial_date} 00:00:00 ",
            "created__lte": f"{final_date} 23:59:00 "
        },
        {
            "nps": "655611e4e39ee72575a9773e",
            "created__gte": f"{initial_date} 00:00:00 ",
            "created__lte": f"{final_date} 23:59:00 "
        }
    ]


def list_files(path):
    return [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]


def clean_and_create_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def resolve_files(folder, prefix_mapper) -> dict[str, str]:
    """
    Retorna {table_name: filepath} resolvendo o arquivo real pela pasta.
    """

    available_files = os.listdir(folder)
    resolved = {}

    for table_name, prefix in prefix_mapper.items():
        match = next(
            (f for f in available_files if f.startswith(prefix) and f.endswith(".csv")),
            None
        )
        if match:
            resolved[table_name] = os.path.join(folder, match)
        else:
            logging.warning("Nenhum arquivo encontrado para: %s", table_name)

    return resolved
