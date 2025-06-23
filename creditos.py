from data import clientes
from utils import input_numero, limpiar_terminal
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

console = Console()

def solicitar_credito_linea():
    """Solicitar crédito directamente de la línea de crédito"""
    limpiar_terminal()
    console.print(Panel("[bold cyan]Solicitud de Crédito - Línea de Crédito[/bold cyan]"))
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    credito_disponible = cliente["linea_credito"] - cliente["credito_usado"]
    console.print(f"\n[cyan]Cliente: {cliente['nombre']} {cliente['apellido']}[/cyan]")
    console.print(f"[cyan]Saldo actual: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Línea de crédito total: ${cliente['linea_credito']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito ya usado: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[bold cyan]Crédito disponible: ${credito_disponible:.2f}[/bold cyan]")

    if credito_disponible <= 0:
        console.print("[red]No tienes crédito disponible en tu línea de crédito.[/red]")
        if cliente["credito_usado"] > 0:
            console.print("[yellow]💡 Realiza un depósito para pagar tu deuda y liberar crédito.[/yellow]")
        return

    monto = input_numero(f"¿Cuánto crédito deseas solicitar? (Máx: ${credito_disponible:.2f}): ", 1)

    if monto > credito_disponible:
        console.print(f"[red]Monto excede el crédito disponible (${credito_disponible:.2f}).[/red]")
        return

    console.print(f"\n[bold yellow]📋 Condiciones del Crédito:[/bold yellow]")
    console.print("💰 Tipo: Línea de crédito rotativa")
    console.print("📈 Interés: Sin interés (se cobra solo si no pagas)")
    console.print("💳 Pago: Flexible - puedes pagar cuando quieras")
    console.print("🔄 Renovable: El crédito se libera al pagar")
    console.print(f"💸 Monto solicitado: ${monto:.2f}")
    console.print(f"🏦 Nuevo crédito usado: ${cliente['credito_usado'] + monto:.2f}")
    console.print(f"📊 Crédito restante: ${credito_disponible - monto:.2f}")

    if not Confirm.ask("\n¿Confirmas la solicitud de crédito?"):
        console.print("[yellow]Solicitud cancelada.[/yellow]")
        return

    cliente["credito_usado"] += monto
    cliente["saldo"] += monto

    console.print(f"\n[bold green]✅ Crédito aprobado y depositado![/bold green]")
    console.print(f"[green]💰 ${monto:.2f} depositados en tu cuenta[/green]")
    console.print(f"[cyan]💳 Nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]🔴 Crédito usado: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[cyan]🟢 Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")

def pagar_credito_linea():
    """Pagar deuda de la línea de crédito"""
    limpiar_terminal()
    console.print(Panel("[bold cyan]Pago de Deuda - Línea de Crédito[/bold cyan]"))
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    if cliente["credito_usado"] <= 0:
        console.print("[green]✅ No tienes deuda en tu línea de crédito.[/green]")
        return

    console.print(f"\n[cyan]Cliente: {cliente['nombre']} {cliente['apellido']}[/cyan]")
    console.print(f"[cyan]Saldo disponible: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[red]Deuda actual: ${cliente['credito_usado']:.2f}[/red]")

    console.print("\n[bold]Opciones de Pago:[/bold]")
    console.print("1. Pago total (pagar toda la deuda)")
    console.print("2. Pago parcial (pagar una parte)")

    opcion = Prompt.ask("Selecciona opción", choices=["1", "2"])

    if opcion == "1":
        monto_pago = cliente["credito_usado"]
        if cliente["saldo"] < monto_pago:
            console.print(f"[red]Saldo insuficiente. Necesitas ${monto_pago:.2f} pero tienes ${cliente['saldo']:.2f}[/red]")
            return
    else:
        monto_pago = input_numero(f"Monto a pagar (máx: ${min(cliente['saldo'], cliente['credito_usado']):.2f}): ", 1)
        
        if monto_pago > cliente["saldo"]:
            console.print(f"[red]Saldo insuficiente. Tienes ${cliente['saldo']:.2f}[/red]")
            return
        
        if monto_pago > cliente["credito_usado"]:
            console.print(f"[red]Monto excede la deuda (${cliente['credito_usado']:.2f})[/red]")
            return

    console.print(f"\n[bold yellow]Resumen del Pago:[/bold yellow]")
    console.print(f"💰 Monto a pagar: ${monto_pago:.2f}")
    console.print(f"💳 Nuevo saldo: ${cliente['saldo'] - monto_pago:.2f}")
    console.print(f"🔴 Nueva deuda: ${cliente['credito_usado'] - monto_pago:.2f}")
    console.print(f"🟢 Crédito liberado: ${monto_pago:.2f}")

    if not Confirm.ask("\n¿Confirmas el pago?"):
        console.print("[yellow]Pago cancelado.[/yellow]")
        return

    cliente["saldo"] -= monto_pago
    cliente["credito_usado"] -= monto_pago

    console.print(f"\n[bold green]✅ Pago procesado exitosamente![/bold green]")
    console.print(f"[cyan]💳 Nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]🔴 Deuda restante: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[cyan]🟢 Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")

    if cliente["credito_usado"] == 0:
        console.print("[bold green]🎉 ¡Felicitaciones! Has pagado toda tu deuda de línea de crédito.[/bold green]")

def consultar_productos_credito():
    """Consultar todos los productos de crédito del cliente"""
    limpiar_terminal()
    console.print(Panel("[bold cyan]Consulta de Productos de Crédito[/bold cyan]"))
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    console.print(f"\n[bold green]Cliente: {cliente['nombre']} {cliente['apellido']}[/bold green]")
    
    table = Table(title="Productos de Crédito")
    table.add_column("Producto", style="cyan")
    table.add_column("Límite/Cupo", justify="right", style="blue")
    table.add_column("Usado", justify="right", style="red")
    table.add_column("Disponible", justify="right", style="green")
    table.add_column("Estado", style="yellow")

    credito_disponible = cliente["linea_credito"] - cliente["credito_usado"]
    estado_linea = "Con deuda" if cliente["credito_usado"] > 0 else "Disponible"
    
    table.add_row(
        "Línea de Crédito",
        f"${cliente['linea_credito']:.2f}",
        f"${cliente['credito_usado']:.2f}",
        f"${credito_disponible:.2f}",
        estado_linea
    )

    table.add_row(
        "Tarjeta de Crédito",
        f"${cliente['tarjeta_credito']:.2f}",
        "N/A",
        f"${cliente['tarjeta_credito']:.2f}",
        "Disponible"
    )

    console.print(table)

    console.print(f"\n[bold cyan]💡 Información:[/bold cyan]")
    console.print("🏦 Línea de Crédito: Para uso general, sin intereses fijos")
    console.print("💳 Tarjeta de Crédito: Para avances con cuotas e intereses")
    console.print("🔄 Ambos productos son independientes")

    if cliente["credito_usado"] > 0:
        console.print(f"\n[yellow]⚠️  Tienes ${cliente['credito_usado']:.2f} de deuda en línea de crédito[/yellow]")
        console.print("[yellow]   Puedes pagarla usando la opción de 'Pagar crédito'[/yellow]")
