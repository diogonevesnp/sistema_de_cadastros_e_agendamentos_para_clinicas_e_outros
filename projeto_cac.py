import json
from pathlib import Path
from datetime import datetime

ARQUIVO = Path("agendamentos.json")

# --- Funções utilitárias ---
# (Sem alterações aqui)
def carregar_agendamentos():
    if ARQUIVO.exists():
        if ARQUIVO.stat().st_size == 0:
            return []
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return [d for d in dados if "CPF" in d]
        except json.JSONDecodeError:
            print(f"\nAviso: {ARQUIVO} está corrompido. Iniciando com uma lista limpa.\n")
            return []
    return []

def salvar_agendamentos(agendamentos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, indent=4, ensure_ascii=False)

def validar_data(data_str):
    try:
        return datetime.strptime(data_str, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        return None

def validar_horario(hora_str):
    try:
        return datetime.strptime(hora_str, "%H:%M").strftime("%H:%M")
    except ValueError:
        return None

def formatar_telefone(ddd, telefone):
    numero = str(telefone).zfill(9) 
    parte1 = numero[1:5]
    parte2 = numero[5:]
    return f"({ddd}) 9 {parte1}-{parte2}"

# --- Cadastro (TOTALMENTE ALTERADA) ---

def cadastrar(agendamentos):
    print("\n--- Novo Cadastro de Paciente ---")
    print("Digite os dados abaixo. Pressione Enter para campos não obrigatórios se aplicável.")

    # NOVO: Loop de validação para Nome
    while True:
        nome = input("Digite o primeiro nome: ").title().strip()
        if not nome:
            print("Erro: o nome não pode ficar em branco!")
        else:
            break # Sai do loop se o nome for válido

    # NOVO: Loop de validação para Sobrenome
    while True:
        sobrenome = input("Sobrenome: ").title().strip()
        if not sobrenome:
            print("Erro: o sobrenome não pode ficar em branco!")
        else:
            break # Sai do loop

    # NOVO: Loop de validação para CPF (com duas checagens)
    while True:
        cpf = input("CPF (somente números, 11 dígitos): ").strip()
        
        # 1. Validação de formato
        if not cpf.isdigit() or len(cpf) != 11:
            print("Erro: CPF deve conter exatamente 11 números!")
            continue # Volta para o início do loop 'while'
        
        # 2. Validação de duplicidade
        cpf_existe = False
        for agendamento in agendamentos:
            if agendamento["CPF"] == cpf:
                cpf_existe = True
                break # Encontrou um CPF igual, para o loop 'for'
        
        if cpf_existe:
            print("Erro: Já existe um paciente com este CPF.")
            continue # Volta para o início do loop 'while'
        
        # Se passou pelas duas validações, sai do loop
        break

    # NOVO: Loop de validação para Data de Nascimento
    while True:
        data_nasc_str = input("Data de nascimento (DD/MM/AAAA): ").strip()
        data_nasc_valida = validar_data(data_nasc_str)
        if not data_nasc_valida:
            print("Erro: data inválida! Use o formato DD/MM/AAAA.")
        else:
            break # Sai do loop

    # NOVO: Loop de validação para Estado
    while True:
        estado = input("Estado (sigla, ex: PR): ").upper().strip()
        if len(estado) != 2 or not estado.isalpha():
            print("Erro: estado inválido! Digite apenas a sigla de 2 letras.")
        else:
            break # Sai do loop

    # NOVO: Loop de validação para Cidade
    while True:
        cidade = input("Cidade: ").title().strip()
        if not cidade:
            print("Erro: cidade não pode ficar em branco!")
        else:
            break # Sai do loop

    # NOVO: Loop de validação para Endereço
    while True:
        endereco = input("Endereço: ").title().strip()
        if not endereco:
            print("Erro: endereço não pode ficar em branco!")
        else:
            break # Sai do loop

    # NOVO: Loop de validação para DDD
    while True:
        ddd = input("DDD (2 dígitos): ").strip()
        if not ddd.isdigit() or len(ddd) != 2:
            print("Erro: DDD inválido! Digite 2 números.")
        else:
            break # Sai do loop
    
    # NOVO: Loop de validação para Número
    while True:
        numero = input("Número de celular (9 dígitos, ex: 9XXXXXXX): ").strip()
        if not numero.isdigit() or len(numero) != 9 or not numero.startswith("9"):
            print("Erro: número inválido! Deve ter 9 dígitos e começar com 9.")
        else:
            break # Sai do loop
    telefone = numero # Atribui o número validado

    # NOVO: Loop de validação para Especialista
    while True:
        especialista = input("Qual médico: ").title().strip()
        if not especialista:
            print("Erro: especialista não pode ficar em branco!")
        else:
            break # Sai do loop

    # NOVO: Loop de validação para Horário
    while True:
        horario_str = input("Horário da consulta (HH:MM): ").strip()
        horario_valido = validar_horario(horario_str)
        if not horario_valido:
            print("Erro: horário inválido! Use o formato HH:MM (ex: 14:30).")
        else:
            break # Sai do loop

    # O restante do código (criação do dicionário) permanece o mesmo
    agendado = {
        "Nome": nome,
        "Sobrenome": sobrenome,
        "CPF": cpf,
        "Data de Nascimento": data_nasc_valida,
        "Estado": estado,
        "Cidade": cidade,
        "Endereço": endereco,
        "DDD": ddd,
        "Telefone": telefone,
        "Especialista": especialista,
        "Horário": horario_valido,
        "Status": "Ativo"
    }
    agendamentos.append(agendado)
    salvar_agendamentos(agendamentos)
    print("\n✅ Paciente cadastrado com sucesso!\n")

# --- Listagem ---
# (Sem alterações aqui)
def listar(agendamentos):
    if not agendamentos:
        print("\nNenhum paciente cadastrado ainda.\n")
        return

    print("\n <<< PACIENTES CADASTRADOS >>>")
    separador = "-" * 40 
    print(separador)

    for i, agendamento in enumerate(agendamentos, start=1):
        print(f"PACIENTE #{i}")
        telefone_formatado = formatar_telefone(agendamento['DDD'], agendamento['Telefone'])
        largura_label = 18 
        
        print(f"  {'Nome completo:':<{largura_label}} {agendamento['Nome']} {agendamento['Sobrenome']}")
        print(f"  {'CPF:':<{largura_label}} {agendamento['CPF']}")
        print(f"  {'Nascimento:':<{largura_label}} {agendamento['Data de Nascimento']}")
        print(f"  {'Status:':<{largura_label}} {agendamento['Status']}")
        print(f"  {'Contato:':<{largura_label}} {telefone_formatado}")
        print(f"  {'Endereço:':<{largura_label}} {agendamento['Endereço']}")
        print(f"  {'Local:':<{largura_label}} {agendamento['Cidade']} - {agendamento['Estado']}")
        print(f"  {'Consulta com:':<{largura_label}} {agendamento['Especialista']}")
        print(f"  {'Horário:':<{largura_label}} {agendamento['Horário']}")
        print(separador)
    print()

# --- Excluir paciente pelo CPF ---
# (Sem alterações aqui)
def excluir(agendamentos):
    cpf = input("Digite o CPF (11 dígitos) do paciente a excluir: ").strip()
    
    paciente_encontrado = None
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            paciente_encontrado = agendamento
            break

    if paciente_encontrado:
        agendamentos.remove(paciente_encontrado)
        salvar_agendamentos(agendamentos)
        print("✅ Paciente excluído com sucesso!")
    else:
        print("Paciente não encontrado.")

# --- Editar paciente pelo CPF (ALTERADA) ---

def editar(agendamentos):
    cpf = input("Digite o CPF (11 dígitos) do paciente a editar: ").strip()
    paciente_encontrado = None
    
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            paciente_encontrado = agendamento
            break
            
    if not paciente_encontrado:
        print("Paciente não encontrado.")
        return

    print("\n--- Editando Paciente ---")
    print("Deixe o campo em branco (apenas pressione Enter) para manter o valor atual.")
    
    # NOVO: Loop de validação para Nome na edição
    while True:
        novo_nome = input(f"Nome ({paciente_encontrado['Nome']}): ").title().strip()
        if not novo_nome:
            break # Usuário apertou Enter, mantém o valor antigo e sai do loop
        
        # Se o usuário digitou algo, consideramos válido
        paciente_encontrado['Nome'] = novo_nome
        break

    # NOVO: Loop de validação para Sobrenome na edição
    while True:
        novo_sobrenome = input(f"Sobrenome ({paciente_encontrado['Sobrenome']}): ").title().strip()
        if not novo_sobrenome:
            break # Mantém o valor antigo
        
        paciente_encontrado['Sobrenome'] = novo_sobrenome
        break

    # NOVO: Loop de validação para Endereço na edição
    while True:
        novo_endereco = input(f"Endereço ({paciente_encontrado['Endereço']}): ").title().strip()
        if not novo_endereco:
            break # Mantém o valor antigo
        
        paciente_encontrado['Endereço'] = novo_endereco
        break

    # Esta lógica de loop para o Horário já estava correta e agora é padrão
    while True:
        novo_horario_str = input(f"Horário ({paciente_encontrado['Horário']}): ").strip()
        if not novo_horario_str:
            break # Mantém o valor antigo
        
        novo_horario_valido = validar_horario(novo_horario_str)
        if novo_horario_valido:
            paciente_encontrado['Horário'] = novo_horario_valido
            break # Novo horário é válido
        else:
            print("Erro: horário inválido (formato HH:MM). Tente novamente.")

    salvar_agendamentos(agendamentos)
    print("✅ Paciente atualizado com sucesso!")

# --- Alterar status pelo CPF ---
# (Sem alterações aqui)
def alterar_status(agendamentos):
    cpf = input("Digite o CPF (11 dígitos) do paciente: ").strip()
    
    paciente_encontrado = None
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            paciente_encontrado = agendamento
            break
            
    if not paciente_encontrado:
        print("Paciente não encontrado.")
        return

    print(f"\nAlterando status para: {paciente_encontrado['Nome']} {paciente_encontrado['Sobrenome']}")
    print(f"Status Atual: {paciente_encontrado['Status']}")
    print("-------------------------")
    print("1 - Cancelado")
    print("2 - Atendimento Realizado")
    print("3 - Ativo")
    opcao = input("Escolha o novo status (ou deixe em branco para cancelar): ")
    
    novo_status = None
    if opcao == "1":
        novo_status = "Cancelado"
    elif opcao == "2":
        novo_status = "Atendimento Realado"
    elif opcao == "3":
        novo_status = "Ativo"
    elif not opcao:
        print("Alteração de status cancelada.")
        return
    else:
        print("Opção inválida.")
        return

    paciente_encontrado["Status"] = novo_status
    salvar_agendamentos(agendamentos)
    print("✅ Status atualizado com sucesso!")

# --- Programa principal ---
# (Sem alterações aqui)
def main():
    agendamentos = carregar_agendamentos()

    while True:
        print("\n===== MENU CLÍNICA MWLTYNHO =====")
        print("1 - Cadastrar paciente")
        print("2 - Listar pacientes")
        print("3 - Excluir paciente")
        print("4. - Editar paciente")
        print("5 - Alterar status da consulta")
        print("6 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar(agendamentos)
        elif opcao == "2":
            listar(agendamentos)
        elif opcao == "3":
            excluir(agendamentos)
        elif opcao == "4":
            editar(agendamentos)
        elif opcao == "5":
            alterar_status(agendamentos)
        elif opcao == "6":
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.\n")

if __name__ == "__main__":
    main()