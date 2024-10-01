import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
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
    def historico(self):
        return self._historico
       
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_limite_saques = numero_saques >= self.limite_saques
        excedeu_saldo = valor > self.saldo

        if excedeu_saldo:
            print(f"\n### Operação falhou! Você não tem saldo suficiente (Saldo: R$ {self.saldo:.2f}). ###")
        elif excedeu_limite :
            print(f"\n### Limite (R$ {self.limite:.2f}) de saque excedido ###")
        elif excedeu_limite_saques :
            print(f"\n### Número saques excedido ({self.limite_saques}) ###")
        elif valor > 0 :
            self._saldo -= valor
            print("\n### Saque realizado com sucesso! ###")
            return True
        else :
            print("\n### Valor inválido ###")
                
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n### Depósito realizado com sucesso! ###")
        else :
            print("Valor inválido")
            return False
        
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self.limite = 500
        self.limite_saques = 3
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def __str__(self):
        return f"""
Agência: \t\t{self.agencia}    
Conta Corrente: \t{self.numero}  
Titular: \t\t{self.cliente.nome}  
CPF:     \t\t{self.cliente.cpf}
Valor Limite:   \t{self.limite}
Limite de saques:\t{self.limite_saques}
"""

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass
    

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
        
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
      
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        return f"""
CPF:     \t\t{self.cpf}
Titular: \t\t{self.nome}  
Data de nascimento: \t{self.data_nascimento}    
Endereço: \t\t{self.endereco}  
"""
def main() :
    
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao.upper() == 'D':
            depositar(usuarios, contas)
        elif opcao.upper() == 'S':
            sacar(usuarios, contas)
        elif opcao.upper() == 'E':
            historico(usuarios, contas)
        elif opcao.upper() == 'NU':
            criar_cliente(usuarios)
        elif opcao.upper() == 'LU':
            listar_cliente(usuarios)
        elif opcao.upper() == "NC":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, usuarios, contas)
        elif opcao.upper() == "LC":
            listar_contas(contas)
        elif opcao.upper() == 'X':
            break
        else :
            print('Opção inválida')    
def menu():

    menu = '''

      [d] Depositar
      [s] Sacar
      [e] Extrato
      [nu] Novo usuário
      [lu] Listar usuário
      [nc] Nova conta
      [lc] Listar conta
      [x] Sair

    ==> '''
    return input(textwrap.dedent(menu))
def filtrar_cliente(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def recuperar_conta_cliente(conta_corrente, contas):
   
    conta_filtradas = [cc for cc in contas if cc.numero == conta_corrente]

    return conta_filtradas[0] if conta_filtradas else None

def depositar(usuarios, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, usuarios)
    
    if not cliente:
        print("\n### Não existe cliente com este CPF! ###")
        return
    
    conta_corrente = int(input('Informe a conta corrente do cliente: '))
    conta = recuperar_conta_cliente(conta_corrente, contas)

    if not conta:
        print("\n### Não existe conta para este cliente! ###")
        return
          
    valor = float(input("Informe o valor do depósito: "))

    transacao = Deposito(valor)
    
    cliente.realizar_transacao(conta, transacao)

    return 

def sacar(usuarios, contas):
    
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, usuarios)
    
    if not cliente:
        print("\n### Não existe cliente com este CPF! ###")
        return
    
    conta_corrente = int(input('Informe a conta corrente do cliente: '))
    conta = recuperar_conta_cliente(conta_corrente, contas)

    if not conta:
        print("\n### Não existe conta para este cliente! ###")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)
    
    return
def historico(usuarios, contas):

    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, usuarios)
    
    if not cliente:
        print("\n### Não existe cliente com este CPF! ###")
        return
    
    conta_corrente = int(input('Informe a conta corrente do cliente: '))
    conta = recuperar_conta_cliente(conta_corrente, contas)

    if not conta:
        print("\n### Não existe conta para este cliente! ###")
        return
    

    print("\n=============================================")
    print(conta)
    print("================== EXTRATO ==================")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes :
        extrato = "Não foram realizadas movimentações."
    else :
        for transacao in transacoes :
            extrato += f"\n{transacao['tipo']}:   \t\tR${transacao['valor']:.2f}"
    
    print(extrato)
    print(f'\nSaldo:  \t\tR${conta.saldo:.2f}')
    print("==============================================")

def criar_cliente(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, usuarios)

    if cliente:
        print("\n### Já existe cliente com esse CPF! ###")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    usuarios.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")
def listar_cliente(usuarios):
    if len(usuarios) > 0 :
        print('\n############## Listagem de Clientes ##############')
        for usuario in usuarios: 
            print(usuario)
            # print(f'CPF:                \t{usuario.cpf}')
            # print(f'Nome:               \t{usuario.nome}')
            # print(f'Data de nascimento: \t{usuario.data_nascimento}')
            # print(f'Endereço:           \t{usuario.endereco}')
            print('----------------------------------------------------')      
            
        print('################ Fim da listagem #################')
    else:
        print('Nenhum cliente encontrado')
def criar_conta(numero_conta, usuarios, contas):

    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, usuarios)

    if not cliente:
        print("\n### Cliente não encontrado, fluxo de criação de conta encerrado! ###")
        return
   
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
        
    print(f"\n=== Conta ( {numero_conta} ) criada com sucesso! ===")

def listar_contas(contas):
    print("=" * 90)
    if len(contas) > 0 :
        for conta in contas:
            print(conta)
            print("-" * 90)      
    else: 
        print('### Nenhuma conta cadastrada ###')

main()
