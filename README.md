# bot-chatguru

ETL automatizado para coleta de dados NPS do ChatGuru. Autentica no painel web do ChatGuru, dispara exportações de 4 pesquisas NPS, aguarda os e-mails de notificação via Gmail API, baixa os CSVs e carrega os dados em um banco SQLite — sem duplicatas.

## Pré-requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes)
- Conta no ChatGuru com acesso às pesquisas NPS
- Projeto no Google Cloud com **Gmail API** habilitada
- Acesso à rede onde o banco SQLite está hospedado (`\\192.168.11.88\Projetos\phd-bi-nps\`)

## Configuração

### 1. Instalar dependências

```bash
uv sync
```

### 2. Variáveis de ambiente

Copie o template e preencha com suas credenciais:

```bash
cp .env.example .env
```

| Variável   | Descrição                                        |
|------------|--------------------------------------------------|
| `BASE_URL` | URL base do ChatGuru (ex: `https://s6.chatguru.app`) |
| `EMAIL`    | E-mail de login no ChatGuru                      |
| `PASSWORD` | Senha de login no ChatGuru                       |

> As variáveis `MYSQL_*` são reservadas para uso futuro e não são necessárias.

### 3. Credenciais do Google (Gmail API)

1. No [Google Cloud Console](https://console.cloud.google.com/), crie um projeto e habilite a **Gmail API**
2. Crie credenciais OAuth 2.0 do tipo **"Aplicativo de desktop"**
3. Baixe o arquivo JSON e salve como `credentials.json` na raiz do projeto
4. Na primeira execução, um browser abrirá para autorização — o token será salvo em `token.json` automaticamente nas execuções seguintes

> `credentials.json` e `token.json` estão no `.gitignore` e **nunca devem ser versionados**.

## Execução

```bash
uv run src/main.py --initial-date "YYYY-MM-DD" --final-date "YYYY-MM-DD"
```

**Exemplo:**

```bash
uv run src/main.py --initial-date "2026-01-01" --final-date "2026-03-31"
```

O script executa na seguinte ordem:

1. Faz login no ChatGuru
2. Dispara exportações para as 4 pesquisas NPS (SAC, Comercial, Financeiro, SAC Técnico)
3. Aguarda até **5 minutos** pelos e-mails de notificação do ChatGuru
4. Baixa os CSVs a partir dos links recebidos por e-mail
5. Transforma e classifica os dados (Promotores / Neutros / Detratores)
6. Carrega os registros no SQLite, ignorando duplicatas
7. Faz logout e limpa os arquivos temporários

Logs são gravados em `logs/app.log`.

## Banco de dados

O banco SQLite é armazenado em `\\192.168.11.88\Projetos\phd-bi-nps\nps.db` (caminho de rede UNC).

### Tabelas

| Tabela                              | Pesquisa    |
|-------------------------------------|-------------|
| `sac_avaliacao_atendimento`         | SAC         |
| `comercial_avaliacao_atendimento`   | Comercial   |
| `financeiro_avaliacao_atendimento`  | Financeiro  |
| `sac_tecnico_avaliacao_atendimento` | SAC Técnico |

Cada tabela contém os campos:

| Campo                | Tipo    | Descrição                        |
|----------------------|---------|----------------------------------|
| `id_da_resposta`     | TEXT PK | Identificador único da resposta  |
| `nota`               | INTEGER | Nota principal (0–10)            |
| `comentario`         | TEXT    | Comentário do respondente        |
| `segunda_nota`       | INTEGER | Segunda nota (quando aplicável)  |
| `segundo_comentario` | TEXT    | Segundo comentário               |
| `chat_da_resposta`   | TEXT    | ID do chat associado             |
| `ip_do_respondedor`  | TEXT    | IP do respondente                |
| `data_da_resposta`   | TEXT    | Data/hora da resposta            |
| `nps_da_resposta`    | TEXT    | Tipo NPS                         |
| `data_de_criacao`    | TEXT    | Data de criação da pesquisa      |
| `data_da_expiracao`  | TEXT    | Data de expiração                |
| `usuario_delegado`   | TEXT    | Usuários delegados               |
| `grupos_delegado`    | TEXT    | Grupos delegados                 |
| `usuario`            | TEXT    | Primeiro usuário delegado        |
| `classificacao`      | TEXT    | Classificação NPS                |

### Classificação NPS

| Nota | Classificação |
|------|---------------|
| 9–10 | Promotores    |
| 7–8  | Neutros       |
| 0–6  | Detratores    |
