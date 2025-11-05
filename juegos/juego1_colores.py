import customtkinter as ctk
import random, json, os

JUEGOS_FILE = "juegos.json"

colores = [
    ("Rojo", "#FF4C4C"),
    ("Verde", "#4CFF4C"),
    ("Azul", "#4C4CFF"),
    ("Amarillo", "#FFFF4C"),
    ("Rosa", "#FF99FF"),
    ("Naranja", "#FFA64C"),
]

def guardar_puntaje(juego, puntos):
    data = {}
    if os.path.exists(JUEGOS_FILE):
        with open(JUEGOS_FILE, "r") as f:
            data = json.load(f)
    data[juego] = data.get(juego, 0) + puntos
    with open(JUEGOS_FILE, "w") as f:
        json.dump(data, f)

def mostrar(app):
    # Limpia la pantalla
    for w in app.winfo_children():
        w.destroy()

    # Título
    ctk.CTkLabel(app, text="🎨 Adivina el color correcto", font=("Arial Rounded MT Bold", 22)).pack(pady=20)

    # Selección de color aleatorio
    nombre_color, codigo_color = random.choice(colores)

    # Cuadro colorido central
    cuadro_color = ctk.CTkFrame(app, width=200, height=200, fg_color=codigo_color)
    cuadro_color.pack(pady=20)

    # Opciones de respuesta
    opciones = random.sample([n for n, _ in colores], 4)
    if nombre_color not in opciones:
        opciones[random.randint(0, 3)] = nombre_color
    random.shuffle(opciones)

    # Etiqueta de resultado
    resultado = ctk.CTkLabel(app, text="", font=("Arial", 18))
    resultado.pack(pady=15)

    # Verificar respuesta
    def verificar(opcion):
        if opcion == nombre_color:
            resultado.configure(text="✅ ¡Muy bien!", text_color="green")
            guardar_puntaje("colores", 1)
        else:
            resultado.configure(text=f"❌ Vuelve a intentar", text_color="red")

    # Botones de opciones
    for op in opciones:
        ctk.CTkButton(app, text=op, command=lambda op=op: verificar(op), width=200, height=40).pack(pady=5)

    # Botones inferiores
    botones = ctk.CTkFrame(app)
    botones.pack(pady=20)

    ctk.CTkButton(botones, text="🔁 Reiniciar", command=lambda: mostrar(app), width=120).pack(side="left", padx=10)
    ctk.CTkButton(botones, text="⬅️ Volver", command=app.volver_menu, width=120).pack(side="left", padx=10)

