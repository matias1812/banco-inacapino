from data import clientes, contactos
from utils import input_numero

def transferir():
    origen_cuenta = input("Tu número de cuenta: ")
    cliente = next((c for c in clientes if c["cuenta"] == origen_cuenta), None)
    if not cliente:
        print("Cuenta no encontrada.")
        return

    destino_cuenta = input("Cuenta destino (debe estar en tus contactos): ")
    if not any(c["cuenta"] == destino_cuenta for c in contactos):
        print("No puedes transferir a esa cuenta.")
        return

    monto = input_numero("Monto a transferir: ", 1)
    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])

    if monto > disponible:
        print("Saldo insuficiente.")
        return

    if monto <= cliente["saldo"]:
        cliente["saldo"] -= monto
    else:
        restante = monto - cliente["saldo"]
        cliente["saldo"] = 0
        cliente["credito_usado"] += restante

    destino = next(c for c in clientes if c["cuenta"] == destino_cuenta)
    destino["saldo"] += monto
    print("Transferencia exitosa.")
