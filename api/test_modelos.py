import array
import numpy as np
from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url_dados = "database/estudo_covid.csv"
colunas = [
    "idade",
    "rt_pcr",
    "leucocitos",
    "basofilos",
    "creatinina",
    "proteina_c",
    "hemoglobina",
]

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Substitui 'POSITIVO' por 1 e 'NEGATIVO' por 0
dataset = dataset.replace({"POSITIVO": 1, "NEGATIVO": 0})

# Remove as linhas com valores NaN
dataset = dataset.dropna()

"""
# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]
"""
# Separando os dados
# Entrada
X = dataset.iloc[:, [0, 2, 3, 4, 5, 6]]  # seleciona as colunas 1, 3, 4, 5, 6, 7
# Saida
Y = dataset.iloc[:, 1]  # seleciona a coluna 2

Y = Y.astype(int)

print("Valores de entrada X:")
print(X)

print("\nValores de saída y:")
print(Y)


# Método para testar o modelo de Regressão Logística a partir do arquivo correspondente
def test_modelo_lr():
    # Importando o modelo de regressão logística
    lr_path = "ml_model/covid_lr.pkl"
    modelo_lr = Model.carrega_modelo(lr_path)

    # Obtendo as métricas da Regressão Logística
    acuracia_lr, recall_lr, precisao_lr, f1_lr = avaliador.avaliar(modelo_lr, X, Y)

    # Testando as métricas da Regressão Logística
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_lr >= 0.6
    assert recall_lr >= 0.5
    assert precisao_lr >= 0.5
    assert f1_lr >= 0.5


# Método para testar modelo KNN a partir do arquivo correspondente
def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = "ml_model/covid_knn.pkl"
    modelo_knn = Model.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn, recall_knn, precisao_knn, f1_knn = avaliador.avaliar(modelo_knn, X, Y)

    # Testando as métricas do KNN
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_knn >= 0.6
    assert recall_knn >= 0.5
    assert precisao_knn >= 0.5
    assert f1_knn >= 0.5
