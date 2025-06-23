clientes = []
contactos = []
avances = []

def inicializar_contactos_integrantes():
    """Registra automáticamente a los integrantes del grupo como contactos"""
    integrantes = [
        {"nombre": "Juan", "apellido": "Pérez", "cuenta": "12345678"},
        {"nombre": "María", "apellido": "González", "cuenta": "87654321"}
    ]
    
    for integrante in integrantes:
        if not any(c["cuenta"] == integrante["cuenta"] for c in contactos):
            contactos.append(integrante)

inicializar_contactos_integrantes()
