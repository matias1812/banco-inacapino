from data import clientes
from utils import validar_run, run_a_cuenta, input_numero, limpiar_terminal
from rich.console import Console
from rich.table import Table

console = Console()

def registrar_cliente():
    limpiar_terminal()
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    run = input("RUN (XX.XXX.XXX-X): ")

    if not validar_run(run):
        console.print("[red]RUN inválido.[/red]")
        return

    if any(c["run"] == run for c in clientes):
        console.print("[yellow]Este cliente ya está registrado.[/yellow]")
        return

    cuenta = run_a_cuenta(run)
    deposito = input_numero("Monto de depósito inicial: ", 0)

    if deposito <= 100000:
        linea_credito = 50000
        tarjeta = 80000
    elif deposito <= 500000:
        linea_credito = 250000
        tarjeta = 300000
    else:
        linea_credito = 500000
        tarjeta = 700000

    cliente = {
        "nombre": nombre,
        "apellido": apellido,
        "run": run,
        "cuenta": cuenta,
        "saldo": deposito,
        "linea_credito": linea_credito,
        "credito_usado": 0,
        "tarjeta_credito": tarjeta
    }

    clientes.append(cliente)
    console.print("[green]Cliente registrado exitosamente.[/green]")

def listar_clientes():
    limpiar_terminal()
    if not clientes:
        console.print("[bold red]No hay clientes registrados.[/bold red]")
        return

    table = Table(title="Listado de Clientes")
    table.add_column("Nombre", style="cyan")
    table.add_column("Apellido", style="cyan")
    table.add_column("RUN", style="magenta")
    table.add_column("Cuenta", style="green")
    table.add_column("Saldo", justify="right")
    table.add_column("Línea Crédito", justify="right")
    table.add_column("Crédito Usado", justify="right")
    table.add_column("Tarjeta Crédito", justify="right")

    for c in clientes:
        table.add_row(
            c["nombre"], c["apellido"], c["run"], c["cuenta"],
            f"${c['saldo']}", f"${c['linea_credito']}", f"${c['credito_usado']}", f"${c['tarjeta_credito']}"
        )

    console.print(table)