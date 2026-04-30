def auto_migrate(cur):
    sac_avaliacao_atendimento = """
        CREATE TABLE IF NOT EXISTS sac_avaliacao_atendimento (
            id_da_resposta TEXT,
            nota INTEGER,
            comentario TEXT,
            segunda_nota INTEGER,
            segundo_comentario TEXT,
            chat_da_resposta TEXT,
            ip_do_respondedor TEXT,
            data_da_resposta TIMESTAMP,
            nps_da_resposta TEXT,
            data_de_criacao TIMESTAMP,
            data_da_expiracao TIMESTAMP,
            usuario_delegado TEXT,
            grupos_delegado TEXT,
            usuario TEXT, 
            classificacao TEXT
        );
    """
    cur.execute(sac_avaliacao_atendimento)

    comercial_avaliacao_atendimento = """
        CREATE TABLE IF NOT EXISTS comercial_avaliacao_atendimento (
            id_da_resposta TEXT,
            nota INTEGER,
            comentario TEXT,
            segunda_nota INTEGER,
            segundo_comentario TEXT,
            chat_da_resposta TEXT,
            ip_do_respondedor TEXT,
            data_da_resposta TIMESTAMP,
            nps_da_resposta TEXT,
            data_de_criacao TIMESTAMP,
            data_da_expiracao TIMESTAMP,
            usuario_delegado TEXT,
            grupos_delegado TEXT,
            usuario TEXT, 
            classificacao TEXT
        );
  
    """
    cur.execute(comercial_avaliacao_atendimento)

    financeiro_avaliacao_atendimento = """
        CREATE TABLE IF NOT EXISTS financeiro_avaliacao_atendimento (
            id_da_resposta TEXT,
            nota INTEGER,
            comentario TEXT,
            segunda_nota INTEGER,
            segundo_comentario TEXT,
            chat_da_resposta TEXT,
            ip_do_respondedor TEXT,
            data_da_resposta TIMESTAMP,
            nps_da_resposta TEXT,
            data_de_criacao TIMESTAMP,
            data_da_expiracao TIMESTAMP,
            usuario_delegado TEXT,
            grupos_delegado TEXT,
            usuario TEXT, 
            classificacao TEXT
        );
    """
    cur.execute(financeiro_avaliacao_atendimento)

    sac_tecnico_avaliacao_atendimento = """
        CREATE TABLE IF NOT EXISTS sac_tecnico_avaliacao_atendimento (
            id_da_resposta TEXT,
            nota INTEGER,
            comentario TEXT,
            segunda_nota INTEGER,
            segundo_comentario TEXT,
            chat_da_resposta TEXT,
            ip_do_respondedor TEXT,
            data_da_resposta TIMESTAMP,
            nps_da_resposta TEXT,
            data_de_criacao TIMESTAMP,
            data_da_expiracao TIMESTAMP,
            usuario_delegado TEXT,
            grupos_delegado TEXT,
            usuario TEXT, 
            classificacao TEXT
        );
    """
    cur.execute(sac_tecnico_avaliacao_atendimento)


def reset(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    for table in tables:
        cur.execute(f"DROP TABLE {table[0]}")
    