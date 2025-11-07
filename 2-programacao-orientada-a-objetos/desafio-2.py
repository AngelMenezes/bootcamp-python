import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


class Cliente:
    """Classe que representa um cliente do banco."""

    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas: List['Conta'] = []

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao') -> None:
        """Realiza uma transação em uma conta."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta: 'Conta') -> None:
        """Adiciona uma conta ao cliente."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """Classe que representa uma pessoa física como cliente do banco."""

    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"PessoaFisica(nome='{self.nome}', cpf='{self.cpf}')"


class Conta:
    """Classe que representa uma conta bancária."""

    def __init__(self, numero: int, cliente: Cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        """Método factory para criar uma nova conta."""
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        """Retorna o saldo atual da conta."""
        return self._saldo

    @property
    def numero(self) -> int:
        """Retorna o número da conta."""
        return self._numero

    @property
    def agencia(self) -> str:
        """Retorna a agência da conta."""
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        """Retorna o cliente titular da conta."""
        return self._cliente

    @property
    def historico(self) -> 'Historico':
        """Retorna o histórico de transações da conta."""
        return self._historico

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta.

        Args:
            valor: Valor a ser sacado

        Returns:
            True se o saque foi bem-sucedido, False caso contrário
        """
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor: float) -> bool:
        """
        Realiza um depósito na conta.

        Args:
            valor: Valor a ser depositado

        Returns:
            True se o depósito foi bem-sucedido, False caso contrário
        """
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    """Classe que representa uma conta corrente com limite de saque."""

    def __init__(self, numero: int, cliente: Cliente, limite: float = 500, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self) -> float:
        """Retorna o limite de saque por transação."""
        return self._limite

    @property
    def limite_saques(self) -> int:
        """Retorna o limite de saques diários."""
        return self._limite_saques

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta corrente respeitando limites.

        Args:
            valor: Valor a ser sacado

        Returns:
            True se o saque foi bem-sucedido, False caso contrário
        """
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        if excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        return super().sacar(valor)

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

    def __repr__(self) -> str:
        return f"ContaCorrente(numero={self.numero}, agencia='{self.agencia}', saldo={self.saldo:.2f})"


class Historico:
    """Classe que representa o histórico de transações de uma conta."""

    def __init__(self):
        self._transacoes: List[dict] = []

    @property
    def transacoes(self) -> List[dict]:
        """Retorna a lista de transações."""
        return self._transacoes

    def adicionar_transacao(self, transacao: 'Transacao') -> None:
        """
        Adiciona uma transação ao histórico.

        Args:
            transacao: Transação a ser adicionada
        """
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self) -> str:
        """Gera um relatório formatado do histórico de transações."""
        if not self._transacoes:
            return "Nenhuma transação realizada."

        relatorio = "\n========== HISTÓRICO DE TRANSAÇÕES ==========\n"
        for transacao in self._transacoes:
            relatorio += f"\n{transacao['tipo']}:\n"
            relatorio += f"  Valor: R$ {transacao['valor']:.2f}\n"
            relatorio += f"  Data: {transacao['data']}\n"
        relatorio += "\n============================================\n"
        return relatorio


class Transacao(ABC):
    """Classe abstrata para representar uma transação bancária."""

    @property
    @abstractmethod
    def valor(self):
        """Retorna o valor da transação."""
        pass

    @abstractmethod
    def registrar(self, conta):
        """Registra a transação na conta especificada."""
        pass


class Saque(Transacao):
    """Classe que representa uma transação de saque."""

    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        """Retorna o valor do saque."""
        return self._valor

    def registrar(self, conta: Conta) -> None:
        """
        Registra o saque na conta.

        Args:
            conta: Conta onde o saque será realizado
        """
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """Classe que representa uma transação de depósito."""

    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        """Retorna o valor do depósito."""
        return self._valor

    def registrar(self, conta: Conta) -> None:
        """
        Registra o depósito na conta.

        Args:
            conta: Conta onde o depósito será realizado
        """
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# ==================== FUNÇÕES DO MENU ====================

def menu():
    """Exibe o menu principal e retorna a opção escolhida."""
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf: str, clientes: List[PessoaFisica]) -> Optional[PessoaFisica]:
    """
    Filtra e retorna um cliente pelo CPF.

    Args:
        cpf: CPF do cliente
        clientes: Lista de clientes

    Returns:
        Cliente encontrado ou None
    """
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente: PessoaFisica) -> Optional[Conta]:
    """
    Recupera a conta de um cliente.

    Args:
        cliente: Cliente

    Returns:
        Conta do cliente ou None
    """
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes: List[PessoaFisica]) -> None:
    """
    Realiza um depósito em uma conta.

    Args:
        clientes: Lista de clientes
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes: List[PessoaFisica]) -> None:
    """
    Realiza um saque de uma conta.

    Args:
        clientes: Lista de clientes
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes: List[PessoaFisica]) -> None:
    """
    Exibe o extrato de uma conta.

    Args:
        clientes: Lista de clientes
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.gerar_relatorio()
    print(transacoes)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes: List[PessoaFisica]) -> None:
    """
    Cria um novo cliente (usuário).

    Args:
        clientes: Lista de clientes
    """
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta: int, clientes: List[PessoaFisica], contas: List[Conta]) -> int:
    """
    Cria uma nova conta para um cliente.

    Args:
        numero_conta: Número da próxima conta
        clientes: Lista de clientes
        contas: Lista de contas

    Returns:
        Novo número de conta
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return numero_conta

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")
    return numero_conta + 1


def listar_contas(contas: List[Conta]) -> None:
    """
    Lista todas as contas cadastradas.

    Args:
        contas: Lista de contas
    """
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))


def main():
    """Função principal que executa o loop do menu."""
    clientes: List[PessoaFisica] = []
    contas: List[Conta] = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\n=== Obrigado por usar nosso sistema! ===")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()
