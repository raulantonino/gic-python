from servicios.clientes_servicios import crear_cliente, listar_clientes
from modelos.clientes import ValidacionError


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
    print("Tipos: 1) Regular  2) Premium  3) Corporativo")
    tipo_op = input("Elige tipo (1/2/3): ").strip()

    if tipo_op == "2":
        tipo = "premium"
    elif tipo_op == "3":
        tipo = "corporativo"
    else:
        tipo = "regular"

    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono (solo números): ").strip()
    direccion = input("Dirección: ").strip()

    descuento = None
    razon_social = None
    rut_empresa = None

    if tipo == "premium":
        txt = input("Descuento (ej 0.10): ").strip()
        try:
            descuento = float(txt)
        except ValueError:
            print("\n❌ Validación: El descuento debe ser un número (ej: 0.10).")
            return

    if tipo == "corporativo":
        razon_social = input("Razón social: ").strip()
        rut_empresa = input("RUT empresa (texto): ").strip()

    try:
        cliente = crear_cliente(
            tipo=tipo,
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion,
            descuento=descuento,
            razon_social=razon_social,
            rut_empresa=rut_empresa,
        )
        print("\n✅ Cliente creado:")
        print(cliente)

    except ValidacionError as e:
        print(f"\n❌ Validación: {e}")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def _menu_listar_clientes() -> None:
    print("\n--- Lista de clientes ---")
    clientes = listar_clientes()

    if not clientes:
        print("No hay clientes registrados.")
        return

    for c in clientes:
        print(c)
