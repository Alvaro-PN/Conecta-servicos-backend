from flask import Flask, request
from flask_cors import CORS
from database import criar_tabelas, conectar_banco, inserir_servicos_iniciais
from flasgger import Swagger


app = Flask(__name__)
CORS(app)
Swagger(app)

@app.route("/")
def inicio():
    return {
        "mensagem": "API Conecta Serviços funcionando!"
    }

@app.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    """
    Cadastra um novo usuário.

    ---
    tags:
      - Usuários

    consumes:
      - application/json

    parameters:
      - in: body
        name: usuario
        required: true
        schema:
          type: object
          required:
            - nome
            - email
            - telefone
            - tipo
            - cidade
          properties:
            nome:
              type: string
              example: Carlos Souza
            email:
              type: string
              example: carlos@email.com
            telefone:
              type: string
              example: "31988888888"
            tipo:
              type: string
              example: profissional
            cidade:
              type: string
              example: Mariana

    responses:
      201:
        description: Usuário cadastrado com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Usuário cadastrado com sucesso!
    """
    
    dados = request.get_json()

    nome = dados["nome"]
    email = dados["email"]
    telefone = dados["telefone"]
    tipo = dados["tipo"]
    cidade = dados["cidade"]

    conexao = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO usuarios (
                nome,
                email,
                telefone,
                tipo,
                cidade,
                data_cadastro
            )
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (
            nome,
            email,
            telefone,
            tipo,
            cidade
        ))

        conexao.commit()

        return {
    "mensagem": "Usuário cadastrado com sucesso!",
    "id": cursor.lastrowid
        }, 201

    except Exception as erro:
        if conexao:
            conexao.rollback()

        return {
            "erro": str(erro)
        }, 500

    finally:
        if conexao:
            conexao.close()

@app.route("/usuarios", methods=["GET"])
def buscar_usuarios():
    """
    Lista todos os usuários cadastrados.

    ---
    tags:
      - Usuários

    responses:
      200:
        description: Lista de usuários cadastrados.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: Joao da Silva
              email:
                type: string
                example: joao@email.com
              telefone:
                type: string
                example: "31999999999"
              tipo:
                type: string
                example: cliente
              cidade:
                type: string
                example: Mariana
              data_cadastro:
                type: string
                example: "2026-09-19 14:00:00"
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios")

    usuarios = cursor.fetchall()

    conexao.close()

    lista_usuarios = []

    for usuario in usuarios:
        lista_usuarios.append(dict(usuario))

    return lista_usuarios


@app.route("/servicos", methods=["GET"])
def buscar_servicos():
    """
    Lista todos os serviços cadastrados.

    ---
    tags:
      - Serviços

    responses:
      200:
        description: Lista de serviços cadastrados.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: Troca de fechadura
              descricao:
                type: string
                example: Troca ou instalação de fechaduras residenciais.
              categoria:
                type: string
                example: Reparos e manutenção
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM servicos")

    servicos = cursor.fetchall()

    conexao.close()

    lista_servicos = []

    for servico in servicos:
        lista_servicos.append(dict(servico))

    return lista_servicos


@app.route("/solicitacoes", methods=["POST"])
def cadastrar_solicitacao():
    """
    Cria uma nova solicitação de serviço.

    ---
    tags:
      - Solicitações

    consumes:
      - application/json

    parameters:
      - in: body
        name: solicitacao
        required: true
        schema:
          type: object
          required:
            - cliente_id
            - servico_id
            - descricao
            - cidade
          properties:
            cliente_id:
              type: integer
              example: 1
            servico_id:
              type: integer
              example: 1
            descricao:
              type: string
              example: Preciso trocar a fechadura da porta principal.
            cidade:
              type: string
              example: Mariana

    responses:
      201:
        description: Solicitação criada com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Solicitação criada com sucesso!
            id:
              type: integer
              example: 1

      404:
        description: Cliente ou serviço não encontrado.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Cliente não encontrado.
    """

    dados = request.get_json()

    cliente_id = dados["cliente_id"]
    servico_id = dados["servico_id"]
    descricao = dados["descricao"]
    cidade = dados["cidade"]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Verifica se o cliente existe
    cursor.execute(
        "SELECT id FROM usuarios WHERE id = ?",
        (cliente_id,)
    )

    cliente = cursor.fetchone()

    if cliente is None:
        conexao.close()

        return {
            "erro": "Cliente não encontrado."
        }, 404

    # Verifica se o serviço existe
    cursor.execute(
        "SELECT id FROM servicos WHERE id = ?",
        (servico_id,)
    )

    servico = cursor.fetchone()

    if servico is None:
        conexao.close()

        return {
            "erro": "Serviço não encontrado."
        }, 404

    # Cria a solicitação
    cursor.execute("""
        INSERT INTO solicitacoes (
            cliente_id,
            servico_id,
            descricao,
            cidade,
            data_solicitacao,
            status
        )
        VALUES (?, ?, ?, ?, datetime('now'), ?)
    """, (
        cliente_id,
        servico_id,
        descricao,
        cidade,
        "aberta"
    ))

    conexao.commit()

    solicitacao_id = cursor.lastrowid

    conexao.close()

    return {
        "mensagem": "Solicitação criada com sucesso!",
        "id": solicitacao_id
    }, 201

@app.route("/solicitacoes", methods=["GET"])
def buscar_solicitacoes():
    """
    Lista todas as solicitações de serviço cadastradas.

    ---
    tags:
      - Solicitações

    responses:
      200:
        description: Lista de solicitações cadastradas.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              cliente_id:
                type: integer
                example: 1
              cliente_nome:
                type: string
                example: Joao da Silva
              servico_id:
                type: integer
                example: 1
              servico_nome:
                type: string
                example: Troca de fechadura
              servico_categoria:
                type: string
                example: Reparos e manutenção
              descricao:
                type: string
                example: Preciso trocar a fechadura da porta principal.
              cidade:
                type: string
                example: Mariana
              data_solicitacao:
                type: string
                example: "2026-09-19 14:10:00"
              status:
                type: string
                example: aberta
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            solicitacoes.id,
            solicitacoes.cliente_id,
            usuarios.nome AS cliente_nome,
            usuarios.telefone AS cliente_telefone,
            solicitacoes.servico_id,
            servicos.nome AS servico_nome,
            servicos.categoria AS servico_categoria,
            solicitacoes.descricao,
            solicitacoes.cidade,
            solicitacoes.data_solicitacao,
            solicitacoes.status
        FROM solicitacoes
        JOIN usuarios
            ON solicitacoes.cliente_id = usuarios.id
        JOIN servicos
            ON solicitacoes.servico_id = servicos.id
    """)

    solicitacoes = cursor.fetchall()

    conexao.close()


    lista_solicitacoes = []

    for solicitacao in solicitacoes:
        lista_solicitacoes.append({
            "id": solicitacao["id"],
            "cliente_id": solicitacao["cliente_id"],
            "cliente_nome": solicitacao["cliente_nome"],
            "cliente_telefone": solicitacao["cliente_telefone"],
            "servico_id": solicitacao["servico_id"],
            "servico_nome": solicitacao["servico_nome"],
            "servico_categoria": solicitacao["servico_categoria"],
            "descricao": solicitacao["descricao"],
            "cidade": solicitacao["cidade"],
            "data_solicitacao": solicitacao["data_solicitacao"],
            "status": solicitacao["status"]
        })

    return lista_solicitacoes


@app.route("/solicitacoes/<int:id>", methods=["DELETE"])
def deletar_solicitacao(id):
    """
    Exclui uma solicitação de serviço pelo ID.

    ---
    tags:
      - Solicitações

    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da solicitação que será excluída.
        example: 1

    responses:
      200:
        description: Solicitação excluída com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Solicitação excluída com sucesso!

      404:
        description: Solicitação não encontrada.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Solicitação não encontrada.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM solicitacoes WHERE id = ?",
        (id,)
    )

    solicitacao = cursor.fetchone()

    if solicitacao is None:
        conexao.close()

        return {
            "erro": "Solicitação não encontrada."
        }, 404

    # Remove propostas relacionadas à solicitação
    cursor.execute(
        "DELETE FROM propostas WHERE solicitacao_id = ?",
        (id,)
    )

    # Remove a solicitação
    cursor.execute(
        "DELETE FROM solicitacoes WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return {
        "mensagem": "Solicitação excluída com sucesso!"
    }, 200


if __name__ == "__main__":
    criar_tabelas()
    inserir_servicos_iniciais()
    app.run(debug=True, use_reloader=False)