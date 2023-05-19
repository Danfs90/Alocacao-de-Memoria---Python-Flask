"""
NOME DO PROGRAMA: Projeto de alocação de Memoria

VERSÃO 1.0

SINTAXE: Educacional

DESCRIÇÃO: O software tem como objetivo simular o funcionamento da alocação de memoria
que os sistemas operacionais fazem automaticamente, esse projeto foi pensado para deixar mais claro
a como os processos sao alocados e redistribuidos na memoria de um computador.

LINGUAGENS BACKEND: Python

LINGUAGENS FRONTEND: Javascript, HTML & CSS (Bootstrap)

FRAMEWORKS: Flask

SISTEMAS OPERACIONAIS: Software roda via web logo nao temos nenhuma restrição para OS.

REQUISITOS: Acesso a internet pois o bootstrap utiliza seus repositorio.

AUTORES: Danilo Ferreira dos Santos e Matheus Tomaz

CRIAÇÃO: 08/05/2023

ALTERAÇÕES: 09/05/2023 - Adicionado visual na pagina web
            10/05/2023 - Correções de bugs
            16/05/2023 - Testes de QA(Aprovado)
    
            
TODAS AS BILIOTECAS UTILIZADAS ESTÃO LOCALIZADAS NO ARQUIVO requirements.txt | Para que sejam importadas deve-se utilizar o seguinte comando no terminal "pip install -requirements.txt"
"""


"""

Importação das bibliotecas que serão utilizadas

"""


import json
from datetime import datetime
from flask import Flask, flash, render_template, request
app = Flask(__name__)
app.secret_key = "abc"

# Criamos um array de tamanho 50 com todos os indices vazio, apos isso criamos uma copia do array de memoria

memoria = [''] * 50
memoria_final = memoria.copy()

"""

Função que verifica se a espaço para alocar o processo

"""


def find_first_fit(memoria, tamanho_processo):
    for i in range(len(memoria)):
        if memoria[i] == '':
            verificacao = i
            while verificacao < len(memoria) and memoria[verificacao] == '':
                if verificacao - i + 1 == tamanho_processo:
                    return i
                verificacao += 1
    return -1


"""

Função que organiza a lista, criando um array com os valores vazios e outra com os não vazio e concatenando ambos.

"""


def reorganizar_memoria():
    global memoria
    valores_vazios = [valor for valor in memoria if valor == '']
    valores_nao_vazios = [valor for valor in memoria if valor != '']
    memoria = valores_nao_vazios + valores_vazios


"""

Nessa etapa indicamos ao framework que receberemos requisições em API, com os metodos POST e GET
"""


@app.route('/', methods=['GET', 'POST'])
def home():
    # O codigo nao permite comentarios por isso utilizaremos o # para cada linha.

    # Aqui indicamos que a variavel memoria será global, para que todas as funções consigam utiliza-la.

    global memoria
    messages = ""
    # Aqui utilizamos um  CASE para verificar qual a solicitação receberemos do frontend, e realizar a função indicada

    if request.method == 'POST':
        opcao = int(request.form['opcao'])

        match opcao:
            # Case 1: Opção que adiciona processo
            case 1:
                tamanho_processo = request.form['tamanho_processo']
                nome_processo = request.form['nome_processo']
                if tamanho_processo.isnumeric() == True and nome_processo != '':
                    tamanho_processo = int(request.form['tamanho_processo'])
                    nome_processo = nome_processo.upper().strip()
                    index = find_first_fit(memoria, tamanho_processo)

                    if index == -1:  # Sinaliza um overflow na aplicação
                        flash(
                            "Não há espaço suficiente para alocar a informação. Aloque uma quantidade menor ou apague um processo existente.")

                    else:
                        # Aloca o processo no primerio espaço disponivel
                        for i in range(index, index + tamanho_processo):
                            memoria[i] = nome_processo

                        flash("Processo alocado com sucesso!")
                else:

                    flash("1")
                    return render_template('index.html', memoria_final=memoria_final, memoria=memoria, messages=messages)
            # Case 2: Opção que remove o processo
            case 2:
                nome_processo = request.form['nome_processo']
                nome_processo = nome_processo.upper().strip()
                if nome_processo not in memoria:  # Valida o nome do processo dentro do array
                    flash("ERRO! Esse processo não existe no bloco.")
                    memoria = memoria
                else:  # Esse for valida item por item e caso localize o processo ele altera para vazio
                    for i in range(len(memoria)):
                        if memoria[i] == nome_processo:
                            memoria[i] = ""

                    flash("Processo removido com sucesso!")
            # Case 3: Opção para reorganizar a lista de processos
            case 3:
                value = [valor for valor in memoria if valor != '']
                if len(value) == 50:
                    flash("2")
                    return render_template('index.html', memoria_final=memoria_final, memoria=memoria, messages=messages)
                else:
                    reorganizar_memoria()
                    flash("Memória reorganizada com sucesso!")
            # Case 4: Salva o array no Json
            case 4:

                date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                memoria_json = json.dumps(memoria)
                with open(f'memoria_{date}.json', 'w') as file:
                    file.write(memoria_json)

                flash("Log salvo com sucesso!")
                return render_template('index.html', memoria_final=memoria_final, memoria=memoria, messages=messages)
            case 0:
                flash("0")
                return render_template('index.html', memoria_final=memoria_final, memoria=memoria, messages=messages)

            case _:
                messages = ""

    return render_template('index.html', memoria_final=memoria_final, memoria=memoria, messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
