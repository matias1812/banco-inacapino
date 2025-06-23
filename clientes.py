from data import clientes
from utils import validar_run, run_a_cuenta, input_numero

def registrar_cliente():
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    run = input("RUN (XX.XXX.XXX-X): ")
    if not validar_run(run):
        print("RUN inválido.")
        return

    cuenta = run_a_cuenta(run)
    deposito = input_numero("Monto de depósito inicial: ", 0)

    if deposito <= 100000:
        linea_credito = 50000
        tarjeta = 80000
    elif deposito <= 500000:
        linea_credito = 250000
        tarjeta = 300000
    else:
        linea_credito = 500000
        tarjeta = 700000

    cliente = {
        "nombre": nombre,
        "apellido": apellido,
        "run": run,
        "cuenta": cuenta,
        "saldo": deposito,
        "linea_credito": linea_credito,
        "credito_usado": 0,
        "tarjeta_credito": tarjeta
    }

    clientes.append(cliente)
    print("Cliente registrado exitosamente.")

def listar_clientes():
    for cliente in clientes:
        print(cliente)
