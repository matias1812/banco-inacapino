from data import clientes, contactos
from utils import input_numero, limpiar_terminal
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def transferir():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Transferencia de Dinero[/bold cyan]"))
    
    origen_cuenta = Prompt.ask("Tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == origen_cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    destino_cuenta = Prompt.ask("Cuenta destino (debe estar en tus contactos)")
    if not any(c["cuenta"] == destino_cuenta for c in contactos):
        console.print("[red]No puedes transferir a esa cuenta.[/red]")
        return

    monto = input_numero("Monto a transferir: ", 1)
    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])

    if monto > disponible:
        console.print("[red]Saldo insuficiente.[/red]")
        return

    if monto <= cliente["saldo"]:
        cliente["saldo"] -= monto
    else:
        restante = monto - cliente["saldo"]
        cliente["saldo"] = 0
        cliente["credito_usado"] += restante

    destino = next(c for c in clientes if c["cuenta"] == destino_cuenta)
    destino["saldo"] += monto
    console.print(f"[green]Transferencia exitosa de ${monto:.2f}[/green]")
