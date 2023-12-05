from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente
import json
import numpy as np


class PacienteSchema(BaseModel):
    """Define como um novo paciente a ser inserido deve ser representado"""

    idade: int = 50
    leucocitos: float = 6000
    basofilos: float = 1
    creatinina: float = 0.60
    proteina_c: float = 250
    hemoglobina: float = 12.6


class PacienteViewSchema(BaseModel):
    """Define como um paciente será retornado"""

    id: int = 1
    idade: int = 50
    leucocitos: float = 6000
    basofilos: float = 1
    creatinina: float = 0.60
    proteina_c: float = 250
    hemoglobina: float = 12.6
    rt_pcr: Optional[int] = None


class PacienteBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no id do paciente.
    """

    id: int = 1


class ListaPacientesSchema(BaseModel):
    """Define como uma lista de pacientes será representada"""

    pacientes: List[PacienteSchema]


class PacienteDelSchema(BaseModel):
    """Define como um paciente para deleção será representado"""

    id: int = 1


# Apresenta apenas os dados de um paciente
def apresenta_paciente(paciente: Paciente):
    """Retorna uma representação do paciente seguindo o schema definido em
    PacienteViewSchema.
    """
    return {
        "id": paciente.id,
        "idade": paciente.idade,
        "leucocitos": paciente.leucocitos,
        "basofilos": paciente.basofilos,
        "creatinina": paciente.creatinina,
        "proteina_c": paciente.proteina_c,
        "hemoglobina": paciente.hemoglobina,
        "rt_pcr": paciente.rt_pcr,
    }


# Apresenta uma lista de pacientes
def apresenta_pacientes(pacientes: List[Paciente]):
    """Retorna uma representação do paciente seguindo o schema definido em
    PacienteViewSchema.
    """
    result = []
    for paciente in pacientes:
        result.append(
            {
                "id": paciente.id,
                "idade": paciente.idade,
                "leucocitos": paciente.leucocitos,
                "basofilos": paciente.basofilos,
                "creatinina": paciente.creatinina,
                "proteina_c": paciente.proteina_c,
                "hemoglobina": paciente.hemoglobina,
                "rt_pcr": paciente.rt_pcr,
            }
        )

    return {"pacientes": result}
