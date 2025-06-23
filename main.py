from clientes import registrar_cliente, listar_clientes
from contactos import registrar_contacto, listar_contactos
from transferencias import transferir
from avances import solicitar_avance
from pagos_avances import pagar_cuota

def menu():
    while True:
        print("\n=== Banco INACAPINO ===")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Registrar contacto")
        print("4. Listar contactos")
        print("5. Realizar transferencia")
        print("6. Solicitar avance con tarjeta")
        print("7. Pagar cuota de avance")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

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
            print("Gracias por usar el Banco INACAPINO.")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    menu()
