# CRUD Simples em Python com SQLAlchemy ORM

Este projeto é uma transição de um CRUD originalmente feito com **SQL bruto** para uma versão totalmente estruturada usando **Python + SQLAlchemy ORM**.  
A migração foi desenvolvida como parte de uma atividade do **SENAI**, com foco em boas práticas de acesso a banco, abstração de dados e organização do código.

---

## **Tecnologias Utilizadas**
- Python 3  
- SQLAlchemy ORM  
- PyMySQL  
- MariaDB/MySQL  
- Bcrypt (hash de senha)  
- Cryptography / Fernet (criptografia da senha real)

---

## **Funcionalidades**
- Cadastro de usuários  
- Armazenamento seguro da senha (bcrypt + criptografia simétrica)  
- CRUD completo de tarefas  
- Relacionamento usuário → tarefas  
- Edição de dados  
- Exclusão com cascata  
- Criação automática do banco de dados, caso não exista

---

## **Estrutura do Projeto**
- `main.py` — código principal contendo rotas, modelos e lógica do CRUD  
- `secret.key` — chave usada para criptografia Fernet  
- Banco gerido automaticamente via ORM (tabelas `usuarios` e `tarefas`)

---

## **Objetivo Educacional**
O projeto demonstra:
- Como sair de SQL manual para um ORM completo  
- Como manter segurança de senhas  
- Como estruturar um CRUD limpo e escalável  
- Como aplicar relacionamentos e constraints corretamente  

Projeto simples, porém funcional, construído para fins de aprendizado e prática profissional.
