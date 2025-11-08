'''
1º PROJETO PESSOAL

[CAC] < Cadastro e Agendamento para Clínicas >

Este sistema tem como objetivo realizar o cadastro de pacientes em clínicas de diferentes segmentos, podendo também ser adaptado
para outros contextos, como petshops, com pequenos ajustes.

O sistema contará com um menu de opções para manipulação de dados, permitindo:
- Criar novos cadastros e agendamentos
- Listar pacientes cadastrados
- Editar informações
- Alterar o status de atendimentos
- Excluir registros

Os cadastros incluem informações como: nome completo, data de nascimento, endereço, DDD, número de telefone, estado, cidade e CPF.  
Todas as operações de manipulação de dados — cadastro, agendamento, listagem, edição e alteração de status — são filtradas pelo CPF
do paciente, garantindo maior precisão e segurança.

Além disso, o sistema aplica validações para evitar entradas inválidas, como impedir números em campos de texto e padronizar formatos. Exemplos:
- CPF sempre com 11 dígitos
- DDD sempre 2 dígitos
- Número de telefone formatado com o '9' e  “-” para separação

Este projeto representa a versão inicial da ideia, que poderá evoluir com melhorias futuras, como persistência dos dados em JSON, uso de dicionários
independentes para cada paciente e implementação de novas funcionalidades.
'''

import json

agendamentos = []
print('<<< AGENDAMENTO DE CONSULTAS >>>')
print('---------------------------------')

while True:
    # Correção do método de validação correta para entrda de Strings (.isalpha)
    nome_digitado = input('Digite o seu primeiro nome: ').title()
    if not nome_digitado.isalpha():
        print('Erro: Por favor digite apenas letras para o nome!')
        continue

    sobrenome_digitado = input('Sobrenome: ').title()
    if not sobrenome_digitado.isalpha():
        print('Erro: Por favor digite apenas letras para o sobrenome!')
        continue

    try:
        ddd_digitado = int(input('DDD: '))
    except ValueError:
        print('Erro: Por favor, digite apenas números inteiros.')
        continue

    try:
        telefone_digitado = int(input('Número: '))
    except ValueError:
        print('Erro: Por favor digite apenas números inteiros!')
        continue

    esp_digitado = input('Qual médico: ').title()
    if not esp_digitado.isalpha():
        print('Erro: Por favor digite apenas letras para o especialista!')
        continue

    # Criar um novo dicionário para cada paciente
    agendado = {
        "Nome": nome_digitado,
        "Sobrenome": sobrenome_digitado,
        "DDD": ddd_digitado,
        "Telefone": telefone_digitado,
        "Especialista": esp_digitado
    }
    agendamentos.append(agendado)

    res_usuario = input('Quer continuar? S/N: ').upper()
    if res_usuario == 'N':
        break
    print()

# Exibir os cadastrados
if agendamentos:
    print('\n <<< PACIENTES CADASTRADOS >>>')
    print('---------------------------------')
    for agendamento in agendamentos:
        print(f"Nome: {agendamento['Nome']} | Sobrenome: {agendamento['Sobrenome']} | "
              f"DDD: {agendamento['DDD']} | Telefone: {agendamento['Telefone']} | "
              f"Especialista: {agendamento['Especialista']}")

# Salvar em arquivo JSON
with open("agendamentos.json", "w", encoding="utf-8") as f:
    json.dump(agendamentos, f, indent=4, ensure_ascii=False)

print("\nAgendamentos salvos em 'agendamentos.json'")