# 🤖 Chatbot de Soporte Técnico Nivel 1

## 📌 Descripción

Este proyecto fue desarrollado como Trabajo Práctico Integrador para la materia Organización Empresarial de la Tecnicatura Universitaria en Programación (UTN).

El sistema consiste en un chatbot de soporte técnico de Nivel 1 capaz de asistir a los usuarios en la resolución de incidencias frecuentes mediante respuestas automáticas obtenidas desde una base de datos simulada implementada con archivos CSV.

Cuando el inconveniente no puede resolverse automáticamente, el chatbot registra un ticket y deriva el caso al área de soporte técnico.

Además del funcionamiento en consola, el sistema fue integrado con Telegram utilizando la API oficial de Telegram Bots, permitiendo interactuar desde cualquier dispositivo.

---

# 🎯 Objetivos

- Automatizar el proceso de soporte técnico de Nivel 1.
- Reducir los tiempos de respuesta.
- Registrar incidencias automáticamente.
- Simular un proceso empresarial mediante un chatbot.
- Aplicar conceptos de BPMN 2.0, procesos y automatización.

---

# 🛠 Tecnologías utilizadas

- Python 3.14
- Telegram Bot API
- python-telegram-bot
- Archivos CSV
- Visual Studio Code
- Git y GitHub

---

# 📂 Estructura del proyecto

```
TPI_OE
│
├── bot_telegram.py
├── main.py
├── respuestas.csv
├── tickets.csv
├── README.md
├── Informe_TPI_Organizacion_Empresarial.pdf
```

---

# ⚙ Funcionalidades

✔ Inicio de conversación.

✔ Validación del nombre del usuario.

✔ Consulta de categorías.

✔ Lectura de respuestas desde respuestas.csv.

✔ Resolución automática de incidencias.

✔ Confirmación de resolución.

✔ Registro automático de tickets.

✔ Derivación al soporte técnico.

✔ Persistencia de la información mediante archivos CSV.

✔ Funcionamiento mediante Telegram.

---

# 💾 Persistencia

El chatbot utiliza dos archivos CSV como base de datos simulada.

### respuestas.csv

Contiene:

- ID
- Categoría
- Problema
- Solución
- Derivar

### tickets.csv

Contiene:

- Número de ticket
- Usuario
- Categoría
- Problema
- Estado

Cada vez que un problema no puede resolverse automáticamente, el chatbot registra un nuevo ticket.

---

# 🔄 Flujo del proceso

Inicio

↓

Ingreso del nombre

↓

Selección de categoría

↓

Consulta de respuestas.csv

↓

¿Existe solución?

├── Sí

│ ↓

│ Mostrar solución

│ ↓

│ ¿Problema resuelto?

│ ├── Sí → Fin

│ └── No → Registrar Ticket

│

└── No

↓

Registrar Ticket

↓

Fin

---

## ▶ Ejecución del proyecto

El proyecto puede ejecutarse de dos maneras:

### Opción 1: Ejecución local (Consola)

Permite probar el funcionamiento del chatbot directamente desde la terminal.

```bash
python main.py
```

### Opción 2: Ejecución mediante Telegram

Permite interactuar con el chatbot desde Telegram utilizando la API oficial de Telegram Bots.

```bash
python bot_telegram.py
```

> **Importante:** Para utilizar la versión de Telegram es necesario crear un bot mediante BotFather y configurar el TOKEN correspondiente en el archivo `bot_telegram.py`.
```

---

# 📱 Integración con Telegram

El chatbot fue integrado mediante la librería oficial **python-telegram-bot**, permitiendo interactuar desde Telegram utilizando una máquina de estados para controlar el flujo conversacional.

---

# 📊 Modelo de datos

El proyecto utiliza una base de datos simulada mediante archivos CSV.

- respuestas.csv → consulta de soluciones.
- tickets.csv → almacenamiento de incidencias.

---

# 📖 Conceptos aplicados

- Procesos empresariales
- BPMN 2.0
- Automatización
- Chatbots
- Persistencia
- Máquina de Estados
- Gestión de incidencias
- Validaciones
- Integración con Telegram

---

# 👨‍💻 Autor

Facundo Gómez
Ricardo Oliva  

Tecnicatura Universitaria en Programación

Universidad Tecnológica Nacional