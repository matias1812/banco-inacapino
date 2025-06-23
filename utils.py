import re

def validar_run(run):
    return bool(re.match(r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$', run))

def run_a_cuenta(run):
    return run.split('-')[0].replace('.', '')

def input_numero(mensaje, minimo=0):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < minimo:
                raise ValueError
            return valor
        except ValueError:
            print(f"Ingrese un número válido mayor o igual a {minimo}.")
