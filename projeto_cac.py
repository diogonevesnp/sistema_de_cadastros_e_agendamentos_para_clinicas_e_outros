import json
from pathlib import Path
from datetime import datetime

ARQUIVO = Path("agendamentos.json")

# Funções utilitárias
def carregar_agendamentos():
    if ARQUIVO.exists():
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            # Garante que todos os registros tenham CPF
            return [d for d in dados if "CPF" in d]
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

# Cadastro
def cadastrar(agendamentos):
    nome = input("Digite o primeiro nome: ").title()
    if not nome.isalpha():
        print("Erro: digite apenas letras para o nome!")
        return

    sobrenome = input("Sobrenome: ").title()
    if not sobrenome.isalpha():
        print("Erro: digite apenas letras para o sobrenome!")
        return

    cpf = input("CPF (somente números, 11 dígitos): ")
    if not cpf.isdigit() or len(cpf) != 11:
        print("Erro: CPF deve conter exatamente 11 números!")
        return

    data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
    data_nasc_valida = validar_data(data_nasc)
    if not data_nasc_valida:
        print("Erro: data inválida!")
        return

    estado = input("Estado (sigla, ex: PR): ").upper()
    if len(estado) != 2 or not estado.isalpha():
        print("Erro: estado inválido!")
        return

    cidade = input("Cidade: ").title()
    if not cidade.replace(" ", "").isalpha():
        print("Erro: cidade inválida!")
        return

    endereco = input("Endereço: ").title()

    ddd = input("DDD (2 dígitos): ")
    if not ddd.isdigit() or len(ddd) != 2:
        print("Erro: DDD inválido!")
        return
    ddd = int(ddd)

    numero = input("Número de celular (9 dígitos, ex: 9XXXXXXX): ")
    if not numero.isdigit() or len(numero) != 9 or not numero.startswith("9"):
        print("Erro: número inválido!")
        return
    telefone = int(numero)

    especialista = input("Qual médico: ").title()
    if not especialista.isalpha():
        print("Erro: especialista inválido!")
        return

    horario = input("Horário da consulta (HH:MM): ")
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
        "DDD": ddd,
        "Telefone": telefone,
        "Especialista": especialista,
        "Horário": horario_valido,
        "Status": "Ativo"
    }
    agendamentos.append(agendado)
    salvar_agendamentos(agendamentos)
    print("\n✅ Paciente cadastrado com sucesso!\n")

# Listagem
def listar(agendamentos):
    if not agendamentos:
        print("\nNenhum paciente cadastrado ainda.\n")
        return
    print("\n <<< PACIENTES CADASTRADOS >>>")
    print("---------------------------------")
    for agendamento in agendamentos:
        telefone_formatado = formatar_telefone(agendamento['DDD'], agendamento['Telefone'])
        print(f"Nome: {agendamento['Nome']} {agendamento['Sobrenome']} | "
              f"CPF: {agendamento.get('CPF', 'N/A')} | "
              f"Nascimento: {agendamento['Data de Nascimento']} | Estado: {agendamento['Estado']} | "
              f"Cidade: {agendamento['Cidade']} | Endereço: {agendamento['Endereço']} | "
              f"Telefone: {telefone_formatado} | "
              f"Especialista: {agendamento['Especialista']} | Horário: {agendamento['Horário']} | "
              f"Status: {agendamento['Status']}")
    print()

# Excluir paciente pelo CPF
def excluir(agendamentos):
    cpf = input("Digite o CPF (11 dígitos) do paciente a excluir: ")
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            agendamentos.remove(agendamento)
            salvar_agendamentos(agendamentos)
            print("✅ Paciente excluído com sucesso!")
            return
    print("Paciente não encontrado.")

# Editar paciente pelo CPF
def editar(agendamentos):
    cpf = input("Digite o CPF (11 dígitos) do paciente a editar: ")
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            print("Deixe em branco para manter o valor atual.")
            novo_nome = input(f"Nome ({agendamento['Nome']}): ").title() or agendamento['Nome']
            novo_sobrenome = input(f"Sobrenome ({agendamento['Sobrenome']}): ").title() or agendamento['Sobrenome']
            novo_endereco = input(f"Endereço ({agendamento['Endereço']}): ").title() or agendamento['Endereço']
            novo_horario = input(f"Horário ({agendamento['Horário']}): ") or agendamento['Horário']

            agendamento['Nome'] = novo_nome
            agendamento['Sobrenome'] = novo_sobrenome
            agendamento['Endereço'] = novo_endereco
            agendamento['Horário'] = novo_horario

            salvar_agendamentos(agendamentos)
            print("✅ Paciente atualizado com sucesso!")
            return
    print("Paciente não encontrado.")

# Alterar status pelo CPF
def alterar_status(agendamentos):
    cpf = input("Digite o CPF (11 dígitos) do paciente: ")
    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            print("1 - Cancelado")
            print("2 - Atendimento Realizado")
            print("3 - Ativo")
            opcao = input("Escolha o novo status: ")
            if opcao == "1":
                agendamento["Status"] = "Cancelado"
            elif opcao == "2":
                agendamento["Status"] = "Atendimento Realizado"
            elif opcao == "3":
                agendamento["Status"] = "Ativo"
            else:
                print("Opção inválida.")
                return
            salvar_agendamentos(agendamentos)
            print("✅ Status atualizado com sucesso!")
            return
    print("Paciente não encontrado.")

# Programa principal
def main():
    agendamentos = carregar_agendamentos()

    while True:
        print("=== MENU ===")
        print("1 - Cadastrar paciente")
        print("2 - Listar pacientes")
        print("3 - Excluir paciente")
        print("4 - Editar paciente")
        print("5 - Alterar status")
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
            print("Opção inválida.\n")

if __name__ == "__main__":
    main()