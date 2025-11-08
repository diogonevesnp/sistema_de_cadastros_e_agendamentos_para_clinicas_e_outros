import json
from pathlib import Path
from datetime import datetime

ARQUIVO = Path("agendamentos.json")

# Função para carregar cadastros existentes
def carregar_agendamentos():
    if ARQUIVO.exists():
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Função para salvar cadastros
def salvar_agendamentos(agendamentos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, indent=4, ensure_ascii=False)

# Função para validar data
def validar_data(data_str):
    try:
        return datetime.strptime(data_str, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        return None

# Função para validar horário
def validar_horario(hora_str):
    try:
        return datetime.strptime(hora_str, "%H:%M").strftime("%H:%M")
    except ValueError:
        return None

# Função para formatar telefone
def formatar_telefone(ddd, telefone):
    numero = str(telefone).zfill(9)  # garante 9 dígitos
    parte1 = numero[1:5]             # depois do 9
    parte2 = numero[5:]              # últimos 4
    return f"({ddd}) 9 {parte1}-{parte2}"

# Função para cadastrar novo paciente
def cadastrar(agendamentos):
    nome = input("Digite o primeiro nome: ").title()
    if not nome.isalpha():
        print("Erro: digite apenas letras para o nome!")
        return

    sobrenome = input("Sobrenome: ").title()
    if not sobrenome.isalpha():
        print("Erro: digite apenas letras para o sobrenome!")
        return

    data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
    data_nasc_valida = validar_data(data_nasc)
    if not data_nasc_valida:
        print("Erro: data inválida, use o formato DD/MM/AAAA!")
        return

    estado = input("Estado (sigla, ex: PR): ").upper()
    if len(estado) != 2 or not estado.isalpha():
        print("Erro: estado deve ser a sigla de 2 letras (ex: SP, RJ, PR).")
        return

    cidade = input("Cidade: ").title()
    if not cidade.replace(" ", "").isalpha():
        print("Erro: cidade deve conter apenas letras!")
        return

    endereco = input("Endereço (rua, número, bairro): ").title()

    ddd = input("DDD (2 dígitos): ")
    if not ddd.isdigit() or len(ddd) != 2:
        print("Erro: o DDD deve conter exatamente 2 números!")
        return
    ddd = int(ddd)

    numero = input("Número de celular (9 dígitos, ex: 9XXXXXXX): ")
    if not numero.isdigit() or len(numero) != 9 or not numero.startswith("9"):
        print("Erro: o número de celular deve ter 9 dígitos e começar com 9!")
        return
    telefone = int(numero)

    especialista = input("Qual médico: ").title()
    if not especialista.isalpha():
        print("Erro: digite apenas letras para o especialista!")
        return

    horario = input("Horário da consulta (HH:MM): ")
    horario_valido = validar_horario(horario)
    if not horario_valido:
        print("Erro: horário inválido, use o formato HH:MM (24h)!")
        return

    agendado = {
        "Nome": nome,
        "Sobrenome": sobrenome,
        "Data de Nascimento": data_nasc_valida,
        "Estado": estado,
        "Cidade": cidade,
        "Endereço": endereco,
        "DDD": ddd,
        "Telefone": telefone,
        "Especialista": especialista,
        "Horário": horario_valido
    }
    agendamentos.append(agendado)
    salvar_agendamentos(agendamentos)
    print("\n✅ Paciente cadastrado com sucesso!\n")

# Função para listar pacientes
def listar(agendamentos):
    if not agendamentos:
        print("\nNenhum paciente cadastrado ainda.\n")
        return

    print("\n <<< PACIENTES CADASTRADOS >>>")
    print("---------------------------------")
    for agendamento in agendamentos:
        telefone_formatado = formatar_telefone(agendamento['DDD'], agendamento['Telefone'])
        print(f"Nome: {agendamento['Nome']} {agendamento['Sobrenome']} | "
              f"Nascimento: {agendamento['Data de Nascimento']} | Estado: {agendamento['Estado']} | "
              f"Cidade: {agendamento['Cidade']} | Endereço: {agendamento['Endereço']} | "
              f"Telefone: {telefone_formatado} | "
              f"Especialista: {agendamento['Especialista']} | Horário: {agendamento['Horário']}")
    print()

# ==============================
# Programa principal
# ==============================
def main():
    agendamentos = carregar_agendamentos()

    while True:
        print("=== MENU ===")
        print("1 - Cadastrar paciente")
        print("2 - Listar pacientes")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar(agendamentos)
        elif opcao == "2":
            listar(agendamentos)
        elif opcao == "3":
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.\n")

if __name__ == "__main__":
    main()