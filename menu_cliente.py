from servicios.clientes_servicios import (
    crear_cliente,
    listar_clientes,
    obtener_cliente_por_id,
    editar_cliente,
    eliminar_cliente,
)
from modelos.clientes import ValidacionError
from modelos.clientes import ClientePremium, ClienteCorporativo


def menu_principal() -> None:
    while True:
        print("\n=== Gestor Inteligente de Clientes (GIC) ===")
        print("1) Crear cliente")
        print("2) Listar clientes")
        print("3) Ver cliente por ID")
        print("4) Editar cliente")
        print("5) Eliminar cliente")
        print("0) Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            _menu_crear_cliente()
        elif opcion == "2":
            _menu_listar_clientes()
        elif opcion == "3":
            _menu_ver_cliente()
        elif opcion == "4":
            _menu_editar_cliente()
        elif opcion == "5":
            _menu_eliminar_cliente()
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


def _menu_ver_cliente() -> None:
    print("\n--- Ver cliente por ID ---")
    txt = input("ID: ").strip()
    if not txt.isdigit():
        print("❌ ID inválido.")
        return

    try:
        c = obtener_cliente_por_id(int(txt))
        print("\n✅ Cliente encontrado:")
        print(c)
    except ValidacionError as e:
        print(f"\n❌ {e}")


def _menu_editar_cliente() -> None:
    print("\n--- Editar cliente ---")
    txt = input("ID del cliente a editar: ").strip()
    if not txt.isdigit():
        print("❌ ID inválido.")
        return

    cliente_id = int(txt)

    try:
        actual = obtener_cliente_por_id(cliente_id)
        print("\nCliente actual:")
        print(actual)

        print("\nDeja en blanco para NO cambiar ese campo.")
        nombre = input("Nuevo nombre: ").strip()
        email = input("Nuevo email: ").strip()
        telefono = input("Nuevo teléfono (solo números): ").strip()
        direccion = input("Nueva dirección: ").strip()

        # Convertimos blanks a None (para no tocar)
        nombre = None if nombre == "" else nombre
        email = None if email == "" else email
        telefono = None if telefono == "" else telefono
        direccion = None if direccion == "" else direccion

        descuento = None
        razon_social = None
        rut_empresa = None

        if isinstance(actual, ClientePremium):
            txt_desc = input("Nuevo descuento (ej 0.10): ").strip()
            if txt_desc != "":
                try:
                    descuento = float(txt_desc)
                except ValueError:
                    print("\n❌ Validación: El descuento debe ser un número (ej: 0.10).")
                    return

        if isinstance(actual, ClienteCorporativo):
            rs = input("Nueva razón social: ").strip()
            re = input("Nuevo RUT empresa: ").strip()
            razon_social = None if rs == "" else rs
            rut_empresa = None if re == "" else re

        actualizado = editar_cliente(
            cliente_id=cliente_id,
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion,
            descuento=descuento,
            razon_social=razon_social,
            rut_empresa=rut_empresa,
        )

        print("\n✅ Cliente actualizado:")
        print(actualizado)

    except ValidacionError as e:
        print(f"\n❌ Validación: {e}")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


def _menu_eliminar_cliente() -> None:
    print("\n--- Eliminar cliente ---")
    txt = input("ID del cliente a eliminar: ").strip()
    if not txt.isdigit():
        print("❌ ID inválido.")
        return

    cliente_id = int(txt)

    try:
        c = obtener_cliente_por_id(cliente_id)
        print("\nCliente a eliminar:")
        print(c)

        confirm = input("¿Confirmas eliminación? (s/n): ").strip().lower()
        if confirm != "s":
            print("Cancelado.")
            return

        eliminado = eliminar_cliente(cliente_id)
        print("\n✅ Cliente eliminado:")
        print(eliminado)

    except ValidacionError as e:
        print(f"\n❌ {e}")

    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
