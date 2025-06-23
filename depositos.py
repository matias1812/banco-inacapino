from utils import input_numero, limpiar_terminal
from rich.console import Console
from rich.panel import Panel

console = Console()

def depositar(cliente):
    limpiar_terminal()
    console.print(Panel("[bold cyan]Depósito de Dinero[/bold cyan]"))
    
    console.print(f"[cyan]Saldo actual: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Deuda de crédito: ${cliente['credito_usado']:.2f}[/cyan]")
    
    monto = input_numero("Monto a depositar: ", 1)
    deuda = cliente["credito_usado"]

    if deuda > 0:
        pago = min(deuda, monto)
        cliente["credito_usado"] -= pago
        monto -= pago
        console.print(f"[yellow]Se pagó ${pago:.2f} de deuda de crédito.[/yellow]")
        console.print(f"[yellow]Deuda restante: ${cliente['credito_usado']:.2f}[/yellow]")

    cliente["saldo"] += monto
    console.print(f"[green]Depósito realizado con éxito.[/green]")
    console.print(f"[cyan]Nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")
    console.print("[bold green]Presione Enter para continuar...[/bold green]")