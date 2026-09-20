# Conecta Serviços API

API REST desenvolvida em Python com Flask para um marketplace de pequenos serviços.

O projeto tem como objetivo conectar pessoas que precisam realizar pequenos serviços residenciais com profissionais que podem executar esses serviços.

O projeto foi desenvolvido como MVP (Minimum Viable Product) para a disciplina de Engenharia de Software.

---

## Objetivo do projeto

O Conecta Serviços permite que:

- clientes se cadastrem;
- profissionais se cadastrem;
- serviços sejam cadastrados;
- clientes criem solicitações de serviços;
- profissionais enviem propostas;
- clientes consultem as propostas recebidas;
- clientes aceitem ou recusem propostas.

O projeto prioriza simplicidade, organização e funcionamento das principais funcionalidades do sistema.

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
├── .gitignore
└── conecta_servicos.db