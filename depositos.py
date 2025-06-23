from utils import input_numero, limpiar_terminal
from rich.console import Console
from rich.panel import Panel

console = Console()

def depositar(cliente):
    limpiar_terminal()
    console.print(Panel("[bold cyan]Depósito de Dinero[/bold cyan]"))
    
    monto = input_numero("Monto a depositar: ", 1)
    deuda = cliente["credito_usado"]

    if deuda > 0:
        pago = min(deuda, monto)
        cliente["credito_usado"] -= pago
        monto -= pago
        console.print(f"[yellow]Se pagó ${pago:.2f} de deuda pendiente.[/yellow]")

    cliente["saldo"] += monto
    console.print(f"[green]Depósito realizado con éxito. Nuevo saldo: ${cliente['saldo']:.2f}[/green]")
