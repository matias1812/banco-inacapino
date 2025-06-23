import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from time import sleep
from clientes import registrar_cliente, listar_clientes, buscar_cliente
from contactos import registrar_contacto, listar_contactos
from transferencias import transferir
from avances import solicitar_avance, mostrar_avances_cliente
from pagos_avances import pagar_cuota
from movimientos import registrar_movimiento, mostrar_historial
from consultas import consultar_saldo, mostrar_ejemplo_credito
from creditos import solicitar_credito_linea, pagar_credito_linea, consultar_productos_credito
from utils import limpiar_terminal

console = Console()

def menu():
    while True:
        limpiar_terminal()
        
        banner = Text("🏦 BANCO INACAPINO 🏦", style="bold blue", justify="center")
        console.print(Panel(banner, style="blue"))

        console.print("\n[bold cyan]📋 MENÚ PRINCIPAL[/bold cyan]")
        
        console.print("\n[bold yellow]👥 GESTIÓN DE CLIENTES[/bold yellow]")
        console.print("1. Registrar cliente")
        console.print("2. Listar clientes")
        console.print("3. Buscar cliente")
        
        console.print("\n[bold yellow]📞 CONTACTOS[/bold yellow]")
        console.print("4. Registrar contacto")
        console.print("5. Listar contactos")
        
        console.print("\n[bold yellow]💰 OPERACIONES BANCARIAS[/bold yellow]")
        console.print("6. Realizar transferencia")
        console.print("7. Registrar movimiento (depósito/retiro/pago)")
        console.print("8. Mostrar historial de movimientos")
        
        console.print("\n[bold yellow]💳 PRODUCTOS DE CRÉDITO[/bold yellow]")
        console.print("9. Solicitar crédito (línea de crédito)")
        console.print("10. Pagar crédito (línea de crédito)")
        console.print("11. Solicitar avance (tarjeta de crédito)")
        console.print("12. Consultar avances")
        console.print("13. Pagar cuota de avance")
        console.print("14. Ver todos los productos de crédito")
        
        console.print("\n[bold yellow]📊 CONSULTAS[/bold yellow]")
        console.print("15. Consultar saldo y estado")
        console.print("16. ¿Cómo funciona el crédito?")
        
        console.print("\n[bold red]0. Salir[/bold red]")

        opcion = Prompt.ask("\n[bold white]Selecciona una opción[/bold white]")

        if opcion == '1':
            registrar_cliente()
        elif opcion == '2':
            listar_clientes()
        elif opcion == '3':
            buscar_cliente()
        elif opcion == '4':
            registrar_contacto()
        elif opcion == '5':
            listar_contactos()
        elif opcion == '6':
            transferir()
        elif opcion == '7':
            registrar_movimiento()
        elif opcion == '8':
            mostrar_historial()
        elif opcion == '9':
            solicitar_credito_linea()
        elif opcion == '10':
            pagar_credito_linea()
        elif opcion == '11':
            solicitar_avance()
        elif opcion == '12':
            mostrar_avances_cliente()
        elif opcion == '13':
            pagar_cuota()
        elif opcion == '14':
            consultar_productos_credito()
        elif opcion == '15':
            consultar_saldo()
        elif opcion == '16':
            mostrar_ejemplo_credito()
        elif opcion == '0':
            console.print("\n[bold green]¡Gracias por usar el Banco INACAPINO![/bold green]")
            console.print("[green]Que tengas un excelente día 😊[/green]")
            sleep(2)
            break
        else:
            console.print("[red]❌ Opción inválida. Intenta nuevamente.[/red]")

        input("\n[bold green]Presiona Enter para continuar...[/bold green]")

if __name__ == "__main__":
    menu()
