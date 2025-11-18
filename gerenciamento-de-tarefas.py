from datetime import datetime, timedelta
import json
import os

# ==============================
# VARIÁVEIS GLOBAIS
# ==============================
ARQUIVO_TAREFAS = 'tarefas.json'
ARQUIVO_ARQUIVADAS = 'tarefas_arquivadas.json'

PRIORIDADE = ['Urgente', 'Alta', 'Media', 'Baixa']
STATUS = ['Pendente', 'Fazendo', 'Concluida', 'Arquivado', 'Excluida']
ORIGEM = ['Email', 'Telefone', 'Chamado do sistema']

lista_tarefas = []
id_controle = 1   # ID numérico sequencial


# ==============================
# FUNÇÕES DE PERSISTÊNCIA
# ==============================
def carregar_dados():
    """Carrega dados dos arquivos JSON ou cria arquivos vazios se não existirem."""
    print("Executando a função carregar_dados")

    global lista_tarefas, id_controle

    # Criar arquivos se não existirem
    for arquivo in [ARQUIVO_TAREFAS, ARQUIVO_ARQUIVADAS]:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w') as f:
                json.dump([], f)

    # Carregar tarefas
    with open(ARQUIVO_TAREFAS, 'r') as f:
        lista_tarefas = json.load(f)

    # Atualizar ID sequencial
    if lista_tarefas:
        id_controle = max(t['ID'] for t in lista_tarefas) + 1


def salvar_dados():
    """Salva as tarefas no arquivo JSON"""
    print("Executando a função salvar_dados")
    with open(ARQUIVO_TAREFAS, 'w') as f:
        json.dump(lista_tarefas, f, indent=4)


# ==============================
# FUNÇÕES DE APOIO
# ==============================
def mostrar_opcoes(lista):
    """Mostra uma lista numerada de opções."""
    print("função (mostrar_opções) está sendo executada")
    for i, opcao in enumerate(lista, 1):
        print(f"{i} - {opcao}")


def escolher_opcao(lista, mensagem):
    """Exibe opções e retorna uma escolha válida."""
    print("função (escolher_opcao) está sendo executada")
    while True:
        print(mensagem)
        mostrar_opcoes(lista)
        escolha = input("Escolha uma opção pelo número: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(lista):
            return lista[int(escolha) - 1]
        print("Opção inválida! Tente novamente.\n")


# ==============================
# FUNÇÃO: CRIAR TAREFA
# ==============================
def criar_tarefa():
    """Cria uma nova tarefa com ID sequencial."""
    print("Executando a função criar_tarefa")
    global lista_tarefas, id_controle

    titulo = input("Digite o título da tarefa: ")
    prioridade = escolher_opcao(PRIORIDADE, "Escolha a prioridade:")
    origem = escolher_opcao(ORIGEM, "Escolha a origem da tarefa:")

    tarefa = {
        'ID': id_controle,
        'titulo': titulo,
        'prioridade': prioridade,
        'status': 'Pendente',
        'origem': origem,
        'data_criacao': datetime.now().isoformat(),
        'data_conclusao': None
    }

    lista_tarefas.append(tarefa)
    id_controle += 1
    salvar_dados()
    print("Tarefa criada com sucesso!")


# ==============================
# FUNÇÃO: VERIFICAR URGÊNCIA
# ==============================
def verificar_urgencia():
    """Seleciona a próxima tarefa mais urgente e muda status para 'Fazendo'."""
    print("Executando a função verificar_urgencia")
    global lista_tarefas

    for t in lista_tarefas:
        if t['status'] == 'Fazendo':
            print(f"Já existe tarefa em andamento: {t['titulo']}")
            return

    for prioridade in PRIORIDADE:
        for tarefa in lista_tarefas:
            if tarefa['prioridade'] == prioridade and tarefa['status'] == 'Pendente':
                tarefa['status'] = 'Fazendo'
                salvar_dados()
                print(f"Tarefa iniciada: {tarefa['titulo']} (Prioridade {prioridade})")
                return
    print("Nenhuma tarefa pendente encontrada.")


# ==============================
# FUNÇÃO: ATUALIZAR PRIORIDADE
# ==============================
def atualizar_prioridade():
    """Atualiza a prioridade de uma tarefa existente."""
    print("Executando a função atualizar_prioridade")

    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    for i, t in enumerate(lista_tarefas, 1):
        print(f"{i} - {t['titulo']} (Atual: {t['prioridade']})")

    escolha = input("Número da tarefa: ")
    if not escolha.isdigit() or not (1 <= int(escolha) <= len(lista_tarefas)):
        print("Opção inválida.")
        return

    tarefa = lista_tarefas[int(escolha) - 1]
    tarefa['prioridade'] = escolher_opcao(PRIORIDADE, "Escolha a nova prioridade:")
    salvar_dados()
    print("Atualizado com sucesso!")


# ==============================
# FUNÇÃO: CONCLUIR TAREFA
# ==============================
def concluir_tarefa():
    """Marca uma tarefa 'Fazendo' como Concluída, com data de término."""
    print("Executando a função concluir_tarefa")

    tarefas_fazendo = [t for t in lista_tarefas if t['status'] == 'Fazendo']
    if not tarefas_fazendo:
        print("Não há tarefas em andamento.")
        return

    tarefa = tarefas_fazendo[0]
    tarefa['status'] = 'Concluida'
    tarefa['data_conclusao'] = datetime.now().isoformat()
    salvar_dados()
    print(f"Tarefa concluída: {tarefa['titulo']}")


# ==============================
# FUNÇÃO: EXCLUSÃO LÓGICA
# ==============================
def excluir_tarefa():
    """Marca uma tarefa como 'Excluida' (não remove da lista)."""
    print("Executando a função excluir_tarefa")

    for i, t in enumerate(lista_tarefas, 1):
        print(f"{i} - {t['titulo']} (Status: {t['status']})")

    escolha = input("Número da tarefa para excluir: ")
    if escolha.isdigit() and 1 <= int(escolha) <= len(lista_tarefas):
        lista_tarefas[int(escolha) - 1]['status'] = 'Excluida'
        salvar_dados()
        print("Tarefa excluída logicamente!")
    else:
        print("Opção inválida.")


# ==============================
# FUNÇÃO: ARQUIVAR AUTOMATICAMENTE
# ==============================
def arquivar_concluidas_antigas():
    """Arquiva tarefas concluídas há mais de 7 dias."""
    print("Executando a função arquivar_concluidas_antigas")
    global lista_tarefas

    agora = datetime.now()
    novas = []
    arquivadas = []

    for t in lista_tarefas:
        if t['status'] == 'Concluida' and t['data_conclusao']:
            dias = (agora - datetime.fromisoformat(t['data_conclusao'])).days
            if dias > 7:
                t['status'] = 'Arquivado'
                arquivadas.append(t)
                continue
        novas.append(t)

    lista_tarefas = novas

    # Registrar em arquivo separado
    with open(ARQUIVO_ARQUIVADAS, 'r+') as f:
        dados = json.load(f)
        dados.extend(arquivadas)
        f.seek(0)
        json.dump(dados, f, indent=4)

    salvar_dados()
    print(f"{len(arquivadas)} tarefa(s) arquivada(s).")


# ==============================
# RELATÓRIOS
# ==============================
def mostrar_relatorio():
    """Exibe todas as tarefas e tempo de execução (se concluída)."""
    print("Executando a função mostrar_relatorio")
    if not lista_tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    print("\n========== RELATÓRIO DE TAREFAS ==========")
    for t in lista_tarefas:
        tempo = "-"
        if t['data_conclusao']:
            ini = datetime.fromisoformat(t['data_criacao'])
            fim = datetime.fromisoformat(t['data_conclusao'])
            tempo = str(fim - ini)

        print(f"ID: {t['ID']} | {t['titulo']} | {t['prioridade']} | "
              f"{t['status']} | Criado: {t['data_criacao']} | "
              f"Conclusão: {t['data_conclusao']} | Tempo: {tempo}")
    print("===========================================")


def relatorio_arquivadas():
    """Mostra apenas as tarefas arquivadas."""
    print("Executando a função relatorio_arquivadas")
    with open(ARQUIVO_ARQUIVADAS, 'r') as f:
        dados = json.load(f)

    if not dados:
        print("Nenhuma tarefa arquivada.")
        return

    print("\n========== TAREFAS ARQUIVADAS ==========")
    for t in dados:
        print(f"ID: {t['ID']} | {t['titulo']} | {t['prioridade']} | {t['data_conclusao']}")
    print("========================================")


# ==============================
# MENU PRINCIPAL
# ==============================
def menu():
    print("Executando a função menu")

    while True:
        print("\n===== MENU DE OPERAÇÕES =====")
        print("1 - Criar Tarefa")
        print("2 - Verificar Urgência")
        print("3 - Atualizar Prioridade")
        print("4 - Concluir Tarefa")
        print("5 - Excluir Tarefa")
        print("6 - Arquivar Concluídas Antigas")
        print("7 - Relatório Geral")
        print("8 - Relatório Arquivadas")
        print("9 - Sair")

        opcao = input("Escolha uma opção: ")

        try:
            if opcao == '1': criar_tarefa()
            elif opcao == '2': verificar_urgencia()
            elif opcao == '3': atualizar_prioridade()
            elif opcao == '4': concluir_tarefa()
            elif opcao == '5': excluir_tarefa()
            elif opcao == '6': arquivar_concluidas_antigas()
            elif opcao == '7': mostrar_relatorio()
            elif opcao == '8': relatorio_arquivadas()
            elif opcao == '9':
                salvar_dados()
                print("Saindo do sistema...")
                exit()
            else:
                print("Opção inválida.")
        except Exception as e:
            print(f"Erro inesperado: {e}")


# ==============================
# EXECUÇÃO DO PROGRAMA
# ==============================
carregar_dados()
menu()
