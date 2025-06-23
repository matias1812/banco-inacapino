from data import contactos, clientes

def registrar_contacto():
    cuenta = input("Número de cuenta del contacto: ")
    contacto = next((c for c in clientes if c["cuenta"] == cuenta), None)
    if not contacto:
        print("Cuenta no encontrada.")
        return

    nuevo_contacto = {
        "nombre": contacto["nombre"],
        "apellido": contacto["apellido"],
        "cuenta": contacto["cuenta"]
    }

    contactos.append(nuevo_contacto)
    print("Contacto registrado correctamente.")

def listar_contactos():
    for c in contactos:
        print(c)
