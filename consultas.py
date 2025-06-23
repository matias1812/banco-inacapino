from data import clientes, avances
from utils import limpiar_terminal
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def consultar_saldo():
    limpiar_terminal()
    console.print(Panel("[bold cyan]Consulta de Saldo y Estado de Cuenta[/bold cyan]"))
    
    cuenta = Prompt.ask("Ingresa tu número de cuenta")
    cliente = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not cliente:
        console.print("[red]Cuenta no encontrada.[/red]")
        return

    console.print(f"\n[bold green]Cliente: {cliente['nombre']} {cliente['apellido']}[/bold green]")
    console.print(f"[bold green]Cuenta: {cliente['cuenta']}[/bold green]")
    
    table = Table(title="Estado de Cuenta Detallado")
    table.add_column("Concepto", style="cyan")
    table.add_column("Monto", justify="right", style="yellow")
    table.add_column("Estado", style="green")
    table.add_column("Explicación", style="white")

    table.add_row(
        "Saldo en Cuenta", 
        f"${cliente['saldo']:.2f}", 
        "✓" if cliente['saldo'] > 0 else "⚠️",
        "Dinero disponible inmediatamente"
    )
    
    table.add_row(
        "Línea de Crédito", 
        f"${cliente['linea_credito']:.2f}", 
        "Límite",
        "Límite máximo de crédito (FIJO)"
    )
    
    table.add_row(
        "Crédito Usado", 
        f"${cliente['credito_usado']:.2f}", 
        "Deuda" if cliente['credito_usado'] > 0 else "✓",
        "Cuánto crédito has usado (VARIABLE)"
    )
    
    credito_disponible = cliente['linea_credito'] - cliente['credito_usado']
    table.add_row(
        "Crédito Disponible", 
        f"${credito_disponible:.2f}", 
        "✓" if credito_disponible > 0 else "❌",
        "Crédito que puedes usar aún"
    )
    
    table.add_row(
        "Cupo Tarjeta", 
        f"${cliente['tarjeta_credito']:.2f}", 
        "Disponible",
        "Para avances con tarjeta"
    )
    
    disponible_total = cliente['saldo'] + credito_disponible
    table.add_row(
        "Total Disponible", 
        f"${disponible_total:.2f}", 
        "✓", 
        "Saldo + Crédito disponible",
        style="bold"
    )

    console.print(table)

    if cliente['credito_usado'] > 0:
        console.print(f"\n[yellow]💡 Tienes ${cliente['credito_usado']:.2f} de deuda en tu línea de crédito.[/yellow]")
        console.print("[yellow]   Puedes pagarla haciendo un depósito.[/yellow]")

    avances_cliente = [a for a in avances if a["cuenta"] == cuenta and a["cuotas_pagadas"] < a["cuotas_totales"]]
    if avances_cliente:
        console.print("\n[bold yellow]Avances Pendientes:[/bold yellow]")
        for i, avance in enumerate(avances_cliente, 1):
            pendiente = avance["monto"] - avance["abonado"]
            cuotas_restantes = avance["cuotas_totales"] - avance["cuotas_pagadas"]
            console.print(f"  {i}. Capital pendiente: ${pendiente:.2f} - Cuotas restantes: {cuotas_restantes}")
            console.print(f"     Próxima cuota: ${avance['cuota_mensual']:.2f}")
    else:
        console.print("\n[green]✅ No tienes avances pendientes[/green]")

def mostrar_ejemplo_credito():
    """Función para explicar cómo funciona el crédito"""
    limpiar_terminal()
    console.print(Panel("[bold cyan]¿Cómo funciona la Línea de Crédito?[/bold cyan]"))
    
    console.print("[bold yellow]Ejemplo práctico:[/bold yellow]")
    console.print("• Tienes $10,000 en tu cuenta")
    console.print("• Tu línea de crédito es de $50,000 (FIJO)")
    console.print("• Crédito usado: $0 (inicialmente)")
    console.print("• Crédito disponible: $50,000 ($50,000 - $0)")
    console.print("• Total disponible: $60,000 ($10,000 + $50,000)")
    
    console.print("\n[bold cyan]Si transfieres $30,000:[/bold cyan]")
    console.print("• Se usan $10,000 de tu saldo (queda en $0)")
    console.print("• Se usan $20,000 de tu crédito")
    console.print("• Crédito usado: $20,000 ⬆️")
    console.print("• Crédito disponible: $30,000 ⬇️ ($50,000 - $20,000)")
    
    console.print("\n[bold green]Si depositas $15,000:[/bold green]")
    console.print("• Primero se paga la deuda: $15,000")
    console.print("• Crédito usado: $5,000 ⬇️ ($20,000 - $15,000)")
    console.print("• Crédito disponible: $45,000 ⬆️")
    console.print("• Saldo: $0 (todo se usó para pagar deuda)")
