from servicios.clientes_servicios import crear_cliente, listar_clientes


def menu_principal() -> None:
    while True:
        print("\n=== Gestor Inteligente de Clientes (GIC) ===")
        print("1) Crear cliente")
        print("2) Listar clientes")
        print("0) Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            _menu_crear_cliente()
        elif opcion == "2":
            _menu_listar_clientes()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")


def _menu_crear_cliente() -> None:
    print("\n--- Crear cliente ---")
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()
    direccion = input("Dirección: ").strip()

    cliente = crear_cliente(nombre, email, telefono, direccion)
    print("\n✅ Cliente creado:")
    print(cliente)


def _menu_listar_clientes() -> None:
    print("\n--- Lista de clientes ---")
    clientes = listar_clientes()

    if not clientes:
        print("No hay clientes registrados.")
        return

    for c in clientes:
        print(c)