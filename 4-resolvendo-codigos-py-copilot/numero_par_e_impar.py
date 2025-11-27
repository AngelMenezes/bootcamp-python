# Como entrada, o programa recebe um número e verifica se ele é par ou ímpar
numero = int(input("Digite um número inteiro: "))
resultado = "par" if numero % 2 == 0 else "ímpar"
print(f"O número é {resultado}.")
