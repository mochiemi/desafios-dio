# -------- COMENTÁRIOS SOBRE O PROJETO ------------------------
# DESAFIO 02: OTIMIZANDO O SISTEMA BANCÁRIO
# Utilizei meu próprio código do desafio anterior, aplicando as otimizações e altereções sugeridas pelo desafio.
# Mantive a implementação do datatime

# --------------  INICIO DO PROGRAMA --------------------------

# ------ Função de data e hora ------

from datetime import date, datetime 

def data_e_hora_atuais (data_hora):
    data_hora = datetime.now()
    data_e_hora_em_texto = data_hora.strftime('%d/%m/%Y às %H:%M')
    return data_e_hora_em_texto

# ----- Função Depositar ------- 

def depositar (saldo, valor, lista_extrato, /):
    if valor > 0:
        data_hora = datetime.now()
        saldo += valor
        lista_extrato.append({'tipo_operacao' : 'deposito' , 'descricao': f"\t- Depósito: R$ {valor:.2f} em {data_e_hora_atuais(data_hora)}\n"})
        print(f'''
        O valor de R${valor:.2f} foi depositado com sucesso!
        ====================================================''')
    else:
        print(f'''
        Sinto muito, não é possivel depositar valores inválidos.
        ====================================================''')
    return saldo, lista_extrato

# ----- Função Sacar -------

def sacar (*, saldo, valor, lista_extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    print(f'''
        ======================= SAQUE =======================
        Seu limite de saque para é R$ 500,00 por operação.
        Você pode realizar até {limite_saques} saques por dia.
        Saques realizados hoje: {numero_saques}. 
              ''')
    if excedeu_saldo:
        print(f'''
        Sinto muito mas a operação falhou! Você não tem saldo suficiente. Seu saldo atual é R$ {saldo:.2f}.
                  ''')

    elif excedeu_limite:
        print(f'''
        Sinto muito mas a operação falhou! O valor do saque excede o limite permitido. Você pode sacar até R$ {limite:.2f} por operação.
                  ''')

    elif excedeu_saques:
        print(f'''
        Sinto muito mas a operação falhou! Número máximo de saques excedido.
                  ''')

    elif valor > 0:
        data_hora = datetime.now()
        saldo -= valor
        lista_extrato.append({'tipo_operacao' : 'saque' , 'descricao': f"\t- Saque: R$ {valor:.2f} em {data_e_hora_atuais(data_hora)}\n"})
        numero_saques += 1
        print (f'''
        O valor de R${valor:.2f} foi sacado com sucesso!
        ====================================================''')

    else:
        print(f'''
        Sinto muito, não é possivel sacar valores inválidos.
        ====================================================''')
        return
    return saldo, lista_extrato, numero_saques

# ------- Função Extrato e filtro  de extrato por tipo de operação -------

def exibir_extrato (saldo, /, *, lista_extrato):
    print('''
        ===================== EXTRATO ======================
              ''')

    operacao_input = input('\n\tQual operacao deseja visualizar? \n\t[1] Todas \n\t[2] Depositos \n\t[3] Saques \n\tDigite o número correspondente ==>')
    if operacao_input == '1':
        print('''
        =================== EXTRATO (SAQUES E DEPÓSITOS) ====================
              ''')
        if listar_contas is not []:
            for item_extrato in lista_extrato:
                print (item_extrato['descricao'])
        else:
                print('''
        Não foram realizadas movimentações nesta conta.
              ''')
    elif operacao_input == '2':
        print('''
        =================== EXTRATO (SOMENTE DEPÓSITOS) ====================
              ''')
        operacao_escolhida = filtrar_extrato('deposito', lista_extrato)
        if operacao_escolhida:
            for item_extrato in operacao_escolhida:
                print (item_extrato['descricao'])
        else:
            print('''
        Não foram realizadas movimentações nesta conta.
              ''')
    elif operacao_input == '3':
        print('''
        =================== EXTRATO (SOMENTE SAQUES) ====================
              ''')
        operacao_escolhida = filtrar_extrato('saque', lista_extrato)
        if operacao_escolhida:
            for item_extrato in operacao_escolhida:
                print (item_extrato['descricao'])
        else:
            print('''
        Não foram realizadas movimentações nesta conta.
              ''')
    else:
        print('''
        Opção inválida! Tente novamente.
              ''')
    print(f'''
        Saldo: R$ {saldo:.2f}
        ====================================================
              ''')

def filtrar_extrato (operacao_input, lista_extrato):
    operacao_escolhida = [operacao for operacao in lista_extrato if operacao['tipo_operacao'] == operacao_input]
    return operacao_escolhida if operacao_escolhida else None

# ------- Função Cadastrar Usuário e filtrar por CPF-------

def filtrar_usuario_por_cpf (cpf_input, lista_usuarios):
    usuarios_filtrados = [usuario for usuario in lista_usuarios if usuario["cpf"] == cpf_input]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def cadastrar_usuario (lista_usuarios):
    print('''
        ===================== NOVO CADASTRO DE USUÁRIO ======================
        Para iniciar o cadastro precisamos de algumas informações.
        Lembramos que cada usuário está associado a um único CPF.
              ''')
    cpf_input = input("\tInforme o CPF (somente números): ")
    usuario_existente = filtrar_usuario_por_cpf(cpf_input, lista_usuarios)
    if usuario_existente:
        print(f'''
        Este CPF já está cadastrado no sistema. Só pode haver um usuário por CPF.
        ====================================================
              ''')
        return
    nome_usuario = input("\tInforme o nome completo: ")
    data_nascimento = input("\tInforme a data de nascimento (dd-mm-aaaa): ")

    endereco = input("\tInforme o endereço (logradouro, número - bairro - cidade/sigla estado): ")
    lista_usuarios.append({"nome_usuario": nome_usuario, "data_nascimento": data_nascimento, "cpf": cpf_input, "endereco": endereco})
    primeiro_nome = nome_usuario.split(" ")[0]
    print(f'''
        CPF {cpf_input} cadastrado com sucesso!
        Este CPF estará vínculado ao usuário {primeiro_nome.title()} 
              ''')
    return lista_usuarios

# -------  Cadastro de contas e lista de contas por usuário ------
def cadastro_conta(agencia, numero_conta, lista_usuarios, todas_contas):
    print('''
        ===================== NOVO CADASTRO DE CONTAS ======================
        Aqui você pode registrar uma nova conta corrente para seu usuário.
        Lembramos que cada usuário está associado a um único CPF.
              ''')
    cpf_input = input("\tInforme o CPF (somente números): ")
    usuario_existente = filtrar_usuario_por_cpf(cpf_input, lista_usuarios)
    if usuario_existente:
        numero_conta = len(todas_contas) + 1
        conta = {'agencia': agencia, 'numero_conta': numero_conta, 'usuario_conta': usuario_existente['cpf'], 'nome_usuario': usuario_existente['nome_usuario']}
        todas_contas.append (conta)
        print ('\n\t ------- Conta registrada com sucesso! ------')
    else:
        print ('\n\tNão foi possível criar conta. CPF não encontrado.\n\tTente novamente.')
        return main()
    return todas_contas
def listar_contas(todas_contas):
        cpf_input = input ('\n\tPara listar suas contas. Confirme novamente o CPF do usuário:  ')    
        contas_do_cpf_buscado = filtro_conta_por_cpf(cpf_input, todas_contas, contas=[])
        for conta in contas_do_cpf_buscado:
            texto_conta= f'''
            Agência: {conta['agencia']}
            Nº C/C: {conta['numero_conta']}
            Titular: {conta['nome_usuario'].title()}
            ------------------------------------'''
            print (texto_conta)
        return contas_do_cpf_buscado
        
def filtro_conta_por_cpf(cpf_input, todas_contas, contas=[]):
    for conta in todas_contas:
        if conta['usuario_conta'] == cpf_input:
            contas.append(conta)
        else:
            print('\n\tCPF digitado não contém nenhuma conta.')
    return contas

# ------- Inicio da tela ---------
def menu_comeco(lista_usuarios, usuario_ativo):
    comeco = True
    data_hoje = date.today()
    data_em_texto = data_hoje.strftime('%d/%m/%Y')

    while comeco is True:
        cpf_input = input (f'''
        ====================================================
                  
                  Bem-vindo(a) ao Banco Mochi!
       
                     Hoje é {data_em_texto}

        ====================================================
        Para acessar sua conta, digite seu CPF.
            ==> ''')
        usuario_existente = filtrar_usuario_por_cpf (cpf_input, lista_usuarios)
        if usuario_existente:    
            usuario_ativo = usuario_existente
            print (f'''
        Esses são seus dados:
        - Nome Completo: {usuario_ativo['nome_usuario'].title()}
        - Data de Nascimento: {usuario_ativo['data_nascimento']}
        - CPF: {usuario_ativo['cpf']}
        - Endereço: {usuario_ativo['endereco']}
            ''')
            return usuario_ativo
        else:
            novo_usuario = input ('''
        Não foi possível encontrar esse CPF no cadastro. Gostaria de fazer um novo cadastro? [s/n]
            ==> ''').lower()
            if novo_usuario == 's':
                cadastrar_usuario(lista_usuarios)
            
            elif novo_usuario == 'n':
                fim_de_operacoes()
                main()
            else:
                print ('\n\tComando inválido. Voltando ao menu inicial')
                
# ------- Menu de Contas ---------

def menu_contas(AGENCIA, todas_contas, lista_usuarios):
    cpf_input = input("\tPara acessar suas contas. Confirme o CPF do usuário \n\t==> ")
    usuario_ativo = filtrar_usuario_por_cpf (cpf_input, lista_usuarios)
    if usuario_ativo:
        selecao_menu_contas = input(f'''
        ======================= CONTAS =======================
        O usuário atual é: {usuario_ativo['nome_usuario'].title()}
        Selecione a ação desejada:
        
        [1] Listar contas
        [2] Cadastrar nova conta
        [3] Sair / Escolher outro usuário
            ==> ''')
        if selecao_menu_contas=='1':
            listar_contas(todas_contas)
            avancar = input('\tAperte qualquer tecla para continuar:  ')
            return avancar
            
        elif selecao_menu_contas=='2':
            numero_conta = len(todas_contas) + 1
            cadastro_conta(AGENCIA, numero_conta, lista_usuarios, todas_contas)
        elif selecao_menu_contas=='3':
            menu_comeco(lista_usuarios, usuario_ativo=None)
        else:
            print ('\n\tComando inválido. Selecione novamente.\n')

# ------- Menu de Operações -------
def menu():
    operacao = input ('''
        ======================= MENU =======================
        Digite o número correspondente a operação desejada:

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Acessar contas
        [5] Selecionar outro usuário
        [6] Sair

            ==> ''')
    return operacao

# -------- Mensagem de despedida/fim do serviço --------

def fim_de_operacoes ():
        print ('''
        ====================================================
                
                O Banco Mochi agradece sua visita!
                
                        Volte sempre!

        ====================================================
            ''')
      
# ------- Main -------

def main(lista_usuarios=[], todas_contas=[], conta_ativa=[], usuario_ativo=None, nome_usuario_ativo=None):
    comeco = True
    continua_menu = False
    continua_contas = False
    valor_limite = 500
    numero_saques = 0
    limite_saques = 3
    saldo = 0
    lista_extrato=[]
    AGENCIA = "0001"

    while comeco:
        usuario_ativo = menu_comeco(lista_usuarios, usuario_ativo)
        if usuario_ativo is None:
            comeco = True
        else:
            continua_menu = True
            comeco =  False
            nome_usuario_ativo = usuario_ativo['nome_usuario']
            primeiro_nome_ativo = nome_usuario_ativo.split(" ")
            print (f'''
        Seja Bem Vindo(a) {primeiro_nome_ativo[0].title()}!''')

    while continua_menu:
        if len(conta_ativa) == 0:
            escolha_criar_conta = input('''
        Verificamos que seu usuário não possui contas
        Gostaria de criar uma nova conta? [s/n]
            ==> ''').lower()
            if escolha_criar_conta == 's':
                continua_contas=True
                while continua_contas:
                    numero_conta = len(todas_contas) + 1
                    conta_ativa = cadastro_conta(AGENCIA, numero_conta, lista_usuarios, todas_contas)
                    continua_contas = False
            elif escolha_criar_conta == 'n':
                fim_de_operacoes()
                main(lista_usuarios)         
            else:
                    print ('\n\tEscolha inválida. Tente novamente\n')
        else:
            continua_contas = False
            print (f'''         
        Bem Vindo(a) de volta,  {usuario_ativo['nome_usuario'].title()}!
            ''')
        operacao = menu()

        if operacao == '1' :
            valor = float(input('''
        ===================== DEPÓSITO =====================
        Você escolheu a opção Depositar
        Por favor, Informe o valor do depósito: '''))
            
            saldo, lista_extrato = depositar(saldo, valor, lista_extrato)
    
        elif  operacao == '2' :
            valor = float(input(f'''
        ======================= SAQUE ======================                       
        Por favor, Informe o valor do saque: '''))
            saldo, lista_extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                lista_extrato=lista_extrato,
                limite=valor_limite,
                numero_saques=numero_saques,
                limite_saques=limite_saques,
            )
        elif operacao == '3' :
            exibir_extrato(saldo, lista_extrato=lista_extrato)
        elif operacao == '4' :
            menu_contas(AGENCIA, todas_contas, lista_usuarios)

        elif operacao == '5':
            cpf_input = input('''
            Digite o CPF que deseja acessar: 
                ==> ''')
            usuario_ativo = filtrar_usuario_por_cpf (cpf_input, lista_usuarios)
            if usuario_ativo:
                continua_menu = True
            else:
                print ('\n\tNão foi possível encontrar o CPF registrado. \n\n\t .... Reiniciando sistema ....')
                main (lista_usuarios, todas_contas)
        elif operacao == '6' :
            fim_de_operacoes()
            break

        else:
            print('''
            Operação inválida, por favor selecione novamente a operação desejada
            ====================================================
                ''')            

main()
# -------------------  FIM DO PROGRAMA -------------------------