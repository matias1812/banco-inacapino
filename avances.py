from data import avances, clientes
from utils import input_numero

def solicitar_avance():
    cuenta = input("Ingresa tu número de cuenta: ")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        print("Cuenta no encontrada.")
        return

    disponible = cliente["tarjeta_credito"]
    monto = input_numero(f"¿Cuánto deseas avanzar? (Máx: {disponible}): ", 1)

    if monto > disponible:
        print("No tienes suficiente cupo en tu tarjeta.")
        return

    print("Opciones de cuotas:")
    print("1. 12 cuotas - 1.5% mensual")
    print("2. 24 cuotas - 3% mensual")
    print("3. 36 cuotas - 4% mensual")
    print("4. 48 cuotas - 5% mensual")

    opciones = {
        "1": (12, 0.015),
        "2": (24, 0.03),
        "3": (36, 0.04),
        "4": (48, 0.05)
    }

    op = input("Elige opción de cuotas: ")
    if op not in opciones:
        print("Opción inválida.")
        return

    cuotas, interes = opciones[op]
    cuota_base = monto / cuotas
    cuota_total = cuota_base * (1 + interes)

    avance = {
        "cuenta": cuenta,
        "monto": monto,
        "cuotas_totales": cuotas,
        "cuotas_pagadas": 0,
        "interes": interes,
        "cuota_mensual": round(cuota_total, 2),
        "cuota_base": round(cuota_base, 2),
        "abonado": 0
    }

    avances.append(avance)
    cliente["saldo"] += monto

    print(f"Avance aprobado y depositado en tu cuenta.")
    print(f"Total cuotas: {cuotas}, Cuota mensual: ${cuota_total:.2f}")
