# Conecta Serviços API

API REST desenvolvida em Python com Flask para o projeto **Conecta Serviços**.

O sistema tem como objetivo conectar pessoas que precisam de pequenos serviços residenciais a profissionais que podem realizar esses serviços.

O projeto foi desenvolvido como MVP (Minimum Viable Product) para a disciplina de Engenharia de Software.

---

## Objetivo do projeto

A API permite:

- cadastrar usuários;
- consultar usuários;
- atualizar usuários;
- excluir usuários;
- cadastrar serviços;
- consultar serviços;
- criar solicitações de serviços;
- consultar solicitações;
- enviar propostas;
- consultar propostas;
- aceitar ou recusar propostas;
- excluir solicitações de serviços;


O projeto prioriza simplicidade, organização e funcionamento das principais funcionalidades de um marketplace de serviços.

---

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- Flasgger
- Swagger / OpenAPI
- Flask-CORS

---

## Estrutura do projeto

```text
Conecta-servicos-api/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore