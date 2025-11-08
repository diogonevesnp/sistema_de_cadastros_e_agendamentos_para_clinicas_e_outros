import json
from pathlib import Path

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

    try:
        ddd = int(input("DDD: "))
    except ValueError:
        print("Erro: digite apenas números inteiros para o DDD!")
        return

    try:
        telefone = int(input("Número: "))
    except ValueError:
        print("Erro: digite apenas números inteiros para o telefone!")
        return

    especialista = input("Qual médico: ").title()
    if not especialista.isalpha():
        print("Erro: digite apenas letras para o especialista!")
        return

    agendado = {
        "Nome": nome,
        "Sobrenome": sobrenome,
        "DDD": ddd,
        "Telefone": telefone,
        "Especialista": especialista
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
        print(f"Nome: {agendamento['Nome']} | Sobrenome: {agendamento['Sobrenome']} | "
              f"DDD: {agendamento['DDD']} | Telefone: {agendamento['Telefone']} | "
              f"Especialista: {agendamento['Especialista']}")
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