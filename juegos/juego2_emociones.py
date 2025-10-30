import customtkinter as ctk
import random, json, os

JUEGOS_FILE = "juegos.json"

# Emociones básicas con sus emojis representativos
emociones = [
    ("🙂", "Feliz"),
    ("😢", "Triste"),
    ("😡", "Enojado"),
    ("😲", "Sorprendido"),
    ("😴", "Cansado"),
    ("😱", "Asustado")
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
    # Limpia ventana
    for w in app.winfo_children():
        w.destroy()

    # Título del juego
    ctk.CTkLabel(app, text="😊 Identifica la emoción correcta", font=("Arial Rounded MT Bold", 22)).pack(pady=20)

    # Selecciona una emoción al azar
    emoji, nombre_correcto = random.choice(emociones)
    opciones = random.sample([n for _, n in emociones], 4)  # 4 opciones
    if nombre_correcto not in opciones:
        opciones[random.randint(0, 3)] = nombre_correcto
    random.shuffle(opciones)

    # Emoji grande en pantalla
    ctk.CTkLabel(app, text=emoji, font=("Arial", 100)).pack(pady=10)

    # Mensaje de resultado
    resultado = ctk.CTkLabel(app, text="", font=("Arial", 18))
    resultado.pack(pady=15)

    # Verifica la respuesta seleccionada
    def verificar(respuesta):
        if respuesta == nombre_correcto:
            resultado.configure(text="✅ ¡Muy bien!", text_color="green")
            guardar_puntaje("emociones", 1)
        else:
            resultado.configure(text=f"❌ Vuelve a intentar", text_color="red")

    # Muestra botones con opciones
    for op in opciones:
        ctk.CTkButton(app, text=op, command=lambda op=op: verificar(op), width=200, height=40).pack(pady=5)

    # Botones inferiores
    botones = ctk.CTkFrame(app)
    botones.pack(pady=20)

    ctk.CTkButton(botones, text="🔁 Reiniciar", command=lambda: mostrar(app), width=120).pack(side="left", padx=10)
    ctk.CTkButton(botones, text="⬅️ Volver", command=app.volver_menu, width=120).pack(side="left", padx=10)

