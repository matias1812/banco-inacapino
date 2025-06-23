from data import avances, clientes

def pagar_cuota():
    cuenta = input("Ingresa tu número de cuenta: ")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        print("Cuenta no encontrada.")
        return

    avance = next((a for a in avances if a["cuenta"] == cuenta and a["cuotas_pagadas"] < a["cuotas_totales"]), None)
    if not avance:
        print("No tienes avances pendientes.")
        return

    monto_cuota = avance["cuota_mensual"]
    capital_cuota = avance["cuota_base"]

    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])
    if monto_cuota > disponible:
        print("Saldo insuficiente para pagar esta cuota.")
        return

    if cliente["saldo"] >= monto_cuota:
        cliente["saldo"] -= monto_cuota
    else:
        restante = monto_cuota - cliente["saldo"]
        cliente["saldo"] = 0
        cliente["credito_usado"] += restante

    avance["cuotas_pagadas"] += 1
    avance["abonado"] += capital_cuota

    print(f"Cuota #{avance['cuotas_pagadas']} pagada exitosamente.")
    print(f"Capital abonado total: ${avance['abonado']:.2f}")
    print(f"Capital pendiente: ${avance['monto'] - avance['abonado']:.2f}")
