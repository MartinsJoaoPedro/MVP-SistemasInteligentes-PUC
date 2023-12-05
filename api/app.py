from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
import joblib

from sqlalchemy.exc import IntegrityError

from model import Session, Paciente, Model
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
paciente_tag = Tag(
    name="Paciente",
    description="Adição, visualização, remoção e predição de pacientes com covid",
)


# Rota home
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de pacientes
@app.get(
    "/pacientes",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def get_pacientes():
    """Lista todos os pacientes cadastrados na base
    Retorna uma lista de pacientes cadastrados na base.

    Args:
         (str): nome do paciente

    Returns:
        list: lista de pacientes cadastrados na base
    """
    session = Session()

    # Buscando todos os pacientes
    pacientes = session.query(Paciente).all()

    if not pacientes:
        logger.warning("Não há pacientes cadastrados na base :/")
        return {"message": "Não há pacientes cadastrados na base :/"}, 404
    else:
        logger.debug(f"%d pacientes econtrados" % len(pacientes))
        return apresenta_pacientes(pacientes), 200


# Rota de adição de paciente
@app.post(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "400": ErrorSchema, "409": ErrorSchema},
)
def predict(form: PacienteSchema):
    """Adiciona um novo paciente à base de dados
    Retorna uma representação dos pacientes e diagnósticos associados.

    Args:
        idade (int): idade (anos)
        leucocitos (int): número de leucocitos
        basofilos (int): concentração de basofilos
        creatinina (int): pressão creatinina
        proteina_c (int): espessura proteina_c
        hemoglobina (int): número de hemoglobina

    Returns:
        número de : representação do paciente e diagnóstico associado
    """

    # Carregando modelo
    ml_path = "ml_model/covid.pkl"
    scaler = joblib.load("ml_model/scaler.joblib")
    modelo = Model.carrega_modelo(ml_path, scaler)

    paciente = Paciente(
        idade=form.idade,
        leucocitos=form.leucocitos,
        basofilos=form.basofilos,
        creatinina=form.creatinina,
        proteina_c=form.proteina_c,
        hemoglobina=form.hemoglobina,
        rt_pcr=Model.preditor(modelo, form),
    )
    logger.debug(f"Adicionando produto de idade: '{paciente.idade}'")

    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando paciente
        session.add(paciente)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação

        return apresenta_paciente(paciente), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar paciente de idade '{paciente.idade}', {error_msg}"
        )
        return {"message": error_msg}, 400


# Métodos baseados em nome
# Rota de busca de paciente por nome
@app.get(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def get_paciente(query: PacienteBuscaSchema):
    """Faz a busca por um paciente cadastrado na base a partir do nome

    Args:
        nome (str): nome do paciente

    Returns:
        dict: representação do paciente e diagnóstico associado
    """

    paciente_id = query.id
    logger.debug(f"Coletando dados sobre produto #{paciente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()

    if not paciente:
        # se o paciente não foi encontrado
        error_msg = f"Paciente {paciente_id} não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{paciente_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Paciente econtrado: '{paciente.id}'")
        # retorna a representação do paciente
        return apresenta_paciente(paciente), 200


# Rota de remoção de paciente por id
@app.delete(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def delete_paciente(query: PacienteBuscaSchema):
    """Remove um paciente cadastrado na base a partir do id

    Args:
        nome (str): nome do paciente

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    paciente_id = query.id
    logger.debug(f"Deletando dados sobre paciente #{paciente_id}")

    # Criando conexão com a base
    session = Session()

    # Buscando paciente
    paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()

    if not paciente:
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente '{paciente_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(paciente)
        session.commit()
        logger.debug(f"Deletado paciente #{paciente_id}")
        return {"message": f"Paciente {paciente_id} removido com sucesso!"}, 200
