import re
import os

def validar_run(run):
    """Criterio 2: Validación del RUN (formato y estructura) (5 pts)"""
    if not isinstance(run, str):
        return False
    
    patron = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
    if not re.match(patron, run):
        return False
    
    try:
        rut_sin_dv = run.split('-')[0].replace('.', '')
        dv = run.split('-')[1].upper()
        
        suma = 0
        multiplicador = 2
        
        for digito in reversed(rut_sin_dv):
            suma += int(digito) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2
        
        resto = suma % 11
        dv_calculado = 11 - resto
        
        if dv_calculado == 11:
            dv_calculado = '0'
        elif dv_calculado == 10:
            dv_calculado = 'K'
        else:
            dv_calculado = str(dv_calculado)
        
        return dv == dv_calculado
    except:
        return False

def run_a_cuenta(run):
    """Criterio 3: Generación correcta del número de cuenta (sin DV) (5 pts)"""
    return run.split('-')[0].replace('.', '')

def input_numero(mensaje, minimo=0):
    """Criterio 20: Validación y sanitización de entradas (5 pts)"""
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada:
                raise ValueError("No puede estar vacío")
            
            valor = float(entrada)
            if valor < minimo:
                raise ValueError(f"El valor debe ser mayor o igual a {minimo}")
            
            return valor
        except ValueError as e:
            if "could not convert" in str(e):
                print(f"Error: Ingrese un número válido.")
            else:
                print(f"Error: {e}")

def limpiar_terminal():
    """Limpiar la terminal para mejor presentación"""
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_entrada_texto(mensaje, min_length=1, max_length=50):
    """Validación adicional para entradas de texto"""
    while True:
        entrada = input(mensaje).strip()
        if len(entrada) < min_length:
            print(f"Error: Debe tener al menos {min_length} caracteres.")
            continue
        if len(entrada) > max_length:
            print(f"Error: No puede exceder {max_length} caracteres.")
            continue
        if not entrada.replace(' ', '').isalpha():
            print("Error: Solo se permiten letras y espacios.")
            continue
        return entrada.title()  