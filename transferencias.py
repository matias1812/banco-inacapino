from data import clientes, contactos
from utils import input_numero, limpiar_terminal
from rich.console import Console
from rich.prompt import Prompt, Confirm
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

    disponible = cliente["saldo"] + (cliente["linea_credito"] - cliente["credito_usado"])
    console.print(f"\n[cyan]Cliente: {cliente['nombre']} {cliente['apellido']}[/cyan]")
    console.print(f"[cyan]Saldo en cuenta: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Línea de crédito: ${cliente['linea_credito']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito usado: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[bold cyan]Total disponible para transferir: ${disponible:.2f}[/bold cyan]")

    destino_cuenta = Prompt.ask("Cuenta destino (debe estar en tus contactos)")
    if not any(c["cuenta"] == destino_cuenta for c in contactos):
        console.print("[red]No puedes transferir a esa cuenta (no está en tus contactos).[/red]")
        return

    destino = next((c for c in clientes if c["cuenta"] == destino_cuenta), None)
    if not destino:
        console.print("[red]La cuenta destino no existe en el sistema.[/red]")
        return

    monto = input_numero("Monto a transferir: ", 1)

    if monto > disponible:
        console.print(f"[red]Saldo insuficiente. Disponible: ${disponible:.2f}[/red]")
        return

    console.print(f"\n[bold yellow]Resumen de la transferencia:[/bold yellow]")
    console.print(f"Destino: {destino['nombre']} {destino['apellido']} (Cuenta: {destino_cuenta})")
    console.print(f"Monto: ${monto:.2f}")
    
    if monto > cliente["saldo"]:
        uso_credito = monto - cliente["saldo"]
        console.print(f"[yellow]Se usará ${uso_credito:.2f} de tu línea de crédito[/yellow]")

    if not Confirm.ask("¿Confirmas la transferencia?"):
        console.print("[yellow]Transferencia cancelada.[/yellow]")
        return

    saldo_anterior = cliente["saldo"]
    credito_anterior = cliente["credito_usado"]

    if monto <= cliente["saldo"]:
        cliente["saldo"] -= monto
        console.print(f"[green]Transferencia realizada desde saldo en cuenta.[/green]")
    else:
        restante = monto - cliente["saldo"]
        cliente["saldo"] = 0
        cliente["credito_usado"] += restante
        console.print(f"[yellow]Transferencia realizada: ${saldo_anterior:.2f} desde saldo, ${restante:.2f} desde línea de crédito.[/yellow]")

    destino["saldo"] += monto
    
    console.print(f"\n[bold green]✅ Transferencia exitosa de ${monto:.2f}[/bold green]")
    console.print(f"[cyan]Tu nuevo saldo: ${cliente['saldo']:.2f}[/cyan]")
    console.print(f"[cyan]Tu crédito usado: ${cliente['credito_usado']:.2f}[/cyan]")
    console.print(f"[cyan]Crédito disponible: ${cliente['linea_credito'] - cliente['credito_usado']:.2f}[/cyan]")
