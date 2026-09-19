# Conecta Serviços API

API REST desenvolvida em Python com Flask para um marketplace de pequenos serviços.

O projeto tem como objetivo conectar pessoas que precisam realizar pequenos serviços residenciais com profissionais que podem executar esses serviços.

## Objetivo do projeto

O Conecta Serviços permite que:

- clientes se cadastrem;
- profissionais se cadastrem;
- serviços sejam cadastrados;
- clientes criem solicitações de serviços;
- profissionais enviem propostas;
- clientes consultem as propostas recebidas;
- propostas sejam aceitas ou recusadas.

O projeto foi desenvolvido como um MVP (Minimum Viable Product), priorizando simplicidade, organização e funcionamento das principais funcionalidades.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- Flasgger
- Swagger / OpenAPI

## Estrutura do banco de dados

O banco de dados utiliza quatro tabelas principais:

### usuarios

Armazena os dados dos usuários do sistema.

Principais campos:

- id
- nome
- email
- telefone
- tipo
- cidade
- data_cadastro

### servicos

Armazena os serviços disponíveis na plataforma.

Principais campos:

- id
- nome
- descricao
- categoria

### solicitacoes

Armazena as solicitações de serviços realizadas pelos clientes.

Principais campos:

- id
- cliente_id
- servico_id
- descricao
- cidade
- data_solicitacao
- status

### propostas

Armazena as propostas enviadas pelos profissionais.

Principais campos:

- id
- solicitacao_id
- profissional_id
- valor
- mensagem
- data_proposta
- status

## Relacionamentos

O banco possui relacionamentos entre as tabelas.

Uma solicitação pertence a um cliente e está relacionada a um serviço.

Uma proposta pertence a uma solicitação e está relacionada a um profissional.

Fluxo principal:

Cliente
↓
Solicitação de serviço
↓
Profissionais
↓
Propostas
↓
Cliente aceita uma proposta

## Rotas da API

### Usuários

| Método | Rota | Descrição |
|---|---|---|
| POST | `/usuarios` | Cadastra um usuário |
| GET | `/usuarios` | Lista todos os usuários |
| GET | `/usuarios/{id}` | Busca um usuário pelo ID |
| PUT | `/usuarios/{id}` | Atualiza um usuário |
| DELETE | `/usuarios/{id}` | Exclui um usuário |

### Serviços

| Método | Rota | Descrição |
|---|---|---|
| POST | `/servicos` | Cadastra um serviço |
| GET | `/servicos` | Lista os serviços |

### Solicitações

| Método | Rota | Descrição |
|---|---|---|
| POST | `/solicitacoes` | Cria uma solicitação |
| GET | `/solicitacoes` | Lista as solicitações |

### Propostas

| Método | Rota | Descrição |
|---|---|---|
| POST | `/propostas` | Envia uma proposta |
| GET | `/solicitacoes/{solicitacao_id}/propostas` | Lista propostas de uma solicitação |
| GET | `/propostas/{id}` | Busca uma proposta pelo ID |
| PUT | `/propostas/{id}` | Atualiza o status de uma proposta |

## Swagger

A API possui documentação interativa utilizando Swagger.

Com a aplicação em execução, acesse:

http://127.0.0.1:5000/apidocs/

O Swagger permite visualizar e testar as rotas da API diretamente pelo navegador.

## Como executar o projeto

### 1. Criar o ambiente virtual

No terminal:

```bash
python -m venv .venv