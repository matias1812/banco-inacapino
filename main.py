from clientes import registrar_cliente, listar_clientes
from contactos import registrar_contacto, listar_contactos
from transferencias import transferir
from avances import solicitar_avance
from pagos_avances import pagar_cuota
from utils import limpiar_terminal
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def menu():
    while True:
        limpiar_terminal()
        console.print(Panel("[bold green]Bienvenido al Banco INACAPINO[/bold green]", expand=False))

        console.print("[bold cyan]Menú Principal[/bold cyan]", style="bold")
        console.print("1. Registrar cliente")
        console.print("2. Listar clientes")
        console.print("3. Registrar contacto")
        console.print("4. Listar contactos")
        console.print("5. Realizar transferencia")
        console.print("6. Solicitar avance con tarjeta")
        console.print("7. Pagar cuota de avance")
        console.print("0. Salir")

        opcion = Prompt.ask("Selecciona una opción")

        if opcion == '1':
            registrar_cliente()
        elif opcion == '2':
            listar_clientes()
        elif opcion == '3':
            registrar_contacto()
        elif opcion == '4':
            listar_contactos()
        elif opcion == '5':
            transferir()
        elif opcion == '6':
            solicitar_avance()
        elif opcion == '7':
            pagar_cuota()
        elif opcion == '0':
            console.print("[bold green]Gracias por usar el Banco INACAPINO. ¡Hasta pronto![/bold green]")
            break
        else:
            console.print("[red]Opción inválida. Intenta nuevamente.[/red]")

        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    menu()  