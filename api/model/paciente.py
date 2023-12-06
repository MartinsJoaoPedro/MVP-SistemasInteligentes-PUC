from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


# colunas = idade	rt_pcr	leucocitos	basofilos	creatinina	proteina_c	hemoglobina
class Paciente(Base):
    __tablename__ = "pacientes"

    # entrada
    id = Column(Integer, primary_key=True)
    idade = Column("Idade", Integer)
    leucocitos = Column("Leucocitos", Float)
    basofilos = Column("Basofilos", Float)
    creatinina = Column("Creatinina", Float)
    proteina_c = Column("Proteina_c", Float)
    hemoglobina = Column("hemoglobina", Float)
    # saida
    rt_pcr = Column("Diagnostico", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        idade: int,
        leucocitos: float,
        basofilos: float,
        creatinina: float,
        proteina_c: float,
        hemoglobina: float,
        rt_pcr: float,
        data_insercao: Union[DateTime, None] = None,
    ):
        """
        Cria um Paciente

        Arguments:
            name: nome do paciente
            idade (int): idade (anos)
            leucocitos (int): número de leucocitos
            basofilos (int): concentração de basofilos
            creatinina (int): pressão creatinina
            proteina_c (int): espessura proteina_c
            hemoglobina (int): número de hemoglobina
            rt_pcr: diagnóstico
            data_insercao: data de quando o paciente foi inserido à base
        """
        self.idade = idade
        self.leucocitos = leucocitos
        self.basofilos = basofilos
        self.creatinina = creatinina
        self.proteina_c = proteina_c
        self.hemoglobina = hemoglobina
        self.rt_pcr = rt_pcr

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
