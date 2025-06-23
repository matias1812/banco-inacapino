from data import clientes
from utils import input_numero, limpiar_terminal
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from datetime import datetime

console = Console()

historial_movimientos = []

def registrar_movimiento():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Registro de Movimiento[/bold cyan]"))
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])
    console.print(f"\n[cyan]Cliente: {cliente['nombre']} {cliente['apellido']}[/cyan]")
    console.print(f"[cyan]Saldo actual: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Línea de crédito: ${cliente['linea_credito']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito usado: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")
    
    console.print("\n[bold]Tipos de Movimiento:[/bold]")
    console.print("1. Depósito")
    console.print("2. Retiro")
    console.print("3. Pago de servicios")
    
    tipo_opcion = Prompt.ask("Selecciona el tipo de movimiento", choices=["1", "2", "3"])
    
    tipos = {
        "1": ("Depósito", "deposito"),
        "2": ("Retiro", "retiro"), 
        "3": ("Pago de servicios", "pago_servicios")
    }
    
    tipo_nombre, tipo_codigo = tipos[tipo_opcion]
    servicio = ""
    
    if tipo_codigo == "deposito":
        monto = input_numero("Monto a depositar: ", 1)
        procesar_deposito(cliente, monto)
        
    elif tipo_codigo == "retiro":
        console.print(f"[cyan]Disponible para retiro: ${disponible:.2f}[/cyan]")
        monto = input_numero("Monto a retirar: ", 1)
        if not procesar_retiro(cliente, monto):
            return  
        
    elif tipo_codigo == "pago_servicios":
        console.print(f"[cyan]Disponible para pago: ${disponible:.2f}[/cyan]")
        monto = input_numero("Monto del pago: ", 1)
        servicio = Prompt.ask("Nombre del servicio")
        if not procesar_pago_servicio(cliente, monto, servicio):
            return  
    
    movimiento = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cuenta": cuenta,
        "tipo": tipo_nombre,
        "monto": monto,
        "saldo_nuevo": cliente["saldo"],
        "credito_usado": cliente["credito_usado"],
        "descripcion": servicio if tipo_codigo == "pago_servicios" else f"{tipo_nombre} de ${monto:.2f}"
    }
    historial_movimientos.append(movimiento)

def procesar_deposito(cliente, monto):
    """Procesa un depósito - PRIMERO paga deuda de crédito si existe"""
    saldo_anterior = cliente["saldo"]
    credito_anterior = cliente["credito_usado"]
    deuda = cliente["credito_usado"]

    console.print(f"\n[bold yellow]Procesando depósito de ${monto:.2f}...[/bold yellow]")
    
    if deuda > 0:
        pago = min(deuda, monto)
        cliente["credito_usado"] -= pago
        monto -= pago
        console.print(f"[yellow]✅ Se pagó ${pago:.2f} de deuda de crédito.[/yellow]")
        console.print(f"[yellow]Deuda restante: ${cliente['credito_usado']:.2f}[/yellow]")

    cliente["saldo"] += monto
    if monto > 0:
        console.print(f"[green]✅ ${monto:.2f} agregados al saldo.[/green]")
    
    console.print(f"\n[bold green]Depósito procesado exitosamente.[/bold green]")
    console.print(f"[cyan]Saldo anterior: ${saldo_anterior:.2f} → Nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito usado anterior: ${credito_anterior:.2f} → Nuevo: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")

def procesar_retiro(cliente, monto):
    """Procesa un retiro - usa saldo primero, luego crédito"""
    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])
    
    if monto > disponible:
        console.print(f"[red]Fondos insuficientes. Disponible: ${disponible:.2f}[/red]")
        return False
    
    saldo_anterior = cliente["saldo"]
    credito_anterior = cliente["credito_usado"]
    
    console.print(f"\n[bold yellow]Procesando retiro de ${monto:.2f}...[/bold yellow]")
    
    if monto <= cliente["saldo"]:
        cliente["saldo"] -= monto
        console.print(f"[green]✅ Retiro realizado desde saldo en cuenta.[/green]")
    else:
        restante = monto - cliente["saldo"]
        cliente["saldo"] = 0
        cliente["credito_usado"] += restante
        console.print(f"[yellow]✅ Retiro realizado: ${saldo_anterior:.2f} desde saldo, ${restante:.2f} desde línea de crédito.[/yellow]")
    
    console.print(f"\n[bold green]Retiro procesado exitosamente.[/bold green]")
    console.print(f"[cyan]Saldo anterior: ${saldo_anterior:.2f} → Nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito usado anterior: ${credito_anterior:.2f} → Nuevo: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")
    return True

def procesar_pago_servicio(cliente, monto, servicio):
    """Procesa un pago de servicio - usa saldo primero, luego crédito"""
    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])
    
    if monto > disponible:
        console.print(f"[red]Fondos insuficientes para el pago. Disponible: ${disponible:.2f}[/red]")
        return False
    
    saldo_anterior = cliente["saldo"]
    credito_anterior = cliente["credito_usado"]
    
    console.print(f"\n[bold yellow]Procesando pago de {servicio} por ${monto:.2f}...[/bold yellow]")
    
    if monto <= cliente["saldo"]:
        cliente["saldo"] -= monto
        console.print(f"[green]✅ Pago realizado desde saldo en cuenta.[/green]")
    else:
        restante = monto - cliente["saldo"]
        cliente["saldo"] = 0
        cliente["credito_usado"] += restante
        console.print(f"[yellow]✅ Pago realizado: ${saldo_anterior:.2f} desde saldo, ${restante:.2f} desde línea de crédito.[/yellow]")
    
    console.print(f"\n[bold green]Pago de {servicio} procesado exitosamente.[/bold green]")
    console.print(f"[cyan]Saldo anterior: ${saldo_anterior:.2f} → Nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito usado anterior: ${credito_anterior:.2f} → Nuevo: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")
    return True

def mostrar_historial():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Historial de Movimientos[/bold cyan]"))
    
    if not historial_movimientos:
        console.print("[yellow]No hay movimientos registrados.[/yellow]")
        return
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta (o 'todos' para ver todos)")
    
    if cuenta.lower() == "todos":
        movimientos_filtrados = historial_movimientos
    else:
        movimientos_filtrados = [m for m in historial_movimientos if m["cuenta"] == cuenta]
    
    if not movimientos_filtrados:
        console.print("[yellow]No se encontraron movimientos para esta cuenta.[/yellow]")
        return
    
    table = Table(title="Historial de Movimientos")
    table.add_column("Fecha", style="cyan")
    table.add_column("Cuenta", style="green")
    table.add_column("Tipo", style="yellow")
    table.add_column("Monto", justify="right", style="red")
    table.add_column("Saldo Final", justify="right")
    table.add_column("Crédito Usado", justify="right")
    table.add_column("Descripción", style="magenta")
    
    for mov in movimientos_filtrados[-10:]:  
        table.add_row(
            mov["fecha"],
            mov["cuenta"],
            mov["tipo"],
            f"${mov['monto']:.2f}",
            f"${mov['saldo_nuevo']:.2f}",
            f"${mov['credito_usado']:.2f}",
            mov["descripcion"]
        )
    
    console.print(table)
