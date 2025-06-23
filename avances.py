from data import avances, clientes
from utils import input_numero
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def solicitar_avance():
    console.clear()
    console.print(Panel("[bold cyan]Solicitud de Avance con Tarjeta[/bold cyan]"))
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    disponible = cliente["tarjeta_credito"]
    monto = input_numero(f"¿Cuánto deseas avanzar? (Máx: {disponible}): ", 1)

    if monto > disponible:
        console.print("[yellow]No tienes suficiente cupo en tu tarjeta.[/yellow]")
        return

    console.print("[bold]Opciones de cuotas:[/bold]")
    console.print("1. 12 cuotas - 1.5% mensual")
    console.print("2. 24 cuotas - 3% mensual")
    console.print("3. 36 cuotas - 4% mensual")
    console.print("4. 48 cuotas - 5% mensual")

    opciones = {
        "1": (12, 0.015),
        "2": (24, 0.03),
        "3": (36, 0.04),
        "4": (48, 0.05)
    }

    op = Prompt.ask("Elige opción de cuotas")
    if op not in opciones:
        console.print("[red]Opción inválida.[/red]")
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

    console.print(f"[green]Avance aprobado y depositado en tu cuenta.[/green]")
    console.print(f"Total cuotas: {cuotas}, Cuota mensual: [bold yellow]${cuota_total:.2f}[/bold yellow]")

