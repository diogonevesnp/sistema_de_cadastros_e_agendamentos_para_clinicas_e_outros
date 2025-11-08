import json
from pathlib import Path
from datetime import datetime

ARQUIVO = Path("agendamentos.json")

# --- Funções utilitárias ---

def carregar_agendamentos():
    if ARQUIVO.exists():
        
        # NOVO: Checa se o arquivo está vazio (0 bytes)
        # json.load() falha em arquivos vazios
        if ARQUIVO.stat().st_size == 0:
            return []
            
        # ALTERADO: Adicionado try/except para JSON corrompido
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                # Garante que todos os registros tenham CPF (ótima ideia!)
                return [d for d in dados if "CPF" in d]
        except json.JSONDecodeError:
            print(f"\nAviso: {ARQUIVO} está corrompido. Iniciando com uma lista limpa.\n")
            return [] # Retorna uma lista vazia se o arquivo estiver corrompido
            
    return [] # Retorna lista vazia se o arquivo não existir

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
    # Esta função já funciona bem com strings, o str() é inofensivo
    numero = str(telefone).zfill(9) 
    parte1 = numero[1:5]
    parte2 = numero[5:]
    return f"({ddd}) 9 {parte1}-{parte2}"

# --- Cadastro ---

def cadastrar(agendamentos):
    # ALTERADO: Validação de strings para permitir espaços (nomes compostos)
    nome = input("Digite o primeiro nome: ").title().strip()
    if not nome:
        print("Erro: o nome não pode ficar em branco!")
        return

    sobrenome = input("Sobrenome: ").title().strip()
    if not sobrenome:
        print("Erro: o sobrenome não pode ficar em branco!")
        return

    cpf = input("CPF (somente números, 11 dígitos): ").strip()
    if not cpf.isdigit() or len(cpf) != 11:
        print("Erro: CPF deve conter exatamente 11 números!")
        return
    
    # NOVO: Checar se CPF já existe
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            print("Erro: Já existe um paciente com este CPF.")
            return

    data_nasc = input("Data de nascimento (DD/MM/AAAA): ").strip()
    data_nasc_valida = validar_data(data_nasc)
    if not data_nasc_valida:
        print("Erro: data inválida!")
        return

    estado = input("Estado (sigla, ex: PR): ").upper().strip()
    if len(estado) != 2 or not estado.isalpha():
        print("Erro: estado inválido!")
        return

    # ALTERADO: Validação de strings
    cidade = input("Cidade: ").title().strip()
    if not cidade:
        print("Erro: cidade não pode ficar em branco!")
        return

    # ALTERADO: Validação de strings
    endereco = input("Endereço: ").title().strip()
    if not endereco:
        print("Erro: endereço não pode ficar em branco!")
        return

    # ALTERADO: DDD e Telefone agora são STRINGS
    ddd = input("DDD (2 dígitos): ").strip()
    if not ddd.isdigit() or len(ddd) != 2:
        print("Erro: DDD inválido!")
        return
    
    # ALTERADO: Telefone agora é STRING
    numero = input("Número de celular (9 dígitos, ex: 9XXXXXXX): ").strip()
    if not numero.isdigit() or len(numero) != 9 or not numero.startswith("9"):
        print("Erro: número inválido!")
        return
    # 'telefone' agora é a string 'numero'
    telefone = numero 

    # ALTERADO: Validação de strings
    especialista = input("Qual médico: ").title().strip()
    if not especialista:
        print("Erro: especialista inválido!")
        return

    horario = input("Horário da consulta (HH:MM): ").strip()
    horario_valido = validar_horario(horario)
    if not horario_valido:
        print("Erro: horário inválido!")
        return

    agendado = {
        "Nome": nome,
        "Sobrenome": sobrenome,
        "CPF": cpf,
        "Data de Nascimento": data_nasc_valida,
        "Estado": estado,
        "Cidade": cidade,
        "Endereço": endereco,
        "DDD": ddd, # Salvo como string
        "Telefone": telefone, # Salvo como string
        "Especialista": especialista,
        "Horário": horario_valido,
        "Status": "Ativo"
    }
    agendamentos.append(agendado)
    salvar_agendamentos(agendamentos)
    print("\n✅ Paciente cadastrado com sucesso!\n")

# --- Listagem ---

def listar(agendamentos):
    if not agendamentos:
        print("\nNenhum paciente cadastrado ainda.\n")
        return
    print("\n <<< PACIENTES CADASTRADOS >>>")
    print("---------------------------------")
    for agendamento in agendamentos:
        # A formatação de telefone funciona perfeitamente com strings
        telefone_formatado = formatar_telefone(agendamento['DDD'], agendamento['Telefone'])
        print(f"Nome: {agendamento['Nome']} {agendamento['Sobrenome']} | "
              f"CPF: {agendamento.get('CPF', 'N/A')} | "
              f"Nascimento: {agendamento['Data de Nascimento']} | "
              f"Status: {agendamento['Status']}\n"
              f"  Local: {agendamento['Cidade']} / {agendamento['Estado']} | "
              f"Endereço: {agendamento['Endereço']}\n"
              f"  Contato: {telefone_formatado} | "
              f"Médico: {agendamento['Especialista']} | "
              f"Horário: {agendamento['Horário']}")
        print("---------------------------------")
    print()

# --- Excluir paciente pelo CPF ---

def excluir(agendamentos):
    cpf = input("Digite o CPF (11 dígitos) do paciente a excluir: ").strip()
    
    # ALTERADO: Lógica de exclusão mais segura
    # 1. Encontre o paciente
    paciente_encontrado = None
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            paciente_encontrado = agendamento
            break # Para o loop assim que encontrar

    # 2. Remova-o fora do loop
    if paciente_encontrado:
        agendamentos.remove(paciente_encontrado)
        salvar_agendamentos(agendamentos)
        print("✅ Paciente excluído com sucesso!")
    else:
        print("Paciente não encontrado.")

# --- Editar paciente pelo CPF ---

def editar(agendamentos):
    cpf = input("Digite o CPF (11 dígitos) do paciente a editar: ").strip()
    paciente_encontrado = None
    
    # Encontra o paciente
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            paciente_encontrado = agendamento
            break
            
    if not paciente_encontrado:
        print("Paciente não encontrado.")
        return

    # Se encontrou, começa a edição
    print("Deixe em branco para manter o valor atual.")
    
    # ALTERADO: Validação com .strip() para campos de texto
    novo_nome = input(f"Nome ({paciente_encontrado['Nome']}): ").title().strip()
    paciente_encontrado['Nome'] = novo_nome or paciente_encontrado['Nome']

    novo_sobrenome = input(f"Sobrenome ({paciente_encontrado['Sobrenome']}): ").title().strip()
    paciente_encontrado['Sobrenome'] = novo_sobrenome or paciente_encontrado['Sobrenome']
    
    novo_endereco = input(f"Endereço ({paciente_encontrado['Endereço']}): ").title().strip()
    paciente_encontrado['Endereço'] = novo_endereco or paciente_encontrado['Endereço']

    # NOVO: Validação com loop para campos com formato específico (horário)
    while True:
        novo_horario_str = input(f"Horário ({paciente_encontrado['Horário']}): ").strip()
        if not novo_horario_str:
            # Usuário apertou Enter, mantém o antigo
            break 
        
        novo_horario_valido = validar_horario(novo_horario_str)
        if novo_horario_valido:
            paciente_encontrado['Horário'] = novo_horario_valido
            break # Horário novo e válido, sai do loop
        else:
            print("Erro: horário inválido (formato HH:MM). Tente novamente.")

    salvar_agendamentos(agendamentos)
    print("✅ Paciente atualizado com sucesso!")

# --- Alterar status pelo CPF ---

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

    # Se encontrou, mostra o menu de status
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
        novo_status = "Atendimento Realizado"
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

def main():
    agendamentos = carregar_agendamentos()

    while True:
        print("\n===== MENU CLÍNICA =====")
        print("1 - Cadastrar paciente")
        print("2 - Listar pacientes")
        print("3 - Excluir paciente")
        print("4 - Editar paciente")
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