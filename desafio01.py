# -------- COMENTÁRIOS SOBRE O DESAFIO: 
# Tive bastante dificuldade com as funções, então acabei não utilizando elas tanto quanto gostaria, espero implementar melhor mais para frente.
# Tentei importar a hora e a data, mas antes de ter visto as aulas sobre, então talvez não esteja implementado da maneira mais elegante

# --------------  INICIO DO PROGRAMA --------------------------

from datetime import date, datetime 
data_hoje = date.today()
data_em_texto = data_hoje.strftime('%d/%m/%Y')

mensagem_inicial = f'''
        ====================================================
                  
                  Bem-vindo(a) ao Banco Mochi!
       
                     Hoje é {data_em_texto}

        ====================================================
       
        Digite o seu nome: '''
nome_digitado = input (mensagem_inicial)
def nome(nome_digitado):
    return nome_digitado.title()

print (f'''
        ====================================================

        Olá Sr(a) {nome(nome_digitado)}, este é o nosso sistema virtual!
        Aqui  você  pode  depositar  ou  sacar  valores
        e ver seu histórico de depósitos e saques  pelo
        extrato  bancário.''')

prosseguir = True

while prosseguir is True:
    verificar_conta = '''
        ====================================================
        Digite a letra correspondente ao tipo de conta:

        [N] Normal
        [B] Black
        [U] Universitaria
        [S] Sair

        ===> '''
    tipo_conta = input(verificar_conta).upper() # O intuito aqui é determinar valor limite de cada saque e a quantidade de saques permitidas de acordo com o tipo de conta, além de associar a escolha a uma string 
    def tipo_conta_registro(tipo_conta):
        return tipo_conta
    if tipo_conta_registro(tipo_conta) == 'N':
        valor_limite = 500
        limite_saques = 3
        tipo_conta_texto = 'Normal'
        break
    elif tipo_conta_registro (tipo_conta) == 'B':
        valor_limite = 5000
        limite_saques = 10
        tipo_conta_texto = 'Black'
        break
    elif tipo_conta_registro (tipo_conta) == 'U':
        valor_limite = 500
        limite_saques = 1
        tipo_conta_texto = 'Universitária'
        break
    elif tipo_conta_registro (tipo_conta) == 'S':
        print('O banco Mochi agradece sua visita!')
        prosseguir = False
        break
    else:
        print('''
        Tipo de conta inválida. Escolha novamente
              ''')

def saldo (saldo):
    return saldo

saldo = 0
lista_extrato = ""
numero_saques = 0

menu = '''
        ======================= MENU =======================
        Digite o número correspondente a operação desejada:

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Sair

      ===> '''

while prosseguir is True :

    def data_e_hora_atuais (data_hora):
        data_hora = datetime.now()
        data_e_hora_em_texto = data_hora.strftime('%d/%m/%Y às %H:%M')
        return data_e_hora_em_texto

    mostra_saldo = f'''
        Sr(a) {nome(nome_digitado)}, seu saldo atual é R$ {saldo:.2f}
'''
    print (mostra_saldo)
    opcao = int(input(menu))
    
    if opcao == 1:
       
        valor = float(input('''
        - Informe o valor do depósito: '''))

        if valor > 0:
            data_hora = datetime.now()
            saldo += valor
            lista_extrato += f"        - Depósito: R$ {valor:.2f} em {data_e_hora_atuais(data_hora)}\n"
            print (f'''
        O valor de R${valor:.2f} foi depositado com sucesso!
        ====================================================''')
                    
        else:
            print('''
        Sinto muito mas a operação falhou! O valor informado é inválido.
        Somente números positivos são permitidos para depositos.''')

    elif opcao == 2:
        print('''
        ======================= SAQUE =======================
              ''')
        print (f'''
        Seu limite de saque para conta {tipo_conta_texto} é R$ {valor_limite:.2f} por operação.
        Você pode realizar até {limite_saques} saques por dia.
        Saques realizados hoje: {numero_saques}.
            ''')
        if numero_saques >= limite_saques:
            print(f'''
        Sinto muito mas a operação falhou! Número máximo de saques excedido.
                  ''')
            continue
        if saldo <= 0:
            print(f'''
        Sinto muito mas a operação falhou! Você não tem saldo suficiente. Seu saldo atual é R$ {saldo:.2f}.
                  ''')
            continue

        valor = float(input('''
        - Informe o valor do saque: '''))

        limite_excedido = valor > valor_limite
        saldo_excedido = valor > saldo
        saque_excedido = numero_saques >= limite_saques

        if limite_excedido:
            print(f'''
        Sinto muito mas a operação falhou! O valor do saque excede o limite permitido. Você pode sacar até R$ {valor_limite:.2f} por operação.
                  ''')
            
        elif saldo_excedido:
            print(f'''
        Sinto muito mas a operação falhou! Você não tem saldo suficiente."
        Você tentou sacar R$ {valor:.2f}, mas seu saldo atual é R$ {saldo:.2f}.
                  ''')

        elif saque_excedido:
            print(f'''
        Sinto muito mas a operação falhou! Número máximo de saques excedido.
                  ''')

        elif valor > 0:
            data_hora = datetime.now()
            saldo -= valor
            lista_extrato += f"        - Saque: R$ {valor:.2f} em {data_e_hora_atuais(data_hora)}\n"
            numero_saques += 1
            print (f'''
        O valor de R${valor:.2f} foi sacado com sucesso!
        ====================================================''')

        else:
            print('''
        Sinto muito mas a operação falhou! O valor informado é inválido.
        Somente números positivos são permitidos.''')

    elif opcao == 3:
        print('''
        ===================== EXTRATO ======================
              ''')
        if lista_extrato == "":
            print('''
        Não foram realizadas movimentações nesta conta.
              ''')
        else: print (lista_extrato)
        print(f'''
        Saldo: R$ {saldo:.2f}
        ====================================================
              ''')

    elif opcao == 4 :
        print ('''
        ====================================================
               
                 O Banco Mochi agradece sua visita!
               
                           Volte sempre!

        ====================================================
               ''')
        
        prosseguir = False
        break

    else:
        print('''
        Operação inválida, por favor selecione novamente a operação desejada
        ====================================================
               ''')
# -------------------  FIM DO PROGRAMA -------------------------