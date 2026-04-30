import csv
import logging

from datetime import datetime
from typing import Any, List, Optional

from src.dtos.avaliacao_atendimento_dto import AvaliacaoAtendimentoDTO

class Transform:
    
    def execute(self, filepath) -> List[AvaliacaoAtendimentoDTO]:
        cleaned = []

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                cleaned_row = self.clean_data(row)
                if cleaned_row is None:
                    continue

                cleaned.append(cleaned_row)

        return cleaned


    def clean_data(self, row: dict[Any]) -> Optional[AvaliacaoAtendimentoDTO]:
        """
            row: lista de colunas na ordem esperada (13 campos).
            Retorna CleanAvaliacaoAtendimento ou None se a linha for inválida.
        """    

        if len(row) < 13:
            logging.warning("Linha com tamanho inesperado %s", row)
            return None
        
        return AvaliacaoAtendimentoDTO(
            id_da_resposta = self.clean_text(row.get("ID da resposta")) or "",
            nota = self.clean_number(row.get("Nota")),
            comentario = self.clean_text(row.get("Comentário")),
            segunda_nota = self.clean_number(row.get("Segunda Nota")),
            segundo_comentario = self.clean_text(row.get("Segundo Comentário")),
            chat_da_resposta = self.clean_text(row.get("Chat da resposta")),
            ip_do_respondedor = self.clean_text(row.get("IP do respondedor")),
            data_da_resposta = self.parse_datetime(row.get("Data da resposta")),
            nps_da_resposta = self.clean_text(row.get("NPS da resposta")),
            data_de_criacao = self.parse_datetime(row.get("Data de criação")),
            data_da_expiracao = self.parse_datetime(row.get("Data de expiração")),
            usuario_delegado = self.parse_list(row.get("Usuários delegado")),
            grupos_delegado = self.parse_list(row.get("Grupos delegado")),
            usuario = self.get_first(row.get("Usuários delegado")),
            classificacao = self.generate_classification(row.get("Nota"))
        )
    
    def clean_text(self, value: str) -> Optional[str]:
        if value is None:
            return None

        transform = value.strip()

        return transform if transform != "" else None


    def parse_datetime(self, value: str) -> Optional[datetime]:
        if not value:
            return None
        
        transform = value.replace("às", "") \
            .replace("as", "") \
            .strip()
        
        if transform == "":
            return None
        
        return datetime.strptime(transform, "%d/%m/%Y %H:%M")

    def parse_list(self, value: str) -> Optional[str]:

        if value is None:
            return None
        
        if not value:
            return None
        
        transform = value.strip().strip("[]")
        
        if transform in ("[]", ""):
            return None
        
        inner = transform.strip("[]")
        parts = [p.strip().strip("'\"") for p in inner.split(",")]
        return ", ".join(parts).strip()
    
    def clean_number(self, value: int) -> Optional[int]:
        if value is None:
            return None
        
        value = value.strip()
        if value == "":
            return None
        
        return int(value)
    
    def get_first(self, value: str) -> Optional[str]:
        if not value:
            return None
        
        parsed = self.parse_list(value)
        if parsed is None:
            return None
        
        return parsed.split(", ")[0]
    
    def generate_classification(self, value: str):
        
        if value is None:
            return None
        
        if value == "":
            return None
        
        if int(value) >= 9:
            return "Promotores"
        elif int(value) > 6:
            return "Neutros"
        
        return "Detratores"
