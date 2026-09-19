import sqlite3


def conectar_banco():
    conexao = sqlite3.connect(
        "conecta_servicos.db",
        timeout=10
    )

    conexao.row_factory = sqlite3.Row

    return conexao


def criar_tabelas():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT,
            tipo TEXT NOT NULL,
            cidade TEXT,
            data_cadastro TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            categoria TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            servico_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            cidade TEXT NOT NULL,
            data_solicitacao TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
            FOREIGN KEY (servico_id) REFERENCES servicos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS propostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitacao_id INTEGER NOT NULL,
            profissional_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            mensagem TEXT,
            data_proposta TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (solicitacao_id) REFERENCES solicitacoes(id),
            FOREIGN KEY (profissional_id) REFERENCES usuarios(id)
        )
    """)

    conexao.commit()
    conexao.close()

    

def inserir_servicos_iniciais():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    servicos = [
        ("Troca de fechadura", "Troca ou instalação de fechaduras residenciais.", "Reparos e manutenção"),
        ("Troca de corrediças de móveis", "Troca de corrediças em gavetas e móveis.", "Reparos e manutenção"),
        ("Regulagem de portas e gavetas de móveis", "Regulagem e alinhamento de portas e gavetas de móveis.", "Reparos e manutenção"),
        ("Troca de dobradiças", "Troca de dobradiças de portas e móveis.", "Reparos e manutenção"),
        ("Instalação de maçaneta", "Instalação ou substituição de maçanetas.", "Reparos e manutenção"),
        ("Instalação de porta", "Instalação de portas residenciais.", "Reparos e manutenção"),
        ("Pequenos reparos elétricos", "Execução de pequenos reparos e ajustes elétricos.", "Reparos e manutenção"),
        ("Troca de tomadas e interruptores", "Troca e instalação de tomadas e interruptores.", "Reparos e manutenção"),
        ("Instalação de luminárias", "Instalação de luminárias e equipamentos de iluminação.", "Reparos e manutenção"),
        ("Pequenos reparos hidráulicos", "Execução de pequenos reparos hidráulicos residenciais.", "Reparos e manutenção"),
        ("Troca de torneira", "Troca e instalação de torneiras.", "Reparos e manutenção"),
        ("Desentupimento", "Serviço de desentupimento residencial.", "Reparos e manutenção"),

        ("Montagem de móveis", "Montagem de móveis residenciais.", "Montagem e instalação"),
        ("Instalação de prateleiras", "Instalação de prateleiras em paredes.", "Montagem e instalação"),
        ("Instalação de nichos", "Instalação de nichos decorativos e funcionais.", "Montagem e instalação"),
        ("Instalação de painéis", "Instalação de painéis decorativos e para televisão.", "Montagem e instalação"),
        ("Instalação de suportes de TV", "Instalação de suportes para televisão.", "Montagem e instalação"),
        ("Instalação de varal", "Instalação de varais de parede ou teto.", "Montagem e instalação"),
        ("Instalação de cortinas", "Instalação de cortinas e seus suportes.", "Montagem e instalação"),
        ("Instalação de acessórios de casa", "Instalação de acessórios e itens para residência.", "Montagem e instalação"),

        ("Pintura de portas", "Pintura e acabamento de portas.", "Pintura"),
        ("Pintura de móveis", "Pintura e renovação de móveis.", "Pintura"),
        ("Pintura de paredes", "Pintura de paredes e ambientes residenciais.", "Pintura"),
        ("Pequenos retoques de pintura pós-obra", "Pequenos reparos e retoques de pintura após obras.", "Pintura"),

        ("Corte de grama", "Corte e manutenção básica de gramados.", "Jardim e área externa"),
        ("Poda de árvores", "Poda e manutenção de árvores.", "Jardim e área externa"),
        ("Manutenção de jardim", "Manutenção e cuidados gerais com jardins.", "Jardim e área externa"),

        ("Limpeza residencial", "Limpeza geral de residências.", "Limpeza"),
        ("Limpeza pós-obra", "Limpeza de ambientes após obras e reformas.", "Limpeza"),
        ("Limpeza de vidros", "Limpeza de vidros e janelas.", "Limpeza"),
        ("Limpeza de quintal", "Limpeza e organização de quintais.", "Limpeza"),
        ("Limpeza de piscina", "Limpeza e manutenção básica de piscinas.", "Limpeza"),

        ("Lavagem de sofá", "Lavagem e higienização de sofás.", "Serviços residenciais"),
        ("Dedetização", "Serviço de controle de pragas em ambientes residenciais.", "Serviços residenciais"),
        ("Montagem e desmontagem para mudança", "Montagem e desmontagem de móveis para mudanças.", "Serviços residenciais"),
        ("Pequenos serviços de mudança", "Auxílio em pequenos serviços relacionados a mudanças.", "Serviços residenciais"),

        ("Instalação de câmera de segurança", "Instalação de câmeras de segurança residenciais.", "Tecnologia"),
        ("Configuração de Smart TV", "Configuração e instalação de recursos de Smart TVs.", "Tecnologia")
    ]

    for nome, descricao, categoria in servicos:
        cursor.execute(
            "SELECT id FROM servicos WHERE nome = ?",
            (nome,)
        )

        servico_existente = cursor.fetchone()

        if servico_existente is None:
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