# Atividade SENAI: Gerenciador de Tarefas (Migração para ORM)

Este projeto foi desenvolvido como parte de uma atividade prática do curso no **SENAI**. O objetivo central deste exercício foi realizar a refatoração e migração de um sistema de banco de dados, abandonando o uso de **SQL Bruto (Raw SQL)** em favor de um **ORM (Object-Relational Mapping)** utilizando a biblioteca **SQLAlchemy**.

<img width="462" height="491" alt="Screenshot From 2025-12-09 15-56-36" src="https://github.com/user-attachments/assets/646309b7-64b8-4456-ac3d-8b5ed8041114" />

<img width="1920" height="1080" alt="Screenshot From 2025-12-09 15-57-43" src="https://github.com/user-attachments/assets/be29dabb-2794-4cec-86a6-b1e089c95ac5" />

## 🎯 Objetivo da Atividade

Demonstrar na prática as vantagens de utilizar um ORM em aplicações Python modernas, focando em:
1.  **Abstração:** Substituir queries textuais (`SELECT * FROM...`) por objetos e métodos Python.
2.  **Segurança:** Implementar hashing e criptografia de dados sensíveis.
3.  **Manutenibilidade:** Criar um código mais limpo e fácil de ler.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **SQLAlchemy:** ORM para mapeamento e manipulação do banco de dados.
* **PyMySQL:** Driver para conexão com o banco MySQL.
* **Bcrypt:** Para hashing seguro de senhas (unidirecional).
* **Cryptography (Fernet):** Para criptografia reversível (demonstração acadêmica de armazenamento e decifragem).
* **MySQL:** Sistema gerenciador de banco de dados.

## 📋 Funcionalidades

O sistema é uma aplicação de linha de comando (CLI) que permite:

### Gestão de Usuários
* **Criação:** Cadastro com geração automática de chave de segurança.
* **Segurança Dupla:** O sistema demonstra duas formas de proteger a senha:
    * *Hash (Bcrypt):* Para autenticação segura (padrão de mercado).
    * *Criptografia (Fernet):* Para demonstrar a capacidade de decifrar a informação original (fins didáticos).
* **Listagem:** Visualização dos usuários cadastrados (exibindo o hash e a senha decifrada).

### Gestão de Tarefas
* **CRUD Completo:** Criar, Ler, Atualizar e Deletar tarefas.
* **Relacionamento:** As tarefas são vinculadas aos usuários via Chave Estrangeira (Foreign Key).
* **Status:** Controle de estados (Pendente, Em Andamento, Concluída, Cancelada).

## 🚀 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python instalado e um servidor MySQL rodando (local ou remoto).

### 1. Instalação das Dependências
Execute o comando abaixo no terminal para instalar as bibliotecas necessárias:

```bash
pip install sqlalchemy pymysql bcrypt cryptography
