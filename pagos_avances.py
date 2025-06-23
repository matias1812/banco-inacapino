from data import avances, clientes
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

console = Console()

def pagar_cuota():
    console.clear()
    console.print(Panel("[bold cyan]Pago de Cuota de Avance[/bold cyan]"))
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    avances_pendientes = [a for a in avances if a["cuenta"] == cuenta and a["cuotas_pagadas"] < a["cuotas_totales"]]
    
    if not avances_pendientes:
        console.print("[yellow]No tienes avances pendientes.[/yellow]")
        return

    if len(avances_pendientes) > 1:
        console.print("\n[bold]Avances Pendientes:[/bold]")
        for i, avance in enumerate(avances_pendientes, 1):
            cuotas_restantes = avance["cuotas_totales"] - avance["cuotas_pagadas"]
            console.print(f"{i}. Avance de ${avance['monto']:.2f} - {cuotas_restantes} cuotas restantes")
        
        opcion = int(Prompt.ask("Selecciona el avance a pagar", choices=[str(i) for i in range(1, len(avances_pendientes) + 1)]))
        avance = avances_pendientes[opcion - 1]
    else:
        avance = avances_pendientes[0]

    cuota_actual = avance["cuotas_pagadas"] + 1
    monto_cuota = avance["cuota_mensual"]
    capital_cuota = avance["cuota_base"]
    interes_cuota = monto_cuota - capital_cuota

    console.print(f"\n[bold cyan]Información de la Cuota:[/bold cyan]")
    console.print(f"📋 Cuota #{cuota_actual} de {avance['cuotas_totales']}")
    console.print(f"💰 Monto total de la cuota: ${monto_cuota:.2f}")
    console.print(f"🏛️  Capital: ${capital_cuota:.2f}")
    console.print(f"📈 Interés: ${interes_cuota:.2f}")

    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])
    console.print(f"\n[cyan]Saldo disponible: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[bold cyan]Total disponible: ${disponible:.2f}[/bold cyan]")

    if monto_cuota > disponible:
        console.print("[red]Saldo insuficiente para pagar esta cuota.[/red]")
        return

    if not Confirm.ask(f"\n¿Confirmas el pago de la cuota #{cuota_actual} por ${monto_cuota:.2f}?"):
        console.print("[yellow]Pago cancelado.[/yellow]")
        return

    if cliente["saldo"] >= monto_cuota:
        cliente["saldo"] -= monto_cuota
        console.print(f"[green]Pago realizado desde saldo en cuenta.[/green]")
    else:
        restante = monto_cuota - cliente["saldo"]
        cliente["saldo"] = 0
        cliente["credito_usado"] += restante
        console.print(f"[yellow]Pago realizado: ${monto_cuota - restante:.2f} desde saldo, ${restante:.2f} desde línea de crédito.[/yellow]")

    avance["cuotas_pagadas"] += 1
    avance["abonado"] += capital_cuota

    capital_pendiente = avance["monto"] - avance["abonado"]
    cuotas_restantes = avance["cuotas_totales"] - avance["cuotas_pagadas"]

    console.print(f"\n[bold green]✅ Cuota #{avance['cuotas_pagadas']} pagada exitosamente![/bold green]")
    
    table = Table(title="Resumen del Avance")
    table.add_column("Concepto", style="cyan")
    table.add_column("Monto", justify="right", style="yellow")
    
    table.add_row("Capital abonado total", f"${avance['abonado']:.2f}")
    table.add_row("Capital pendiente", f"${capital_pendiente:.2f}")
    table.add_row("Cuotas pagadas", f"{avance['cuotas_pagadas']}")
    table.add_row("Cuotas restantes", f"{cuotas_restantes}")
    
    if cuotas_restantes > 0:
        table.add_row("Próxima cuota", f"${avance['cuota_mensual']:.2f}")
    else:
        table.add_row("Estado", "¡PAGADO COMPLETAMENTE!")
        cliente["tarjeta_credito"] += avance["monto"]
        console.print(f"[green]🎉 ¡Avance pagado completamente! Cupo de tarjeta restaurado.[/green]")

    console.print(table)
    
    console.print(f"\n[cyan]Nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito usado: ${cliente['credito_usado']:.2f}[/cyan]")
