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

agendados = {}
agendamentos = []
print('<<< AGENDAMENTO DE CONSULTAS >>>')
print('---------------------------------')

while True:   
     
     try:
        nome_digitado = input('Digite o seu primeiro nome: ').title()
     except ValueError:
        print('Erro: Por favor digite apenas letras para o nome!')
        continue

     try:
        sobrenome_digitado = input('Sobrenome: ').title()
     except ValueError:
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
        print('Erro: Por favor digite apenas números e inteiros!')
        continue
     try:
        esp_digitado = input('Qual médico: ').title()
     except ValueError:
        print('Erro: Por favor digite apenas letras para o tipo de especialista!')

     agendados ['Nome'] = nome_digitado
     agendados ['Sobrenome'] = sobrenome_digitado
     agendados ['DDD'] = ddd_digitado
     agendados ['Telefone'] = telefone_digitado
     agendados ['Especialista'] = esp_digitado
     agendamentos.append(agendados.copy())

     try:
        res_usuario = str(input('Quer continuar? S/N')).upper()
     except ValueError:
        print('Erro por favor digite apenas letra!')   
        continue
     
     if res_usuario == 'N':
        break
     
     print()
     
if agendamentos:
   print('\n <<< PACIENTES CADASTRADOS >>>') 
   print('---------------------------------')

for agendamento in agendamentos:
    print(f"Nome: {agendamento['Nome']} | Sobrenome: {agendamento['Sobrenome']} | DDD: {agendamento['DDD']} | Telefone: {agendamento['Telefone']} | Especialista: {agendamento['Especialista']}")