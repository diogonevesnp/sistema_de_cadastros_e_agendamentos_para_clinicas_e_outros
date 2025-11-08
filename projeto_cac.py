import json
from pathlib import Path
from datetime import datetime

ARQUIVO = Path("agendamentos.json")

# --- Funções utilitárias ---

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

# --- Helper de Impressão (ALTERADA) ---
def imprimir_paciente_detalhado(agendamento, indice=None):
    """Imprime um bloco formatado com os dados de um paciente."""
    
    if indice:
        print(f"PACIENTE #{indice}")
    
    telefone_formatado = formatar_telefone(agendamento['DDD'], agendamento['Telefone'])
    largura_label = 19 # Aumentei um pouco a largura para os novos campos
    
    print(f"  {'Nome completo:':<{largura_label}} {agendamento['Nome']} {agendamento['Sobrenome']}")
    print(f"  {'CPF:':<{largura_label}} {agendamento['CPF']}")
    print(f"  {'Nascimento:':<{largura_label}} {agendamento['Data de Nascimento']}")
    print(f"  {'Status:':<{largura_label}} {agendamento['Status']}")
    print(f"  {'Contato:':<{largura_label}} {telefone_formatado}")
    print(f"  {'Endereço:':<{largura_label}} {agendamento['Endereço']}")
    print(f"  {'Local:':<{largura_label}} {agendamento['Cidade']} - {agendamento['Estado']}")
    print(f"  {'Consulta com:':<{largura_label}} {agendamento['Especialista']}")
    print(f"  {'Horário Início:':<{largura_label}} {agendamento['Horário']}")
    
    # NOVO: Imprime a Hora Final (se existir)
    print(f"  {'Horário Final:':<{largura_label}} {agendamento.get('HoraFinal', 'N/A')}")
    # NOVO: Imprime os timestamps
    print(f"  {'Data de Cadastro:':<{largura_label}} {agendamento.get('DataCadastro', 'N/A')}")
    print(f"  {'Última Modificação:':<{largura_label}} {agendamento.get('UltimaModificacao', 'N/A')}")


# --- Cadastro (ALTERADA) ---
def cadastrar(agendamentos):
    print("\n--- Novo Cadastro de Paciente ---")
    
    # (Loops de validação 'while True' ... sem alteração)
    while True:
        nome = input("Digite o primeiro nome: ").title().strip()
        if nome: break
        print("Erro: o nome não pode ficar em branco!")
    while True:
        sobrenome = input("Sobrenome: ").title().strip()
        if sobrenome: break
        print("Erro: o sobrenome não pode ficar em branco!")
    while True:
        cpf = input("CPF (somente números, 11 dígitos): ").strip()
        if not cpf.isdigit() or len(cpf) != 11:
            print("Erro: CPF deve conter exatamente 11 números!")
            continue
        cpf_existe = any(ag["CPF"] == cpf for ag in agendamentos)
        if cpf_existe:
            print("Erro: Já existe um paciente com este CPF.")
            continue
        break
    while True:
        data_nasc_str = input("Data de nascimento (DD/MM/AAAA): ").strip()
        data_nasc_valida = validar_data(data_nasc_str)
        if data_nasc_valida: break
        print("Erro: data inválida! Use o formato DD/MM/AAAA.")
    while True:
        estado = input("Estado (sigla, ex: PR): ").upper().strip()
        if len(estado) == 2 and estado.isalpha(): break
        print("Erro: estado inválido! Digite apenas a sigla de 2 letras.")
    while True:
        cidade = input("Cidade: ").title().strip()
        if cidade: break
        print("Erro: cidade não pode ficar em branco!")
    while True:
        endereco = input("Endereço: ").title().strip()
        if endereco: break
        print("Erro: endereço não pode ficar em branco!")
    while True:
        ddd = input("DDD (2 dígitos): ").strip()
        if ddd.isdigit() and len(ddd) == 2: break
        print("Erro: DDD inválido! Digite 2 números.")
    while True:
        numero = input("Número de celular (9 dígitos, ex: 9XXXXXXX): ").strip()
        if numero.isdigit() and len(numero) == 9 and numero.startswith("9"): break
        print("Erro: número inválido! Deve ter 9 dígitos e começar com 9.")
    telefone = numero
    while True:
        especialista = input("Qual médico: ").title().strip()
        if especialista: break
        print("Erro: especialista não pode ficar em branco!")
    while True:
        horario_str = input("Horário da consulta (HH:MM): ").strip()
        horario_valido = validar_horario(horario_str)
        if horario_valido: break
        print("Erro: horário inválido! Use o formato HH:MM (ex: 14:30).")

    # Pega a data e hora do cadastro
    data_cadastro_str = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

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
        "Horário": horario_valido, # Horário de Início
        "HoraFinal": "N/A", # NOVO: Inicializa Hora Final
        "DataCadastro": data_cadastro_str, 
        "UltimaModificacao": "N/A", # NOVO: Inicializa Timestamp de modificação
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

    print("\n <<< PACIENTES CADASTRADOS (TODOS) >>>")
    separador = "-" * 40 
    print(separador)

    for i, agendamento in enumerate(agendamentos, start=1):
        # Chama a função helper de impressão
        imprimir_paciente_detalhado(agendamento, indice=i)
        print(separador)
    
    print()

# --- Excluir paciente pelo CPF ---
# (Sem alterações)
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
    
    # (Loops de validação... sem alteração)
    while True:
        novo_nome = input(f"Nome ({paciente_encontrado['Nome']}): ").title().strip()
        if not novo_nome: break
        paciente_encontrado['Nome'] = novo_nome
        break
    while True:
        novo_sobrenome = input(f"Sobrenome ({paciente_encontrado['Sobrenome']}): ").title().strip()
        if not novo_sobrenome: break
        paciente_encontrado['Sobrenome'] = novo_sobrenome
        break
    while True:
        novo_endereco = input(f"Endereço ({paciente_encontrado['Endereço']}): ").title().strip()
        if not novo_endereco: break
        paciente_encontrado['Endereço'] = novo_endereco
        break
    while True:
        novo_horario_str = input(f"Horário ({paciente_encontrado['Horário']}): ").strip()
        if not novo_horario_str: break
        novo_horario_valido = validar_horario(novo_horario_str)
        if novo_horario_valido:
            paciente_encontrado['Horário'] = novo_horario_valido
            break
        else:
            print("Erro: horário inválido (formato HH:MM). Tente novamente.")

    # NOVO: Atualiza o timestamp de modificação
    paciente_encontrado["UltimaModificacao"] = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    salvar_agendamentos(agendamentos)
    print("✅ Paciente atualizado com sucesso!")

# --- Alterar status pelo CPF (TOTALMENTE ALTERADA) ---
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
        # Limpa a hora final se for cancelado (opcional, mas limpo)
        paciente_encontrado["HoraFinal"] = "N/A"
    elif opcao == "2":
        novo_status = "Atendimento Realizado"
        
        # NOVO: Pede a hora final da consulta
        while True:
            hora_final_str = input("Digite a HORA FINAL da consulta (HH:MM): ").strip()
            if not hora_final_str:
                print("Erro: A hora final é obrigatória para marcar como 'Realizado'.")
                continue # Força o usuário a digitar
            
            hora_final_valida = validar_horario(hora_final_str)
            
            if hora_final_valida:
                # Validação extra: hora final deve ser depois da inicial
                if hora_final_valida <= paciente_encontrado['Horário']:
                    print(f"Erro: A hora final ({hora_final_valida}) deve ser DEPOIS da hora inicial ({paciente_encontrado['Horário']}).")
                else:
                    paciente_encontrado["HoraFinal"] = hora_final_valida
                    break # Hora final é válida
            else:
                print("Erro: horário inválido (formato HH:MM). Tente novamente.")
                
    elif opcao == "3":
        novo_status = "Ativo"
        # Limpa a hora final se voltar para "Ativo"
        paciente_encontrado["HoraFinal"] = "N/A"
    elif not opcao:
        print("Alteração de status cancelada.")
        return
    else:
        print("Opção inválida.")
        return

    # Atualiza o status e o timestamp de modificação
    paciente_encontrado["Status"] = novo_status
    paciente_encontrado["UltimaModificacao"] = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    
    salvar_agendamentos(agendamentos)
    print("✅ Status atualizado com sucesso!")

# --- Buscar Consultas Realizadas ---
# (Sem alterações)
def mostrar_consultas_realizadas(agendamentos):
    print("\n--- Buscar Consulta Realizada por CPF ---")
    cpf = input("Digite o CPF (11 dígitos) do paciente: ").strip()
    
    if not cpf.isdigit() or len(cpf) != 11:
        print("Erro: Formato de CPF inválido.")
        return

    paciente_encontrado = None
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            paciente_encontrado = agendamento
            break

    if paciente_encontrado:
        if paciente_encontrado["Status"] == "Atendimento Realizado":
            print("\n✅ Paciente encontrado com status 'Atendimento Realizado':\n")
            separador = "-" * 40
            print(separador)
            imprimir_paciente_detalhado(paciente_encontrado) 
            print(separador)
        else:
            print(f"Paciente encontrado, mas o status é '{paciente_encontrado['Status']}', não 'Atendimento Realizado'.")
    else:
        print("Nenhum paciente encontrado com este CPF.")

# --- Programa principal ---
# (Sem alterações no menu)
def main():
    agendamentos = carregar_agendamentos()

    while True:
        print("\n===== MENU CLÍNICA =====")
        print("1 - Cadastrar paciente")
        print("2 - Listar pacientes (Todos)")
        print("3 - Excluir paciente")
        print("4 - Editar paciente")
        print("5 - Alterar status da consulta")
        print("6 - Buscar Consulta Realizada (por CPF)")
        print("7 - Sair")
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
            mostrar_consultas_realizadas(agendamentos)
        elif opcao == "7":
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.\n")

if __name__ == "__main__":
    main()