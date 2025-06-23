from data import avances, clientes
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def pagar_cuota():
    console.clear()
    console.print(Panel("[bold cyan]Pago de Cuota de Avance[/bold cyan]"))
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    avance = next((a for a in avances if a["cuenta"] == cuenta and a["cuotas_pagadas"] < a["cuotas_totales"]), None)
    if not avance:
        console.print("[yellow]No tienes avances pendientes.[/yellow]")
        return

    monto_cuota = avance["cuota_mensual"]
    capital_cuota = avance["cuota_base"]

    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])
    if monto_cuota > disponible:
        console.print("[red]Saldo insuficiente para pagar esta cuota.[/red]")
        return

    if cliente["saldo"] >= monto_cuota:
        cliente["saldo"] -= monto_cuota
    else:
        restante = monto_cuota - cliente["saldo"]
        cliente["saldo"] = 0
        cliente["credito_usado"] += restante

    avance["cuotas_pagadas"] += 1
    avance["abonado"] += capital_cuota

    console.print(f"[green]Cuota #{avance['cuotas_pagadas']} pagada exitosamente.[/green]")
    console.print(f"Capital abonado total: [bold yellow]${avance['abonado']:.2f}[/bold yellow]")
    console.print(f"Capital pendiente: [bold red]${avance['monto'] - avance['abonado']:.2f}[/bold red]")
