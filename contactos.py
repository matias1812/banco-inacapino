from data import contactos, clientes
from utils import limpiar_terminal
from rich.console import Console
from rich.table import Table

console = Console()

def registrar_contacto():
    limpiar_terminal()
    cuenta = input("Número de cuenta del contacto: ")
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
    if not contactos:
        console.print("[bold yellow]No tienes contactos registrados.[/bold yellow]")
        return

    table = Table(title="Contactos Registrados")
    table.add_column("Nombre")
    table.add_column("Apellido")
    table.add_column("Cuenta")

    for c in contactos:
        table.add_row(c["nombre"], c["apellido"], c["cuenta"])

    console.print(table)

