# ----- DESAFIO MODELO DE SISTEMA BANCÁRIO EM POO - PYTHON ------#

from abc import ABC, abstractmethod
from datetime import datetime, date

# ----- CLASSES DE OBJETOS ------#

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao (self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta (self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
class Conta:
    def __init__(self ,numero, cliente, tipo_conta, limite, limite_saques):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._tipo_conta = tipo_conta
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def tipo_conta(self):
        return self._tipo_conta

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print(f'''
    Sinto muito mas a operação falhou! Você não tem saldo suficiente. Seu saldo atual é R$ {self.saldo:.2f}.
    --------------------------------------------------------------''')                
        elif valor > 0:
            self._saldo -= valor
            print (f'''
    O valor de R${valor:.2f} foi sacado com sucesso!
    Seu saldo agora é de R${self.saldo:.2f}
    --------------------------------------------------------------''')
            return True
        else:
            print(f'''
    Sinto muito mas a operação falhou! Valor informado é inválido.
    --------------------------------------------------------------''')
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'''
    O valor de R${valor:.2f} foi depositado com sucesso!
    Seu saldo agora é de R${self.saldo:.2f}
    --------------------------------------------------------------''')
            return True
        
        else:
            print(f'''
    Sinto muito mas a operação falhou! Valor {valor} informado é inválido.
    --------------------------------------------------------------''')            
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, tipo_conta, limite, limite_saques):
        super().__init__(numero, cliente, tipo_conta, limite, limite_saques)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques
    
    @classmethod
    def nova_conta(cls, numero, cliente, tipo_conta, limite, limite_saques):
        return cls(numero, cliente, tipo_conta, limite, limite_saques)
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo_transacao'].lower() == 'saque'])
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
           
        if excedeu_limite:
            print(f'''
    Sinto muito mas a operação falhou! O valor do saque excede o limite permitido. Você pode sacar até R$ {self._limite:.2f} por operação.
    --------------------------------------------------------------''')
            
        elif excedeu_saques:
            print(f'''
    Sinto muito mas a operação falhou! Número máximo de saques excedido. Limite diário de {self._limite_saques} por dia.
    --------------------------------------------------------------''')
        else:
            return super().sacar(valor), numero_saques
        return False

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def extrato_transacoes(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao['tipo_transacao'].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def adicionar_transacao(self, transacao):
        data_hora = datetime.now().strftime('%d/%m/%Y às %H:%M')
        self._transacoes.append({'tipo_transacao' : transacao.__class__.__name__,
                                 'valor': transacao.valor,
                                 'data': data_hora,
                                })
    
    def transacoes_do_dia(self):
        data_atual = datetime.now()
        transacoes = []
        for transacao in self._trasacoes:
            data_transacao = datetime.strptime(transacao['data'], '%d/%m/%Y às %H:%M').date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass
        
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# ------ FILTROS E UTILITÁRIOS ----- #
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def selecionar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n\tNão foi possível encontrar uma conta registrada para este cliente.")
        return
    else:
        contas = cliente.contas
        listar_contas(cliente, contas)
        x = int(input('\n\tSelecione a conta que deseja movimentar:  '))
        if x <= len(contas):
            x -= 1
            return contas[x]
        else:
            print('\n ### Conta inexistente. Selecione novamente o nº [x] da conta. ###')

# ----- ACÕES DOS MENUS ------#

def depositar(cliente_ativo, conta_ativa):
    cliente = cliente_ativo
    conta = conta_ativa
    if not conta_ativa:
        print ("\tNão há conta ativa no momento.")
        selecionar_conta_cliente(cliente)

    print (f'''
    ========================  DEPÓSITO  ========================
    Conta ativa: {conta_ativa.agencia}/{conta_ativa.numero} - Conta {conta_ativa.tipo_conta.title()}
    Os valores depositados serão computados na sua conta ativa.''')
    valor = float(input('''
    Digite o valor do deposito:  '''))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

def sacar(cliente_ativo, conta_ativa, numero_saques=0):
    cliente = cliente_ativo
    conta = conta_ativa
    numero_saques = len([transacao for transacao in conta.historico.transacoes if transacao['tipo_transacao'].lower() == 'saque'])
    valor = float(input(f'''
    ========================= SAQUE ========================
    Conta ativa: {conta_ativa.agencia}/{conta_ativa.numero} - Conta {conta_ativa.tipo_conta} 
    Limite por saque: R${conta_ativa.limite:.2f} - Saques realizados: {numero_saques}/{conta_ativa.limite_saques}                      
    Por favor, Informe o valor do saque: '''))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)
    return

def exibir_extrato(conta_ativa):
    conta = conta_ativa
    extrato = ""
    tem_transacao = False
    escolha_extrato= input('\tGostaria de visualizar qual tipo de extrato?\n\t[1] Depositos\t[2] Saques\t[3] Todos\n\t\t==> ')
    print("    =======================  EXTRATO  =======================")
    if escolha_extrato == '1':
        tipo_transacao = 'deposito'
        for transacao in conta.historico.extrato_transacoes(tipo_transacao):
            tem_transacao = True
            extrato += f"\t[{transacao['tipo_transacao']}] - {transacao['data']}:\n\t  R$ {transacao['valor']:.2f}\n"
        print(extrato)
    elif escolha_extrato == '2':
        tipo_transacao = 'saque'
        for transacao in conta.historico.extrato_transacoes(tipo_transacao):
            tem_transacao = True
            extrato += f"\t[{transacao['tipo_transacao']}] - {transacao['data']}:\n\t  R$ {transacao['valor']:.2f}\n"
        print(extrato)

    else:
        for transacao in conta.historico.extrato_transacoes():
            tem_transacao = True
            extrato += f"\t[{transacao['tipo_transacao']}] - {transacao['data']}:\n\t  R$ {transacao['valor']:.2f}\n"
        print(extrato)   
    if not tem_transacao:
        extrato = "  Não foram realizadas movimentações desse tipo nesta conta!"
        print(extrato)
    
    print(f"  -----------------------------------------------------\n\tSaldo:\tR$ {conta.saldo:.2f}")
    print("  -----------------------------------------------------")

def listar_contas(cliente_ativo, contas):
    contas = cliente_ativo.contas
    conta_numero = 1
    for conta in contas:
            texto_conta= f'''
    --------------------------------------------------------------
    Conta nº : [{conta_numero}]\tTipo: {conta.tipo_conta.title()}
        Titular: {cliente_ativo.nome.title()}
        Agência-C/C: {conta.agencia}-{conta.numero}     
        Saldo: R${conta.saldo:.2f}'''
            print (texto_conta)
            conta_numero += 1
    return contas

def cadastrar_conta(numero_conta, clientes, contas, cliente_ativo):
    cpf = cliente_ativo.cpf
    cliente = filtrar_cliente(cpf, clientes)
    selecionar_tipo_conta = input('''
    Selecione o tipo de Conta Corrente que deseja:
    --------------------------------------------------------------
    | Tipo de Conta        | Limite por saque | Saques diários |
      [1] Regular               R$500,00              3
      [2] Universitário         R$1000,00             1
      [3] Especial              R$5000,00            10
    --------------------------------------------------------------
        ==> ''')
        
    if selecionar_tipo_conta == '1':
        tipo_conta = 'regular'
        limite = 500
        limite_saques = 3
    elif selecionar_tipo_conta == '2':
        tipo_conta = 'universitario'
        limite = 1000
        limite_saques = 1
    elif selecionar_tipo_conta == '3':
        tipo_conta = 'especial'
        limite = 5000
        limite_saques = 10
    else:
        print ('\n   ####### Tipo de conta inválida Selecione novamente #######')
        return
    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, tipo_conta=tipo_conta, limite=limite ,limite_saques=limite_saques)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n  --------------  Conta cadastrada com sucesso! --------------")
    return contas

def cadastrar_conta_inicio(numero_conta, clientes, contas, cliente_ativo):
    cpf = cliente_ativo.cpf
    cliente_cadastro = filtrar_cliente(cpf, clientes)
    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente_cadastro, numero=numero_conta, tipo_conta='regular', limite=500, limite_saques=3)
    contas.append(conta)
    cliente_cadastro.contas.append(conta)
    print("\n  --------------  Conta cadastrada com sucesso! --------------")

def selecionar_cliente(clientes):
    cpf_input = input('''
    Digite o CPF que deseja acessar: 
        ==> ''')
    cliente_existe = filtrar_cliente (cpf_input, clientes)
    if cliente_existe:
        cliente_ativo = cpf_input
        return cliente_ativo
    else:
        print ('\n ########  Não foi possível encontrar o CPF registrado!  ######## \n')
        menu_inicio()

def cadastrar_cliente(clientes):
    cpf = input("\n   =================  CADASTRO DE CLIENTES  ==================\n\tInforme o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n  ######## Este CPF já foi registrado! Tente novamente ########")
        return

    nome = input("\tInforme o nome completo: ")
    data_nascimento = input("\tInforme a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "\tInforme o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n  ^^^^ Cliente cadastrado com sucesso! Voltando ao menu anterior. ^^^^")
    return cliente

# ----- MENUS/MENSAGENS ------#
def menu_inicio():
    print (f'''
    =========================================================
                  
                Bem-vindo(a) ao Banco Mochi!
       
                    Hoje é {date.today().strftime('%d/%m/%Y')}

    =========================================================''')
    cpf_inicio = input('''
    Para acessar sua conta, digite seu CPF.
        ==> ''')
    return cpf_inicio
    
def menu_contas(cliente_ativo, conta_ativa, clientes, contas, numero_conta):
    while True:
        selecao_menu_contas = input(f'''
    ========================   CONTAS   ========================

        A C/C ativa é: {conta_ativa.agencia}/{conta_ativa.numero} - {conta_ativa.tipo_conta.title()}
        Selecione a ação desejada:
            
        [1] Listar contas
        [2] Cadastrar nova conta
        [3] Trocar conta ativa
        [4] Voltar ao menu anterior
            ==> ''')

        if selecao_menu_contas == '1':
            listar_contas(cliente_ativo, contas)
        elif selecao_menu_contas == '2':
            cadastrar_conta(numero_conta, clientes, contas, cliente_ativo)
        elif selecao_menu_contas == '3':
            nova_conta_ativa = selecionar_conta_cliente(cliente_ativo)
            return nova_conta_ativa
        elif selecao_menu_contas == '4':
            return conta_ativa
        else:
            print (' ########  Opção inválida! Tente novamente.  ########')

def menu_geral(clientes, contas, numero_conta, cliente_ativo, conta_ativa=None):
    while True:
        contas_cliente_geral = cliente_ativo.contas
        if len(contas_cliente_geral) == 0:
            escolha_criar_conta = input('''
    Verificamos que seu usuário não possui contas.
    Gostaria de criar uma nova conta? [s/n]
        ==> ''').lower()
            if escolha_criar_conta =='s':
                numero_conta = len(contas) + 1
                contas_cliente_geral = cadastrar_conta_inicio(numero_conta, clientes, contas, cliente_ativo)
            elif escolha_criar_conta == 'n':
                fim_de_operacoes()
                return 
            else:
                print('\t============  Opção inválida! Tente novamente.  ==========')
        else:
            contas_cliente_geral = cliente_ativo.contas
            if len(contas_cliente_geral) == 1:
                conta_ativa = contas_cliente_geral[0]
            elif conta_ativa is None:
                print ('\tEscolha uma conta para movimentar: ')
                conta_ativa = selecionar_conta_cliente(cliente_ativo)
            else:
                pass  

            print(f'''
    ==========================  MENU  ==========================
        Olá, {cliente_ativo.nome.title()}
        Digite o número correspondente a operação desejada:
            [1] Depositar
            [2] Sacar
            [3] Extrato
            [4] Acessar contas
            [5] Sair''')

            operacao = input ('\t\t==> ')
            if operacao == '1':
                depositar(cliente_ativo, conta_ativa)
            elif operacao == '2':
                sacar(cliente_ativo, conta_ativa)
            elif operacao  == '3':
                exibir_extrato(conta_ativa)

            elif operacao == '4':
                conta_ativa = menu_contas(cliente_ativo, conta_ativa, clientes, contas, numero_conta)
            elif operacao == '5':
                fim_de_operacoes()
                break
            else:
                print ('\t============  Opção inválida! Tente novamente.  ==========')

def fim_de_operacoes():
    print ('''
    ==========================================================

                O Banco Mochi agradece sua visita!
                
                        Volte sempre!
           
    ==========================================================
        Contato: tiemi.suyama@gmail.com
                 github.com/mochiemi
           
    ----------------------------------------------------------''')

# ------------- MAIN --------------- #
def main(clientes=[], contas=[], numero_conta=0):
    while True:        
        cpf_inicio = menu_inicio()
        cliente_ativo_inicio = filtrar_cliente(cpf_inicio, clientes)
        if cliente_ativo_inicio:
            cliente_ativo = cliente_ativo_inicio
            menu_geral(clientes, contas, numero_conta, cliente_ativo)
        else:
            novo_cliente = input ('''
    Não foi possível encontrar esse CPF no cadastro. Gostaria de fazer um novo cadastro? [s/n]
        ==> ''').lower()
            if novo_cliente == 's':
                cliente_ativo_cadastro = cadastrar_cliente(clientes)
                cliente_ativo = cliente_ativo_cadastro
            elif novo_cliente == 'n':
                fim_de_operacoes()
            else:
                print ('\n-------------- Comando inválido! Voltando ao menu inicial --------------')

main()