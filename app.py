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

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    """
    Exclui um usuário pelo ID.

    ---
    tags:
      - Usuários

    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário que será excluído.
        example: 3

    responses:
      200:
        description: Usuário deletado com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Usuário deletado com sucesso!

      404:
        description: Usuário não encontrado.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Usuário não encontrado.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # restante do seu código continua aqui

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (id,)
    )

    usuario = cursor.fetchone()

    if usuario is None:
        conexao.close()

        return {
            "erro": "Usuário não encontrado."
        }, 404

    cursor.execute(
        "DELETE FROM usuarios WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return {
        "mensagem": "Usuário deletado com sucesso!"
    }


@app.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    """
    Atualiza os dados de um usuário.

    ---
    tags:
      - Usuários

    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário que será atualizado.
        example: 3

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
              example: Carlos Souza Atualizado
            email:
              type: string
              example: carlosnovo@email.com
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
      200:
        description: Usuário atualizado com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Usuário atualizado com sucesso!

      404:
        description: Usuário não encontrado.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Usuário não encontrado.
    """

    dados = request.get_json()

    nome = dados["nome"]
    email = dados["email"]
    telefone = dados["telefone"]
    tipo = dados["tipo"]
    cidade = dados["cidade"]

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (id,)
    )

    usuario = cursor.fetchone()

    if usuario is None:
        conexao.close()

        return {
            "erro": "Usuário não encontrado."
        }, 404

    cursor.execute("""
        UPDATE usuarios
        SET
            nome = ?,
            email = ?,
            telefone = ?,
            tipo = ?,
            cidade = ?
        WHERE id = ?
    """, (
        nome,
        email,
        telefone,
        tipo,
        cidade,
        id
    ))

    conexao.commit()
    conexao.close()

    return {
        "mensagem": "Usuário atualizado com sucesso!"
    }

@app.route("/usuarios/<int:id>", methods=["GET"])
def buscar_usuario(id):
    """
    Busca um usuário pelo ID.

    ---
    tags:
      - Usuários

    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário que será consultado.
        example: 1

    responses:
      200:
        description: Usuário encontrado com sucesso.
        schema:
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

      404:
        description: Usuário não encontrado.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Usuário não encontrado.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = ?",
        (id,)
    )

    usuario = cursor.fetchone()

    conexao.close()

    if usuario is None:
        return {
            "erro": "Usuário não encontrado."
        }, 404

    return dict(usuario)

@app.route("/servicos", methods=["POST"])
def cadastrar_servico():
     """
    Cadastra um novo serviço.

    ---
    tags:
      - Serviços

    consumes:
      - application/json

    parameters:
      - in: body
        name: servico
        required: true
        schema:
          type: object
          required:
            - nome
            - descricao
            - categoria
          properties:
            nome:
              type: string
              example: Instalação de porta
            descricao:
              type: string
              example: Instalação de portas residenciais.
            categoria:
              type: string
              example: Montagem e instalação

    responses:
      201:
        description: Serviço cadastrado com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Serviço cadastrado com sucesso!
    """
     
     dados = request.get_json()

     nome = dados["nome"]
     descricao = dados["descricao"]
     categoria = dados["categoria"]

     conexao = conectar_banco()
     cursor = conexao.cursor()

     cursor.execute("""
        INSERT INTO servicos (
            nome,
            descricao,
            categoria
        )
        VALUES (?, ?, ?)
    """, (
        nome,
        descricao,
        categoria
    ))

     conexao.commit()
     conexao.close()

     return {
        "mensagem": "Serviço cadastrado com sucesso!"
    }, 201

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

@app.route("/propostas", methods=["POST"])
def cadastrar_proposta():
    """
    Envia uma proposta para uma solicitação de serviço.

    ---
    tags:
      - Propostas

    consumes:
      - application/json

    parameters:
      - in: body
        name: proposta
        required: true
        schema:
          type: object
          required:
            - solicitacao_id
            - profissional_id
            - valor
          properties:
            solicitacao_id:
              type: integer
              example: 1
            profissional_id:
              type: integer
              example: 3
            valor:
              type: number
              format: float
              example: 150.00
            mensagem:
              type: string
              example: Posso realizar o servico amanha a tarde.

    responses:
      201:
        description: Proposta enviada com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Proposta enviada com sucesso!
            id:
              type: integer
              example: 1

      404:
        description: Solicitação ou profissional não encontrado.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Solicitação não encontrada.

      400:
        description: O usuário informado não é um profissional.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: O usuário informado não é um profissional.
    """

    dados = request.get_json()

    solicitacao_id = dados["solicitacao_id"]
    profissional_id = dados["profissional_id"]
    valor = dados["valor"]
    mensagem = dados.get("mensagem")

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM solicitacoes WHERE id = ?",
        (solicitacao_id,)
    )

    solicitacao = cursor.fetchone()

    if solicitacao is None:
        conexao.close()

        return {
            "erro": "Solicitação não encontrada."
        }, 404

    cursor.execute(
        "SELECT id, tipo FROM usuarios WHERE id = ?",
        (profissional_id,)
    )

    profissional = cursor.fetchone()

    if profissional is None:
        conexao.close()

        return {
            "erro": "Profissional não encontrado."
        }, 404

    if profissional["tipo"] != "profissional":
        conexao.close()

        return {
            "erro": "O usuário informado não é um profissional."
        }, 400

    cursor.execute("""
        INSERT INTO propostas (
            solicitacao_id,
            profissional_id,
            valor,
            mensagem,
            data_proposta,
            status
        )
        VALUES (?, ?, ?, ?, datetime('now'), ?)
    """, (
        solicitacao_id,
        profissional_id,
        valor,
        mensagem,
        "enviada"
    ))

    conexao.commit()

    proposta_id = cursor.lastrowid

    conexao.close()

    return {
        "mensagem": "Proposta enviada com sucesso!",
        "id": proposta_id
    }, 201

@app.route("/solicitacoes/<int:solicitacao_id>/propostas", methods=["GET"])
def buscar_propostas(solicitacao_id):
    """
    Lista as propostas recebidas para uma solicitação de serviço.

    ---
    tags:
      - Propostas

    parameters:
      - in: path
        name: solicitacao_id
        type: integer
        required: true
        description: ID da solicitação que terá suas propostas consultadas.
        example: 1

    responses:
      200:
        description: Lista de propostas da solicitação.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              solicitacao_id:
                type: integer
                example: 1
              profissional_id:
                type: integer
                example: 3
              profissional_nome:
                type: string
                example: Carlos Souza
              valor:
                type: number
                format: float
                example: 150.00
              mensagem:
                type: string
                example: Posso realizar o servico amanha a tarde.
              data_proposta:
                type: string
                example: "2026-09-19 14:14:36"
              status:
                type: string
                example: enviada

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
        (solicitacao_id,)
    )

    solicitacao = cursor.fetchone()

    if solicitacao is None:
        conexao.close()

        return {
            "erro": "Solicitação não encontrada."
        }, 404

    cursor.execute("""
        SELECT
            propostas.id,
            propostas.solicitacao_id,
            propostas.profissional_id,
            usuarios.nome AS profissional_nome,
            propostas.valor,
            propostas.mensagem,
            propostas.data_proposta,
            propostas.status
        FROM propostas
        JOIN usuarios
            ON propostas.profissional_id = usuarios.id
        WHERE propostas.solicitacao_id = ?
    """, (
        solicitacao_id,
    ))

    propostas = cursor.fetchall()

    conexao.close()

    lista_propostas = []

    for proposta in propostas:
        lista_propostas.append(dict(proposta))

    return lista_propostas

@app.route("/propostas/<int:id>", methods=["GET"])
def buscar_proposta(id):
    """
    Busca uma proposta específica pelo ID.

    ---
    tags:
      - Propostas

    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da proposta que será consultada.
        example: 1

    responses:
      200:
        description: Proposta encontrada com sucesso.
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            solicitacao_id:
              type: integer
              example: 1
            profissional_id:
              type: integer
              example: 3
            profissional_nome:
              type: string
              example: Carlos Souza
            valor:
              type: number
              format: float
              example: 150.00
            mensagem:
              type: string
              example: Posso realizar o servico amanha a tarde.
            data_proposta:
              type: string
              example: "2026-09-19 14:14:36"
            status:
              type: string
              example: aceita

      404:
        description: Proposta não encontrada.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Proposta não encontrada.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            propostas.id,
            propostas.solicitacao_id,
            propostas.profissional_id,
            usuarios.nome AS profissional_nome,
            propostas.valor,
            propostas.mensagem,
            propostas.data_proposta,
            propostas.status
        FROM propostas
        JOIN usuarios
            ON propostas.profissional_id = usuarios.id
        WHERE propostas.id = ?
    """, (
        id,
    ))

    proposta = cursor.fetchone()

    conexao.close()

    if proposta is None:
        return {
            "erro": "Proposta não encontrada."
        }, 404

    return dict(proposta)

@app.route("/propostas/<int:id>", methods=["PUT"])
def atualizar_proposta(id):
    """
    Atualiza o status de uma proposta.

    ---
    tags:
      - Propostas

    consumes:
      - application/json

    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da proposta que será atualizada.
        example: 1

      - in: body
        name: proposta
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum:
                - enviada
                - aceita
                - recusada
              example: aceita

    responses:
      200:
        description: Proposta atualizada com sucesso.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Proposta atualizada com sucesso!

      400:
        description: Status informado é inválido.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: "Status inválido. Use: enviada, aceita ou recusada."

      404:
        description: Proposta não encontrada.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Proposta não encontrada.
    """

    dados = request.get_json()

    status = dados["status"]

    status_validos = [
        "enviada",
        "aceita",
        "recusada"
    ]

    if status not in status_validos:
        return {
            "erro": "Status inválido. Use: enviada, aceita ou recusada."
        }, 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM propostas WHERE id = ?",
        (id,)
    )

    proposta = cursor.fetchone()

    if proposta is None:
        conexao.close()

        return {
            "erro": "Proposta não encontrada."
        }, 404

    cursor.execute("""
        UPDATE propostas
        SET status = ?
        WHERE id = ?
    """, (
        status,
        id
    ))

    if status == "aceita":
        cursor.execute("""
            UPDATE solicitacoes
            SET status = ?
            WHERE id = ?
        """, (
            "aceita",
            proposta["solicitacao_id"]
        ))

    conexao.commit()

    conexao.close()

    return {
        "mensagem": "Proposta atualizada com sucesso!"
    }

if __name__ == "__main__":
    criar_tabelas()
    inserir_servicos_iniciais()
    app.run(debug=True, use_reloader=False)