from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AvaliacaoAtendimentoDTO:
    id_da_resposta: str
    nota: Optional[int]
    comentario: Optional[str]
    segunda_nota: Optional[int]
    segundo_comentario: Optional[str]
    chat_da_resposta: Optional[str]
    ip_do_respondedor: Optional[str]
    data_da_resposta: Optional[datetime]
    nps_da_resposta: Optional[str]
    data_de_criacao: Optional[datetime]
    data_da_expiracao: Optional[datetime]
    usuario_delegado: Optional[str]
    grupos_delegado: Optional[str]
    usuario: Optional[str]
    classificacao: Optional[str]