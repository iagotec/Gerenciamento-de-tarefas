from datetime import datetime, timedelta
import uuid
 
 
PRIORIDADE = ['Urgente', 'Alta', 'Media', 'Baixa']
STATUS = ['Pendente', 'Fazendo', 'Concluida']
ORIGEM = ['Email', 'Telefone', 'Chamado do sistema']
 
 
 
lista_tarefas = []
 
 
 
 
 
def mostrar_opcoes(lista):
    print("função (mostrar_opções) está sendo executada")

    for i, opcao in enumerate(lista, 1):
        print(f"{i} - {opcao}")
 
 
 
def escolher_opcao(lista, mensagem):
    print("função (escolher_opcao) opções está sendo executada")

    while True:
        print(mensagem)
        mostrar_opcoes(lista)
        escolha = input("Escolha uma opção pelo número: ")
        if escolha.isdigit():
            escolha = int(escolha)
            if 1 <= escolha <= len(lista):
                return lista[escolha - 1]
        print(" Opção inválida, tente novamente.\n")
 
 
 
 
def criar_tarefa():
    print("função (criar_tarefa) opções está sendo executada")

    global lista_tarefas
 
 
    titulo = input("Digite o título da tarefa: ")
    prioridade = escolher_opcao(PRIORIDADE, "Escolha a prioridade:")
    origem = escolher_opcao(ORIGEM, "Escolha a origem da tarefa:")
    id_tarefa = uuid.uuid1()
 
    tarefa = {
        'titulo': titulo,
        'prioridade': prioridade,
        'status': 'Pendente',
        'origem': origem,
        'data_conclusao': None,
        'ID': id_tarefa
    }
 
 
    lista_tarefas.append(tarefa)
    print("Tarefa criada com sucesso!")

 
 
def verificar_urgencia():
    print("função (verificar_urgencia) está sendo executada")
    
    global lista_tarefas
 
 
    
    for t in lista_tarefas:
        if t['status'] == 'Fazendo':
            print(f" Já há uma tarefa em andamento: {t['titulo']}")
            return
 
 
   
    for prioridade in PRIORIDADE:
        for tarefa in lista_tarefas:
            if tarefa['prioridade'] == prioridade and tarefa['status'] == 'Pendente':
                tarefa['status'] = 'Fazendo'
                print(f" Tarefa selecionada: {tarefa['titulo']} (Prioridade: {tarefa['prioridade']})")
                return
    print(" Nenhuma tarefa pendente encontrada.")
 
 
 
def atualizar_prioridade():
    print("função (atualizar_prioridade) está sendo executada")
   
    global lista_tarefas
 
 
    if not lista_tarefas:
        print(" Não há tarefas cadastradas.")
        return
 
 
    print("Selecione a tarefa para atualizar a prioridade:")
    for i, t in enumerate(lista_tarefas, 1):
        print(f"{i} - {t['titulo']} (Prioridade atual: {t['prioridade']})")
 
 
    escolha = input("Número da tarefa: ")
 
 
    if not escolha.isdigit() or not (1 <= int(escolha) <= len(lista_tarefas)):
        print(" Opção inválida.")
        return
 
 
    tarefa = lista_tarefas[int(escolha) - 1]
    nova_prioridade = escolher_opcao(PRIORIDADE, "Escolha a nova prioridade:")
    tarefa['prioridade'] = nova_prioridade
    print(f" Prioridade da tarefa '{tarefa['titulo']}' atualizada para {nova_prioridade}.")
 
 
 
def concluir_tarefa():
    print("função (concluir_tarefa) está sendo executada")
    
    global lista_tarefas
 
 
    tarefas_fazendo = [t for t in lista_tarefas if t['status'] == 'Fazendo']
    if not tarefas_fazendo:
        print(" Não há tarefas em execução para concluir.")
        return
 
 
    tarefa = tarefas_fazendo[0]
    tarefa['status'] = 'Concluida'
    tarefa['data_conclusao'] = datetime.now()  
 
 
    data_formatada = tarefa['data_conclusao'].strftime("%d/%m/%Y %H:%M")
    print(f"Tarefa '{tarefa['titulo']}' concluída com sucesso em {data_formatada}!")
 
 
 
def excluir_concluidas_antigas():
    print("função (excluir_concluidas_antigas) está sendo executada")
   
    global lista_tarefas
 
 
    agora = datetime.now()
    antes = len(lista_tarefas)
    lista_tarefas = [
        t for t in lista_tarefas
        if not (t['status'] == 'Concluida' and t['data_conclusao'] and (agora - t['data_conclusao']).days > 7)
    ]
    depois = len(lista_tarefas)
    excluidas = antes - depois
    print(f" {excluidas} tarefa(s) concluída(s) antiga(s) removida(s).")
 
 
 
def mostrar_relatorio():
    print("função (mostrar_relatorio) está sendo executada")
    
    global lista_tarefas
 
 
    if not lista_tarefas:
        print(" Nenhuma tarefa cadastrada.")
        return
 
 
    print("\n RELATÓRIO DE TAREFAS")
    print("-" * 70)
 
 
    for tarefa in lista_tarefas:
        data = tarefa['data_conclusao'].strftime("%d/%m/%Y %H:%M") if tarefa['data_conclusao'] else "-"
        print(
            f"ID_tarefa: {tarefa['ID']} | "
            f"Título: {tarefa['titulo']} | "
            f"Prioridade: {tarefa['prioridade']} | "
            f"Status: {tarefa['status']} | "
            f"Origem: {tarefa['origem']} | "
            f"Data de Conclusão: {data}"
        )
    print("-" * 70)
 
 
 
 
def menu():

    print("função (menu) está sendo executada")

    while True:
        print("\n===== MENU DE OPERAÇÕES =====")
        print("1 - Criar Tarefa")
        print("2 - Verificar Urgência / Pegar Tarefa")
        print("3 - Atualizar Prioridade")
        print("4 - Concluir Tarefa")
        print("5 - Excluir Concluídas Antigas")
        print("6 - Mostrar Relatório")
        print("7 - Sair")

        opcao = input("Escolha uma opção: ")

        try:
            if opcao == '1':
                criar_tarefa()
            elif opcao == '2':
                verificar_urgencia()
            elif opcao == '3':
                atualizar_prioridade()
            elif opcao == '4':
                concluir_tarefa()
            elif opcao == '5':
                excluir_concluidas_antigas()
            elif opcao == '6':
                mostrar_relatorio()
            elif opcao == '7':
                print(" Saindo do sistema...")
                break
            else:
                print(" Opção inválida, tente novamente.")
        except Exception as e:
            print(f"\n Ocorreu um erro inesperado: {e}")
            print("Tente novamente ou verifique os dados inseridos.\n")
menu()