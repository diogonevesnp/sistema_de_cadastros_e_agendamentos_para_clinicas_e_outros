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