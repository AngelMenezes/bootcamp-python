#vamos solicitar como entrada dois números inteiros e realizar a operação de soma entre eles
num1 = int(input("Digite o primeiro número inteiro: ")) 
num2 = int(input("Digite o segundo número inteiro: "))
operacao = input("Escolha a operação (+, -, *, /): ")

if operacao == "+":
    resultado = num1 + num2
    print("Resultado da soma:", resultado)
elif operacao == "-":
    resultado = num1 - num2
    print("Resultado da subtração:", resultado)
elif operacao == "*":
    resultado = num1 * num2
    print("Resultado da multiplicação:", resultado)
elif operacao == "/":
    if num2 != 0:
        resultado = num1 / num2
        print("Resultado da divisão:", resultado)
    else:
        print("Não é possível dividir por zero.")
else:
    print("Operação inválida.")