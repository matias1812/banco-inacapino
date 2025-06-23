from data import avances, clientes
from utils import input_numero, limpiar_terminal
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

console = Console()

def solicitar_avance():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Solicitud de Avance con Tarjeta de Crédito[/bold cyan]"))
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    console.print(f"\n[cyan]Cliente: {cliente['nombre']} {cliente['apellido']}[/cyan]")
    console.print(f"[cyan]Saldo actual: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Cupo disponible en tarjeta: ${cliente['tarjeta_credito']:.2f}[/cyan]")
    
    if cliente['credito_usado'] > 0:
        console.print(f"[yellow]⚠️  Deuda en línea de crédito: ${cliente['credito_usado']:.2f}[/yellow]")
        console.print("[yellow]Nota: El avance NO se usará para pagar esta deuda automáticamente[/yellow]")

    avances_pendientes = [a for a in avances if a["cuenta"] == cuenta and a["cuotas_pagadas"] < a["cuotas_totales"]]
    if avances_pendientes:
        console.print(f"[yellow]⚠️  Tienes {len(avances_pendientes)} avance(s) pendiente(s)[/yellow]")

    disponible = cliente["tarjeta_credito"]
    if disponible <= 0:
        console.print("[red]No tienes cupo disponible en tu tarjeta.[/red]")
        return

    monto = input_numero(f"¿Cuánto deseas avanzar? (Máx: ${disponible:.2f}): ", 1)

    if monto > disponible:
        console.print("[yellow]No tienes suficiente cupo en tu tarjeta.[/yellow]")
        return

    console.print("\n[bold]Opciones de Financiamiento:[/bold]")
    
    table = Table()
    table.add_column("Opción", style="cyan")
    table.add_column("Cuotas", justify="center")
    table.add_column("Interés Mensual", justify="center")
    table.add_column("Cuota Mensual", justify="right", style="yellow")
    table.add_column("Total a Pagar", justify="right", style="red")

    opciones = {
        "1": (12, 0.015, "Corto plazo"),
        "2": (24, 0.03, "Mediano plazo"),
        "3": (36, 0.04, "Largo plazo"),
        "4": (48, 0.05, "Muy largo plazo")
    }

    for key, (cuotas, interes, descripcion) in opciones.items():
        cuota_base = monto / cuotas
        cuota_total = cuota_base * (1 + interes)
        total_pagar = cuota_total * cuotas
        
        table.add_row(
            f"{key}. {descripcion}",
            str(cuotas),
            f"{interes*100:.1f}%",
            f"${cuota_total:.2f}",
            f"${total_pagar:.2f}"
        )

    console.print(table)

    op = Prompt.ask("Elige opción de cuotas", choices=["1", "2", "3", "4"])
    cuotas, interes, descripcion = opciones[op]
    
    cuota_base = monto / cuotas
    cuota_total = cuota_base * (1 + interes)
    total_pagar = cuota_total * cuotas
    total_intereses = total_pagar - monto

    console.print(f"\n[bold yellow]📋 Resumen del Avance:[/bold yellow]")
    console.print(f"💰 Monto solicitado: ${monto:.2f}")
    console.print(f"📅 Plan: {cuotas} cuotas ({descripcion})")
    console.print(f"💳 Cuota mensual: ${cuota_total:.2f}")
    console.print(f"💸 Total a pagar: ${total_pagar:.2f}")
    console.print(f"📈 Total intereses: ${total_intereses:.2f}")
    console.print(f"🏦 Nuevo cupo tarjeta: ${cliente['tarjeta_credito'] - monto:.2f}")

    if not Confirm.ask("\n¿Confirmas la solicitud del avance?"):
        console.print("[yellow]Operación cancelada.[/yellow]")
        return

    avance = {
        "cuenta": cuenta,
        "monto": monto,
        "cuotas_totales": cuotas,
        "cuotas_pagadas": 0,
        "interes": interes,
        "cuota_mensual": round(cuota_total, 2),
        "cuota_base": round(cuota_base, 2),
        "abonado": 0,
        "descripcion": descripcion
    }

    cliente["tarjeta_credito"] -= monto
    
    cliente["saldo"] += monto  
    
    avances.append(avance)

    console.print(f"\n[bold green]✅ Avance aprobado y procesado exitosamente![/bold green]")
    console.print(f"[green]💰 ${monto:.2f} depositados en tu cuenta[/green]")
    console.print(f"[cyan]💳 Nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]🏦 Cupo restante tarjeta: ${cliente['tarjeta_credito']:.2f}[/cyan]")
    console.print(f"[yellow]📅 Próxima cuota: ${cuota_total:.2f}[/yellow]")
    
    if cliente['credito_usado'] > 0:
        console.print(f"[yellow]⚠️  Recuerda: Aún tienes ${cliente['credito_usado']:.2f} de deuda en línea de crédito[/yellow]")

def mostrar_avances_cliente():
    """Función adicional para mostrar todos los avances de un cliente"""
    limpiar_terminal()
    console.print(Panel("[bold cyan]Consulta de Avances[/bold cyan]"))
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    avances_cliente = [a for a in avances if a["cuenta"] == cuenta]
    
    if not avances_cliente:
        console.print("[yellow]No tienes avances registrados.[/yellow]")
        return

    console.print(f"\n[bold cyan]Avances de {cliente['nombre']} {cliente['apellido']}[/bold cyan]")
    
    for i, avance in enumerate(avances_cliente, 1):
        estado = "✅ Pagado" if avance["cuotas_pagadas"] >= avance["cuotas_totales"] else "⏳ Pendiente"
        pendiente = avance["monto"] - avance["abonado"]
        cuotas_restantes = avance["cuotas_totales"] - avance["cuotas_pagadas"]
        
        console.print(f"\n[bold yellow]Avance #{i}[/bold yellow]")
        console.print(f"💰 Monto original: ${avance['monto']:.2f}")
        console.print(f"📅 Plan: {avance['cuotas_totales']} cuotas ({avance.get('descripcion', 'N/A')})")
        console.print(f"✅ Cuotas pagadas: {avance['cuotas_pagadas']}")
        console.print(f"⏳ Cuotas restantes: {cuotas_restantes}")
        console.print(f"💳 Próxima cuota: ${avance['cuota_mensual']:.2f}")
        console.print(f"💸 Capital abonado: ${avance['abonado']:.2f}")
        console.print(f"📊 Capital pendiente: ${pendiente:.2f}")
        console.print(f"🏷️  Estado: {estado}")
