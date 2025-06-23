from data import contactos, clientes
from utils import limpiar_terminal
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def registrar_contacto():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Registro de Contacto[/bold cyan]"))
    
    if contactos:
        console.print("[bold yellow]Contactos existentes (integrantes del grupo):[/bold yellow]")
        for contacto in contactos:
            console.print(f"- {contacto['nombre']} {contacto['apellido']} (Cuenta: {contacto['cuenta']})")
        console.print()
    
    cuenta = Prompt.ask("Número de cuenta del contacto")
    contacto = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not contacto:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    if any(c["cuenta"] == cuenta for c in contactos):
        console.print("[yellow]Este contacto ya está registrado.[/yellow]")
        return

    nuevo_contacto = {
        "nombre": contacto["nombre"],
        "apellido": contacto["apellido"],
        "cuenta": contacto["cuenta"]
    }

    contactos.append(nuevo_contacto)
    console.print("[green]Contacto registrado correctamente.[/green]")

def listar_contactos():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Lista de Contactos[/bold cyan]"))
    
    if not contactos:
        console.print("[bold yellow]No tienes contactos registrados.[/bold yellow]")
        return

    table = Table(title="Contactos Registrados")
    table.add_column("Nombre", style="cyan")
    table.add_column("Apellido", style="cyan")
    table.add_column("Cuenta", style="green")
    table.add_column("Tipo", style="yellow")

    for c in contactos:
        tipo = "Integrante" if c["cuenta"] in ["12345678", "87654321"] else "Agregado"
        table.add_row(c["nombre"], c["apellido"], c["cuenta"], tipo)

    console.print(table)
