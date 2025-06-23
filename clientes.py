from data import clientes
from utils import validar_run, run_a_cuenta, input_numero, limpiar_terminal, validar_entrada_texto
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def registrar_cliente():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Registro de Nuevo Cliente[/bold cyan]"))
    
    nombre = validar_entrada_texto("Nombre: ")
    apellido = validar_entrada_texto("Apellido: ")
    
    while True:
        run = input("RUN (XX.XXX.XXX-X): ").strip()
        if validar_run(run):
            break
        console.print("[red]❌ RUN inválido. Formato correcto: XX.XXX.XXX-X[/red]")
        console.print("[yellow]Ejemplo: 12.345.678-9[/yellow]")

    if any(c["run"] == run for c in clientes):
        console.print("[yellow]⚠️  Este cliente ya está registrado.[/yellow]")
        return

    cuenta = run_a_cuenta(run)
    console.print(f"[cyan]Número de cuenta generado: {cuenta}[/cyan]")
    
    deposito = input_numero("Monto de depósito inicial: $", 0)

    if deposito <= 100000:
        linea_credito = 50000
        tarjeta = 80000
        categoria = "Básica"
    elif deposito <= 500000:
        linea_credito = 250000
        tarjeta = 300000
        categoria = "Intermedia"
    else:
        linea_credito = 500000
        tarjeta = 700000
        categoria = "Premium"

    console.print(f"\n[bold yellow]📋 Resumen del Cliente:[/bold yellow]")
    console.print(f"👤 Nombre: {nombre} {apellido}")
    console.print(f"🆔 RUN: {run}")
    console.print(f"🏦 Cuenta: {cuenta}")
    console.print(f"💰 Depósito inicial: ${deposito:.2f}")
    console.print(f"🏷️  Categoría: {categoria}")
    console.print(f"💳 Línea de crédito: ${linea_credito:.2f}")
    console.print(f"🎫 Cupo tarjeta: ${tarjeta:.2f}")

    if not Prompt.ask("¿Confirmas el registro?", choices=["s", "n"], default="s") == "s":
        console.print("[yellow]Registro cancelado.[/yellow]")
        return

    # Crear cliente
    cliente = {
        "nombre": nombre,
        "apellido": apellido,
        "run": run,
        "cuenta": cuenta,
        "saldo": float(deposito),  
        "linea_credito": float(linea_credito),  
        "credito_usado": 0.0,  
        "tarjeta_credito": float(tarjeta) 
    }

    clientes.append(cliente)
    console.print(f"\n[bold green]✅ Cliente {nombre} {apellido} registrado exitosamente![/bold green]")
    console.print(f"[green]Cuenta: {cuenta}[/green]")

def listar_clientes():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Listado de Clientes Registrados[/bold cyan]"))
    
    if not clientes:
        console.print("[bold red]❌ No hay clientes registrados.[/bold red]")
        console.print("[yellow]💡 Usa la opción 1 del menú para registrar el primer cliente.[/yellow]")
        return

    table = Table(title=f"Total de Clientes: {len(clientes)}")
    table.add_column("Nombre", style="cyan", width=12)
    table.add_column("Apellido", style="cyan", width=12)
    table.add_column("RUN", style="magenta", width=13)
    table.add_column("Cuenta", style="green", width=10)
    table.add_column("Saldo", justify="right", style="yellow", width=12)
    table.add_column("L. Crédito", justify="right", style="blue", width=12)
    table.add_column("Créd. Usado", justify="right", style="red", width=12)
    table.add_column("Cupo Tarjeta", justify="right", style="purple", width=12)
    table.add_column("Estado", style="white", width=10)

    for c in clientes:
        if c['credito_usado'] > 0:
            estado = "Con deuda"
            estado_style = "red"
        elif c['saldo'] > 100000:
            estado = "Solvente"
            estado_style = "green"
        else:
            estado = "Normal"
            estado_style = "yellow"

        table.add_row(
            c["nombre"], 
            c["apellido"], 
            c["run"], 
            c["cuenta"],
            f"${c['saldo']:.2f}",  
            f"${c['linea_credito']:.2f}",  
            f"${c['credito_usado']:.2f}",  
            f"${c['tarjeta_credito']:.2f}",  
            estado,
            style=estado_style if estado != "Normal" else None
        )

    console.print(table)
    
def buscar_cliente():
    """Nueva función para buscar un cliente específico"""
    limpiar_terminal()
    console.print(Panel("[bold cyan]Buscar Cliente[/bold cyan]"))
    
    if not clientes:
        console.print("[red]No hay clientes registrados.[/red]")
        return
    
    criterio = Prompt.ask("Buscar por", choices=["cuenta", "run", "nombre"])
    
    if criterio == "cuenta":
        valor = input("Número de cuenta: ").strip()
        cliente = next((c for c in clientes if c["cuenta"] == valor), None)
    elif criterio == "run":
        valor = input("RUN: ").strip()
        cliente = next((c for c in clientes if c["run"] == valor), None)
    else:  
        valor = input("Nombre o apellido: ").strip().lower()
        cliente = next((c for c in clientes if valor in c["nombre"].lower() or valor in c["apellido"].lower()), None)
    
    if not cliente:
        console.print("[red]Cliente no encontrado.[/red]")
        return
    
    console.print(f"\n[bold green]Cliente encontrado:[/bold green]")
    
    table = Table(title=f"{cliente['nombre']} {cliente['apellido']}")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="yellow")
    
    table.add_row("Nombre completo", f"{cliente['nombre']} {cliente['apellido']}")
    table.add_row("RUN", cliente['run'])
    table.add_row("Cuenta", cliente['cuenta'])
    table.add_row("Saldo", f"${cliente['saldo']:.2f}")
    table.add_row("Línea de crédito", f"${cliente['linea_credito']:.2f}")
    table.add_row("Crédito usado", f"${cliente['credito_usado']:.2f}")
    table.add_row("Crédito disponible", f"${cliente['linea_credito'] - cliente['credito_usado']:.2f}")
    table.add_row("Cupo tarjeta", f"${cliente['tarjeta_credito']:.2f}")
    table.add_row("Total disponible", f"${cliente['saldo'] + (cliente['linea_credito'] - cliente['credito_usado']):.2f}")
    
    console.print(table)
