import json
from pathlib import Path
from datetime import datetime

# NOVO: O arquivo agora guarda um dicionário com pacientes E agendamentos
ARQUIVO_DADOS = Path("clinica_dados.json")

# --- Funções utilitárias ---

# ALTERADO: Carrega o novo formato de dados (dicionário)
def carregar_dados():
    """Carrega pacientes e agendamentos do arquivo JSON."""
    dados_padrao = {"pacientes": [], "agendamentos": []}
    if not ARQUIVO_DADOS.exists():
        return dados_padrao # Retorna estrutura padrão se o arquivo não existe

    if ARQUIVO_DADOS.stat().st_size == 0:
        return dados_padrao # Retorna estrutura padrão se o arquivo está vazio

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            
            # NOVO: Tentativa de migrar dados do formato antigo (lista)
            if isinstance(dados, list):
                print("!! Aviso: Detectado formato de arquivo antigo (lista).")
                print("!! Movendo dados antigos para a lista de 'pacientes'.")
                print("!! Por favor, recadastre os agendamentos.")
                # Migra os dados antigos, assumindo que eram pacientes
                migrados = {"pacientes": dados, "agendamentos": []}
                # Garante que o campo 'NomeCompleto' exista
                for p in migrados["pacientes"]:
                    if "Nome" in p and "NomeCompleto" not in p:
                        p["NomeCompleto"] = f"{p.get('Nome', '')} {p.get('Sobrenome', '')}".strip()
                return migrados

            # Carrega o formato de dicionário esperado
            return {
                "pacientes": dados.get("pacientes", []),
                "agendamentos": dados.get("agendamentos", [])
            }
    except json.JSONDecodeError:
        print(f"\n!! Erro: O arquivo {ARQUIVO_DADOS} está corrompido. Iniciando com dados limpos.\n")
        return dados_padrao

# ALTERADO: Salva o novo formato de dados (dicionário)
def salvar_dados(pacientes, agendamentos):
    """Salva as listas de pacientes e agendamentos no arquivo JSON."""
    dados_completos = {
        "pacientes": pacientes,
        "agendamentos": agendamentos
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados_completos, f, indent=4, ensure_ascii=False)

# Funções de validação (sem alteração)
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

# NOVO: Função helper para buscar um paciente pelo CPF na lista de pacientes
def buscar_paciente_por_cpf(cpf, pacientes):
    """Retorna o dicionário do paciente se encontrado, senão None."""
    for paciente in pacientes:
        if paciente["CPF"] == cpf:
            return paciente
    return None

# NOVO: Função helper para imprimir dados de um PACIENTE (registro)
def imprimir_paciente_registro(paciente, indice=None):
    """Imprime um bloco formatado com os dados de registro de um paciente."""
    if indice:
        print(f"PACIENTE #{indice}")
    
    largura_label = 19
    print(f"  {'Nome Completo:':<{largura_label}} {paciente.get('NomeCompleto', 'N/A')}")
    print(f"  {'CPF:':<{largura_label}} {paciente.get('CPF', 'N/A')}")
    print(f"  {'Nascimento:':<{largura_label}} {paciente.get('Data de Nascimento', 'N/A')}")
    print(f"  {'Contato:':<{largura_label}} {formatar_telefone(paciente.get('DDD', ''), paciente.get('Telefone', ''))}")
    print(f"  {'Endereço:':<{largura_label}} {paciente.get('Endereço', 'N/A')}")
    print(f"  {'Local:':<{largura_label}} {paciente.get('Cidade', 'N/A')} - {paciente.get('Estado', 'N/A')}")
    print(f"  {'Data de Cadastro:':<{largura_label}} {paciente.get('DataCadastro', 'N/A')}")
    print(f"  {'Última Modificação:':<{largura_label}} {paciente.get('UltimaModificacao', 'N/A')}")

# NOVO: Função helper para imprimir dados de um AGENDAMENTO
def imprimir_agendamento_detalhado(ag, indice=None):
    """Imprime um bloco formatado com os dados de um agendamento."""
    if indice:
        print(f"AGENDAMENTO #{indice}")
    
    largura_label = 15
    print(f"  {'Data:':<{largura_label}} {ag.get('DataConsulta', 'N/A')}")
    print(f"  {'Horário Início:':<{largura_label}} {ag.get('HorarioInicio', 'N/A')}")
    print(f"  {'Status:':<{largura_label}} {ag.get('Status', 'N/A')}")
    print(f"  {'Paciente:':<{largura_label}} {ag.get('NomeCompleto', 'N/A')}")
    print(f"  {'CPF:':<{largura_label}} {ag.get('CPF', 'N/A')}")
    print(f"  {'Médico:':<{largura_label}} {ag.get('Especialista', 'N/A')}")
    print(f"  {'Horário Final:':<{largura_label}} {ag.get('HoraFinal', 'N/A')}")

# (Função formatar_telefone não precisa de mudanças)
def formatar_telefone(ddd, telefone):
    # Converte para string e zfill para o caso de dados antigos
    ddd = str(ddd)
    telefone = str(telefone).zfill(9) 
    
    if not ddd and not telefone:
        return "N/A"
        
    parte1 = telefone[1:5]
    parte2 = telefone[5:]
    return f"({ddd}) 9 {parte1}-{parte2}"


# --- 1. Cadastrar Paciente (ALTERADO) ---
def cadastrar_paciente(pacientes):
    print("\n--- 1. Novo Cadastro de Paciente ---")
    print("Insira os dados de registro do paciente. (Isso não cria um agendamento).")

    # ALTERADO: Pede Nome Completo
    while True:
        nome_completo = input("Nome Completo: ").title().strip()
        if nome_completo: break
        print("Erro: o nome completo não pode ficar em branco!")

    # Loop de validação de CPF (checa duplicidade na lista de PACIENTES)
    while True:
        cpf = input("CPF (somente números, 11 dígitos): ").strip()
        if not cpf.isdigit() or len(cpf) != 11:
            print("Erro: CPF deve conter exatamente 11 números!")
            continue
        
        if buscar_paciente_por_cpf(cpf, pacientes):
            print("Erro: Já existe um paciente cadastrado com este CPF.")
            # Pergunta se quer parar o cadastro
            if input("Deseja cancelar o cadastro? (S/N): ").strip().upper() == 'S':
                return False # Retorna ao menu principal
            else:
                continue # Pede o CPF novamente
        
        break # CPF válido e único

    # Loops de validação (semelhantes a antes)
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

    data_cadastro_str = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    # Cria o dicionário do PACIENTE (sem dados de consulta)
    paciente_novo = {
        "NomeCompleto": nome_completo, # ALTERADO
        "CPF": cpf,
        "Data de Nascimento": data_nasc_valida,
        "Estado": estado,
        "Cidade": cidade,
        "Endereço": endereco,
        "DDD": ddd,
        "Telefone": telefone,
        "DataCadastro": data_cadastro_str, 
        "UltimaModificacao": "N/A"
    }
    pacientes.append(paciente_novo)
    # Nota: A função 'main' que chamou esta, será responsável por salvar.
    print("\n✅ Paciente cadastrado com sucesso!\n")
    return True # Sinaliza sucesso

# --- 2. Realizar Agendamento (NOVO) ---
def realizar_agendamento(pacientes, agendamentos):
    print("\n--- 2. Realizar Novo Agendamento ---")
    
    nome_paciente = None
    cpf_paciente = None
    paciente_cadastrado = False

    while True:
        resposta = input("O agendamento é para um paciente já cadastrado? (S/N): ").strip().upper()
        if resposta in ('S', 'N'):
            break
        print("Opção inválida.")

    if resposta == 'S':
        # Loop para encontrar o paciente cadastrado
        while True:
            cpf_busca = input("Digite o CPF do paciente (11 dígitos): ").strip()
            paciente_encontrado = buscar_paciente_por_cpf(cpf_busca, pacientes)
            
            if paciente_encontrado:
                print(f"Paciente encontrado: {paciente_encontrado['NomeCompleto']}")
                nome_paciente = paciente_encontrado['NomeCompleto']
                cpf_paciente = paciente_encontrado['CPF']
                paciente_cadastrado = True
                break # Sai do loop de busca
            else:
                print("Paciente não cadastrado com este CPF.")
                if input("Tentar outro CPF? (S/N): ").strip().upper() == 'N':
                    print("Cancelando. Por favor, cadastre o paciente primeiro (Opção 1) ou faça um agendamento não cadastrado.")
                    return False # Cancela o agendamento
    
    elif resposta == 'N':
        print("Agendamento para paciente não cadastrado.")
        # Pede os dados mínimos para o agendamento
        while True:
            nome_paciente = input("Nome Completo do paciente: ").title().strip()
            if nome_paciente: break
            print("Erro: o nome completo não pode ficar em branco!")
        while True:
            cpf_paciente = input("CPF do paciente (11 dígitos, para controle): ").strip()
            if cpf_paciente.isdigit() and len(cpf_paciente) == 11: break
            print("Erro: CPF inválido!")

    # Se não definimos um paciente (cancelou a busca 'S' ou é 'N' e falhou)
    if not nome_paciente or not cpf_paciente:
        print("Dados do paciente incompletos. Agendamento cancelado.")
        return False

    # Coleta de dados do AGENDAMENTO
    print(f"\nAgendando para: {nome_paciente} (CPF: {cpf_paciente})")
    
    # NOVO: Pede a data da consulta
    while True:
        data_consulta_str = input("Data da Consulta (DD/MM/AAAA): ").strip()
        data_consulta_valida = validar_data(data_consulta_str)
        if data_consulta_valida:
            # Validação bônus: não agendar no passado
            if datetime.strptime(data_consulta_valida, '%d/%m/%Y').date() < datetime.now().date():
                print("Erro: Não é possível agendar em uma data passada.")
            else:
                break # Data válida e no futuro
        print("Erro: data inválida! Use o formato DD/MM/AAAA.")
        
    while True:
        especialista = input("Qual médico: ").title().strip()
        if especialista: break
        print("Erro: especialista não pode ficar em branco!")
    while True:
        horario_str = input("Horário de Início (HH:MM): ").strip()
        horario_valido = validar_horario(horario_str)
        if horario_valido: break
        print("Erro: horário inválido! Use o formato HH:MM (ex: 14:30).")

    data_agendamento_str = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

    # Cria o dicionário do AGENDAMENTO
    novo_agendamento = {
        "NomeCompleto": nome_paciente,
        "CPF": cpf_paciente,
        "PacienteCadastrado": paciente_cadastrado, # Guarda se o CPF é de um registro
        "DataConsulta": data_consulta_valida,
        "Especialista": especialista,
        "HorarioInicio": horario_valido, # Nome do campo mudado de 'Horário'
        "HoraFinal": "N/A",
        "DataAgendamento": data_agendamento_str, # Quando foi marcado
        "Status": "Ativo"
    }
    agendamentos.append(novo_agendamento)
    print("\n✅ Agendamento realizado com sucesso!\n")
    return True # Sinaliza sucesso

# --- 3. Listar Pacientes (ALTERADO) ---
def listar_pacientes(pacientes):
    print("\n--- 3. Pacientes Cadastrados ---")
    if not pacientes:
        print("\nNenhum paciente cadastrado ainda.\n")
        return

    separador = "-" * 40 
    print(separador)

    for i, paciente in enumerate(pacientes, start=1):
        # Chama a função helper de impressão de PACIENTE
        imprimir_paciente_registro(paciente, indice=i)
        print(separador)
    print()

# --- 4. Listar Agendamentos (NOVO) ---
def get_sort_key_agendamento(ag):
    """Helper para ordenar agendamentos por data e hora."""
    data_consulta = ag.get("DataConsulta", "")
    hora_inicio = ag.get("HorarioInicio", "00:00")
    
    data_obj = datetime.min # Padrão para dados inválidos (coloca no topo)
    try:
        data_obj = datetime.strptime(f"{data_consulta} {hora_inicio}", '%d/%m/%Y %H:%M')
    except (ValueError, TypeError):
        pass # Usa datetime.min se houver erro
        
    return data_obj

def listar_agendamentos(agendamentos):
    print("\n--- 4. Agendamentos ---")
    if not agendamentos:
        print("\nNenhum agendamento encontrado.\n")
        return

    # Filtra apenas agendamentos 'Ativos'
    agendamentos_ativos = [ag for ag in agendamentos if ag.get("Status") == "Ativo"]
    
    if not agendamentos_ativos:
        print("\nNenhum agendamento 'Ativo' encontrado.\n")
        return

    # NOVO: Ordena pela chave (data + hora)
    agendamentos_ordenados = sorted(agendamentos_ativos, key=get_sort_key_agendamento)
    
    print("(Mostrando agendamentos 'Ativos' ordenados por data e hora)")
    separador = "-" * 40 
    print(separador)
    
    for i, ag in enumerate(agendamentos_ordenados, start=1):
        # Chama a função helper de impressão de AGENDAMENTO
        imprimir_agendamento_detalhado(ag, indice=i)
        print(separador)
    print()

# --- 5. Editar Paciente (ALTERADO E CORRIGIDO) ---
def editar_paciente(pacientes, agendamentos): # <--- ALTERADO: Recebe agendamentos
    print("\n--- 5. Editar Paciente ---")
    cpf = input("Digite o CPF (11 dígitos) do paciente a editar: ").strip()
    
    paciente_encontrado = buscar_paciente_por_cpf(cpf, pacientes)
            
    if not paciente_encontrado:
        print("Paciente não cadastrado.")
        return False

    print(f"Editando paciente: {paciente_encontrado['NomeCompleto']}")
    print("Deixe o campo em branco (pressione Enter) para manter o valor atual.")
    
    # NOVO: Flags para saber se o nome mudou
    nome_alterado = False 
    nome_antigo = paciente_encontrado['NomeCompleto']

    # 1. Loop para Nome Completo
    while True:
        novo_nome = input(f"Nome Completo ({paciente_encontrado['NomeCompleto']}): ").title().strip()
        if not novo_nome: 
            break # Mantém o antigo
        
        paciente_encontrado['NomeCompleto'] = novo_nome
        if novo_nome != nome_antigo: # Marca que o nome foi alterado
            nome_alterado = True
        break

    # 2. NOVO: Loop para Data de Nascimento
    while True:
        nova_data_str = input(f"Data de nascimento ({paciente_encontrado['Data de Nascimento']}): ").strip()
        if not nova_data_str:
            break # Mantém o antigo
        data_nasc_valida = validar_data(nova_data_str)
        if data_nasc_valida:
            paciente_encontrado['Data de Nascimento'] = data_nasc_valida
            break
        print("Erro: data inválida! Use o formato DD/MM/AAAA.")

    # 3. NOVO: Loop para Estado
    while True:
        novo_estado = input(f"Estado ({paciente_encontrado['Estado']}): ").upper().strip()
        if not novo_estado:
            break # Mantém o antigo
        if len(novo_estado) == 2 and novo_estado.isalpha():
            paciente_encontrado['Estado'] = novo_estado
            break
        print("Erro: estado inválido! Digite apenas a sigla de 2 letras.")

    # 4. NOVO: Loop para Cidade
    while True:
        nova_cidade = input(f"Cidade ({paciente_encontrado['Cidade']}): ").title().strip()
        if not nova_cidade:
            break # Mantém o antigo
        if nova_cidade: # (Validação simples de não estar vazio)
            paciente_encontrado['Cidade'] = nova_cidade
            break
        print("Erro: cidade não pode ficar em branco!")

    # 5. Loop para Endereço (já existia)
    while True:
        novo_endereco = input(f"Endereço ({paciente_encontrado['Endereço']}): ").title().strip()
        if not novo_endereco: 
            break # Mantém o antigo
        paciente_encontrado['Endereço'] = novo_endereco
        break

    # 6. NOVO: Loop para DDD
    while True:
        novo_ddd = input(f"DDD ({paciente_encontrado['DDD']}): ").strip()
        if not novo_ddd:
            break # Mantém o antigo
        if novo_ddd.isdigit() and len(novo_ddd) == 2:
            paciente_encontrado['DDD'] = novo_ddd
            break
        print("Erro: DDD inválido! Digite 2 números.")

    # 7. NOVO: Loop para Telefone
    while True:
        novo_numero = input(f"Número de celular ({paciente_encontrado['Telefone']}): ").strip()
        if not novo_numero:
            break # Mantém o antigo
        if novo_numero.isdigit() and len(novo_numero) == 9 and novo_numero.startswith("9"):
            paciente_encontrado['Telefone'] = novo_numero
            break
        print("Erro: número inválido! Deve ter 9 dígitos e começar com 9.")

    # NOVO: Sincroniza agendamentos ativos se o nome mudou
    if nome_alterado:
        print("\nDetectada alteração de nome. Sincronizando agendamentos 'Ativos'...")
        agendamentos_atualizados = 0
        for ag in agendamentos:
            # Atualiza apenas agendamentos do mesmo CPF E que estejam "Ativo"
            if ag.get("CPF") == cpf and ag.get("Status") == "Ativo":
                ag["NomeCompleto"] = paciente_encontrado['NomeCompleto']
                agendamentos_atualizados += 1
        
        if agendamentos_atualizados > 0:
            print(f"{agendamentos_atualizados} agendamento(s) 'Ativo(s)' foram atualizados com o novo nome.")
        else:
            print("Nenhum agendamento 'Ativo' precisou ser atualizado.")


    # Atualiza o timestamp de modificação
    paciente_encontrado["UltimaModificacao"] = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    print("\n✅ Paciente atualizado com sucesso!")
    return True # Sinaliza sucesso

# --- 6. Alterar Status do Agendamento (ALTERADO) ---
def alterar_status_agendamento(agendamentos):
    print("\n--- 6. Alterar Status do Agendamento ---")
    cpf = input("Digite o CPF do paciente para buscar agendamentos: ").strip()
    
    # Encontra TODOS os agendamentos para este CPF
    agendamentos_do_paciente = [
        ag for ag in agendamentos if ag.get("CPF") == cpf
    ]
    
    if not agendamentos_do_paciente:
        print("Nenhum agendamento encontrado para este CPF.")
        return False

    # Se houver mais de um, o usuário deve escolher
    if len(agendamentos_do_paciente) == 1:
        agendamento_alvo = agendamentos_do_paciente[0]
        print(f"Agendamento encontrado para {agendamento_alvo['NomeCompleto']} em {agendamento_alvo['DataConsulta']}.")
    else:
        print("Múltiplos agendamentos encontrados para este CPF:")
        for i, ag in enumerate(agendamentos_do_paciente):
            print(f"  {i+1}) Data: {ag['DataConsulta']} | Hora: {ag['HorarioInicio']} | Status: {ag['Status']} | Médico: {ag['Especialista']}")
        
        while True:
            try:
                escolha = int(input("Qual agendamento você quer alterar (digite o número)? "))
                if 1 <= escolha <= len(agendamentos_do_paciente):
                    agendamento_alvo = agendamentos_do_paciente[escolha - 1]
                    break
                else:
                    print("Escolha inválida.")
            except ValueError:
                print("Por favor, digite um número.")

    # Agora temos o 'agendamento_alvo'
    print(f"\nAlterando agendamento de {agendamento_alvo['DataConsulta']} às {agendamento_alvo['HorarioInicio']}")
    print(f"Status Atual: {agendamento_alvo['Status']}")
    print("-------------------------")
    print("1 - Cancelado")
    print("2 - Atendimento Realizado")
    print("3 - Ativo")
    opcao = input("Escolha o novo status (ou deixe em branco para cancelar): ")
    
    novo_status = None
    if opcao == "1":
        novo_status = "Cancelado"
        agendamento_alvo["HoraFinal"] = "N/A"
    elif opcao == "2":
        novo_status = "Atendimento Realizado"
        # Pede a hora final
        while True:
            hora_final_str = input("Digite a HORA FINAL da consulta (HH:MM): ").strip()
            if not hora_final_str:
                print("Erro: A hora final é obrigatória.")
                continue
            hora_final_valida = validar_horario(hora_final_str)
            if hora_final_valida:
                if hora_final_valida <= agendamento_alvo['HorarioInicio']:
                    print(f"Erro: A hora final ({hora_final_valida}) deve ser DEPOIS da hora inicial ({agendamento_alvo['HorarioInicio']}).")
                else:
                    agendamento_alvo["HoraFinal"] = hora_final_valida
                    break
            else:
                print("Erro: horário inválido (formato HH:MM).")
                
    elif opcao == "3":
        novo_status = "Ativo"
        agendamento_alvo["HoraFinal"] = "N/A"
    elif not opcao:
        print("Alteração de status cancelada.")
        return False
    else:
        print("Opção inválida.")
        return False

    agendamento_alvo["Status"] = novo_status
    # (Não atualizamos 'UltimaModificacao' do paciente, pois isso é um agendamento)
    print("✅ Status do agendamento atualizado com sucesso!")
    return True # Sinaliza sucesso

# --- 7. Buscar Consulta Realizada (ALTERADO) ---
def buscar_consultas_realizadas(agendamentos):
    print("\n--- 7. Buscar Consultas Realizadas por CPF ---")
    cpf = input("Digite o CPF (11 dígitos) do paciente: ").strip()
    
    if not cpf.isdigit() or len(cpf) != 11:
        print("Erro: Formato de CPF inválido.")
        return

    # Filtra agendamentos realizados para o CPF
    consultas_realizadas = [
        ag for ag in agendamentos 
        if ag.get("CPF") == cpf and ag.get("Status") == "Atendimento Realizado"
    ]
    
    if not consultas_realizadas:
        print("Nenhum 'Atendimento Realizado' encontrado para este CPF.")
        return

    print(f"Exibindo {len(consultas_realizadas)} consulta(s) realizada(s) para o CPF {cpf}:")
    separador = "-" * 40
    print(separador)
    
    for ag in consultas_realizadas:
        imprimir_agendamento_detalhado(ag)
        print(separador)

# --- 8. Excluir Paciente (ALTERADO) ---
def excluir_paciente(pacientes, agendamentos):
    print("\n--- 8. Excluir Paciente (Registro) ---")
    cpf = input("Digite o CPF (11 dígitos) do paciente a excluir: ").strip()
    
    paciente_encontrado = buscar_paciente_por_cpf(cpf, pacientes)
            
    if not paciente_encontrado:
        print("Paciente não cadastrado.")
        return False

    print(f"!! ATENÇÃO !!")
    print(f"Você está prestes a excluir o registro do paciente: {paciente_encontrado['NomeCompleto']}")
    print("Isso NÃO excluirá os agendamentos dele (eles permanecerão no histórico).")
    
    if input("Confirmar exclusão? (S/N): ").strip().upper() != 'S':
        print("Exclusão cancelada.")
        return False

    pacientes.remove(paciente_encontrado)
    print("✅ Paciente (registro) excluído com sucesso!")
    return True # Sinaliza sucesso

# --- Programa principal (ALTERADO) ---
def main():
    # Carrega ambas as listas no início
    dados = carregar_dados()
    pacientes = dados["pacientes"]
    agendamentos = dados["agendamentos"]
    
    dados_modificados = False # Flag para saber se precisa salvar

    while True:
        print("\n===== MENU CLÍNICA =====")
        print("1 - Cadastrar Paciente")
        print("2 - Realizar Agendamento")
        print("3 - Listar Pacientes (Registros)")
        print("4 - Listar Agendamentos (Ativos)")
        print("5 - Editar Paciente (Registro)")
        print("6 - Alterar Status do Agendamento")
        print("7 - Buscar Consultas Realizadas (Histórico)")
        print("8 - Excluir Paciente (Registro)")
        print("9 - Sair")
        opcao = input("Escolha uma opção: ")

        # Reseta o flag no início de cada loop
        dados_modificados = False

        if opcao == "1":
            # Passa a lista de pacientes; se retornar True, marca para salvar
            dados_modificados = cadastrar_paciente(pacientes)
        elif opcao == "2":
            # Passa ambas as listas; se retornar True, marca para salvar
            dados_modificados = realizar_agendamento(pacientes, agendamentos)
        elif opcao == "3":
            listar_pacientes(pacientes)
        elif opcao == "4":
            listar_agendamentos(agendamentos)
        elif opcao == "5":
            # ALTERADO: Passa 'agendamentos' para sincronizar nomes
            dados_modificados = editar_paciente(pacientes, agendamentos)
        elif opcao == "6":
            dados_modificados = alterar_status_agendamento(agendamentos)
        elif opcao == "7":
            buscar_consultas_realizadas(agendamentos)
        elif opcao == "8":
            dados_modificados = excluir_paciente(pacientes, agendamentos)
        elif opcao == "9":
            # Antes de sair, faz um último save se necessário
            if dados_modificados:
                salvar_dados(pacientes, agendamentos)
                print("(Dados pendentes salvos.)")
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida, tente novamente.\n")
        
        # NOVO: Salva os dados APENAS se alguma função (que retorna True) modificou os dados
        if dados_modificados:
            salvar_dados(pacientes, agendamentos)
            print("(Dados salvos no disco.)")

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()