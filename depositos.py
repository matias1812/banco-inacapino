def depositar(cliente):
    from utils import input_numero
    monto = input_numero("Monto a depositar: ", 1)
    deuda = cliente["credito_usado"]

    if deuda > 0:
        pago = min(deuda, monto)
        cliente["credito_usado"] -= pago
        monto -= pago

    cliente["saldo"] += monto
    print("Depósito realizado con éxito.")
