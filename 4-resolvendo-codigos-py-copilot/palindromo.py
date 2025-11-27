#Faça um programa que verifique se uma palavra é um palíndromo
palavra = input("Digite uma palavra: ")

def eh_palindromo(palavra):
    if palavra == palavra[::-1]:
        print(f"A palavra '{palavra}' é um palíndromo.")
    else:
        print(f"A palavra '{palavra}' não é um palíndromo.")

def eh_palindromo_string(palavra):
    invertida = ''.join(reversed(palavra))
    if palavra == invertida:
        print(f"(NEW) A palavra '{palavra}' é um palíndromo.")
    else:
        print(f"(NEW) A palavra '{palavra}' não é um palíndromo.")

eh_palindromo(palavra)
eh_palindromo_string(palavra)

