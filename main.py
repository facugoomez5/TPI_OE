import csv
import os

ARCHIVO_RESPUESTAS = "respuestas.csv"
ARCHIVO_TICKETS = "tickets.csv"


def cargar_respuestas():
    respuestas = []

    with open(ARCHIVO_RESPUESTAS, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            respuestas.append(fila)

    return respuestas


def mostrar_categorias(respuestas):
    print("\nCategorías disponibles:")

    categorias = []

    for respuesta in respuestas:
        categoria = respuesta["categoria"]

        if categoria not in categorias:
            categorias.append(categoria)

    for i, categoria in enumerate(categorias, start=1):
        print(f"{i}. {categoria}")

    return categorias


def validar_nombre(nombre):
    return nombre.strip() != "" and not nombre.isdigit()


def buscar_respuesta(respuestas, categoria):
    for respuesta in respuestas:
        if respuesta["categoria"].lower() == categoria.lower():
            return respuesta

    return None


def obtener_ultimo_ticket():
    if not os.path.exists(ARCHIVO_TICKETS):
        return 1000

    with open(ARCHIVO_TICKETS, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        tickets = list(lector)

        if len(tickets) == 0:
            return 1000

        return int(tickets[-1]["ticket"])


def generar_ticket(usuario, categoria, problema):
    nuevo_ticket = obtener_ultimo_ticket() + 1

    existe_archivo = os.path.exists(ARCHIVO_TICKETS)

    with open(ARCHIVO_TICKETS, "a", encoding="utf-8", newline="") as archivo:
        campos = ["ticket", "usuario", "categoria", "problema", "estado"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)

        if not existe_archivo or os.path.getsize(ARCHIVO_TICKETS) == 0:
            escritor.writeheader()

        escritor.writerow({
            "ticket": nuevo_ticket,
            "usuario": usuario,
            "categoria": categoria,
            "problema": problema,
            "estado": "Abierto"
        })

    return nuevo_ticket


def ejecutar_chatbot():
    respuestas = cargar_respuestas()

    print("===================================")
    print(" CHATBOT DE SOPORTE TÉCNICO NIVEL 1")
    print("===================================")

    nombre = input("\nIngrese su nombre: ").strip()

    while not validar_nombre(nombre):
        print("Nombre inválido. No puede estar vacío ni ser solo números.")
        nombre = input("Ingrese su nombre: ").strip()

    print(f"\nHola {nombre}, bienvenido al soporte técnico.")

    categorias = mostrar_categorias(respuestas)

    opcion = input("\nSeleccione una categoría por número: ").strip()

    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(categorias):
        print("Opción inválida. Intente nuevamente.")
        opcion = input("Seleccione una categoría por número: ").strip()

    categoria_elegida = categorias[int(opcion) - 1]

    respuesta = buscar_respuesta(respuestas, categoria_elegida)

    if respuesta is not None:
        print("\nProblema registrado:")
        print(respuesta["problema"])

        print("\nSolución sugerida:")
        print(respuesta["solucion"])

        if respuesta["derivar"].lower() == "sí":
            ticket = generar_ticket(nombre, categoria_elegida, respuesta["problema"])

            print("\nEste caso requiere derivación.")
            print(f"Se generó el ticket N° {ticket}.")
            print("Un técnico especializado revisará el caso.")

        else:
            confirmacion = input("\n¿El problema fue solucionado? (S/N): ").strip().upper()

            while confirmacion not in ["S", "N"]:
                print("Respuesta inválida. Ingrese S o N.")
                confirmacion = input("¿El problema fue solucionado? (S/N): ").strip().upper()

            if confirmacion == "S":
                print("\nCaso cerrado correctamente.")
            else:
                ticket = generar_ticket(nombre, categoria_elegida, respuesta["problema"])

                print("\nEl problema no fue resuelto.")
                print(f"Se generó el ticket N° {ticket}.")
                print("El caso fue derivado al soporte técnico.")

    print("\nGracias por utilizar el chatbot.")


ejecutar_chatbot()