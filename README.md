# 📌 Sistema de Gerenciamento de Tarefas (CLI)

Este projeto é um **sistema de gerenciamento de tarefas via terminal**, desenvolvido em **Python**, utilizando arquivos **JSON** para salvar e carregar dados.  
Ele permite criar tarefas, definir prioridades, concluir, arquivar automaticamente tarefas antigas e gerar relatórios completos.

---

## ✨ Funcionalidades

- ✔ Criar novas tarefas  
- ✔ Definir prioridade e origem  
- ✔ Selecionar automaticamente a tarefa mais urgente  
- ✔ Atualizar prioridade  
- ✔ Concluir tarefas  
- ✔ Exclusão lógica (status "Excluída")  
- ✔ Arquivamento automático após 7 dias  
- ✔ Relatório geral  
- ✔ Relatório de tarefas arquivadas  
- ✔ Salvamento automático em arquivos JSON  

---

## 📂 Estrutura de Arquivos

.
├── tarefas.json # Banco de tarefas ativas
├── tarefas_arquivadas.json # Banco de tarefas arquivadas
├── gerenciador_tarefas.py # Código principal
└── README.md # Documentação

## 🛠️ Como Executar

1. Instale o **Python 3.8+**.
2. Baixe o projeto ou clone o repositório


## 🧩 Detalhes das Funcionalidades
🔹 Criar Tarefa

Define título, prioridade e origem.

Sistema registra a data de criação.

Atribuição automática de ID sequencial.

🔹 Verificar Urgência

O sistema escolhe a próxima tarefa seguindo esta ordem:

Urgente

Alta

Média

Baixa

A tarefa é marcada como Fazendo.

🔹 Atualizar Prioridade

Escolha uma tarefa e defina uma nova prioridade.

🔹 Concluir Tarefa

Marca a tarefa como Concluída

Registra a data de conclusão

Calcula tempo total no relatório

🔹 Exclusão Lógica

O item não é removido do JSON

Apenas recebe o status "Excluída"

🔹 Arquivamento Automático

Tarefas concluídas há mais de 7 dias são movidas para tarefas_arquivadas.json.

# 🛠 Tecnologias Utilizadas

- Python 3

- JSON

Módulos padrão:

- datetime

- json

- os