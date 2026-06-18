import csv
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

ARCHIVO_RESPUESTAS = "respuestas.csv"
ARCHIVO_TICKETS = "tickets.csv"

ESPERANDO_NOMBRE, ESPERANDO_CATEGORIA, ESPERANDO_CONFIRMACION = range(3)


def cargar_respuestas():
    with open(ARCHIVO_RESPUESTAS, "r", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def validar_nombre(nombre):
    return nombre.strip() != "" and not nombre.isdigit()


def obtener_categorias():
    respuestas = cargar_respuestas()
    categorias = []

    for respuesta in respuestas:
        if respuesta["categoria"] not in categorias:
            categorias.append(respuesta["categoria"])

    return categorias


def buscar_respuesta(categoria):
    respuestas = cargar_respuestas()

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenido al Chatbot de Soporte Técnico Nivel 1.\n\nIngrese su nombre:"
    )
    return ESPERANDO_NOMBRE


async def recibir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.text.strip()

    if not validar_nombre(nombre):
        await update.message.reply_text(
            "Nombre inválido. No puede estar vacío ni ser solo números.\nIngrese su nombre nuevamente:"
        )
        return ESPERANDO_NOMBRE

    context.user_data["nombre"] = nombre

    categorias = obtener_categorias()

    teclado = [[categoria] for categoria in categorias]

    texto_categorias = "Categorías disponibles:\n\n"

    for i, categoria in enumerate(categorias, start=1):
        texto_categorias += f"{i}. {categoria}\n"

    await update.message.reply_text(
        f"Hola {nombre}.\n\n{texto_categorias}\nSeleccione una categoría tocando un botón o escribiendo el nombre:",
        reply_markup=ReplyKeyboardMarkup(
            teclado,
            one_time_keyboard=False,
            resize_keyboard=True,
            input_field_placeholder="Seleccione una categoría"
            )
)

    return ESPERANDO_CATEGORIA


async def recibir_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categoria = update.message.text.strip()
    categorias = obtener_categorias()

    if categoria not in categorias:
        await update.message.reply_text(
            "Categoría inválida. Seleccione una opción del menú."
        )
        return ESPERANDO_CATEGORIA

    respuesta = buscar_respuesta(categoria)

    context.user_data["categoria"] = categoria
    context.user_data["problema"] = respuesta["problema"]

    mensaje = (
        f"Problema registrado: {respuesta['problema']}\n\n"
        f"Solución sugerida: {respuesta['solucion']}"
    )

    if respuesta["derivar"].lower() == "sí":
        ticket = generar_ticket(
            context.user_data["nombre"],
            categoria,
            respuesta["problema"]
        )

        await update.message.reply_text(
            mensaje +
            f"\n\nEste caso requiere derivación.\nSe generó el ticket N° {ticket}.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    teclado = [["S", "N"]]

    await update.message.reply_text(
        mensaje + "\n\n¿El problema fue solucionado? Responda S o N.",
        reply_markup=ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
    )

    return ESPERANDO_CONFIRMACION


async def recibir_confirmacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    confirmacion = update.message.text.strip().upper()

    if confirmacion not in ["S", "N"]:
        await update.message.reply_text("Respuesta inválida. Ingrese S o N.")
        return ESPERANDO_CONFIRMACION

    if confirmacion == "S":
        await update.message.reply_text(
            "Caso cerrado correctamente.\nGracias por utilizar el chatbot.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    ticket = generar_ticket(
        context.user_data["nombre"],
        context.user_data["categoria"],
        context.user_data["problema"]
    )

    await update.message.reply_text(
        f"El problema no fue resuelto.\nSe generó el ticket N° {ticket}.\nEl caso fue derivado al soporte técnico.",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Proceso cancelado.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main():
    TOKEN = "COLOCAR_AQUI_EL_TOKEN_DE_BOTFATHER"

    app = ApplicationBuilder().token(TOKEN).build()

    conversacion = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ESPERANDO_NOMBRE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nombre)
            ],
            ESPERANDO_CATEGORIA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_categoria)
            ],
            ESPERANDO_CONFIRMACION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_confirmacion)
            ],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)]
    )

    app.add_handler(conversacion)

    print("Bot funcionando...")
    app.run_polling()


main()