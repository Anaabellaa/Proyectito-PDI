import customtkinter as ctk
import random, json, os, winsound

JUEGOS_FILE = "juegos.json"
SONIDOS_DIR = "sonidos"

sonidos = {
    "Perro": "perro.wav",
    "Gato": "gato.wav",
    "Pájaro": "pajaro.wav",
    "Campana": "campana.wav"
}

def guardar_puntaje(juego, puntos):
    data = {}
    if os.path.exists(JUEGOS_FILE):
        with open(JUEGOS_FILE, "r") as f:
            data = json.load(f)
    data[juego] = data.get(juego, 0) + puntos
    with open(JUEGOS_FILE, "w") as f:
        json.dump(data, f)

def mostrar(app):
    for w in app.winfo_children():
        w.destroy()

    nombre, archivo = random.choice(list(sonidos.items()))
    ruta = os.path.join(SONIDOS_DIR, archivo)
    opciones = list(sonidos.keys())
    random.shuffle(opciones)

    ctk.CTkLabel(app, text="🔊 Escucha el sonido y elige qué es", font=("Arial Rounded MT Bold", 18)).pack(pady=20)

    def reproducir():
        if os.path.exists(ruta):
            winsound.PlaySound(ruta, winsound.SND_FILENAME)
        else:
            print(f"No se encontró el archivo: {ruta}")

    ctk.CTkButton(app, text="▶️ Reproducir sonido", command=reproducir).pack(pady=10)

    resultado = ctk.CTkLabel(app, text="", font=("Arial", 16))
    resultado.pack(pady=10)

    def verificar(opcion):
        if opcion == nombre:
            resultado.configure(text="✅ ¡Muy bien!", text_color="green")
            guardar_puntaje("sonidos", 1)
        else:
            resultado.configure(text=f"❌ Vuelve a intentar", text_color="red")

    for o in opciones:
        ctk.CTkButton(app, text=o, command=lambda o=o: verificar(o)).pack(pady=5)

    botones = ctk.CTkFrame(app)
    botones.pack(pady=20)

    ctk.CTkButton(botones, text="🔁 Reiniciar", command=lambda: mostrar(app), width=100).pack(side="left", padx=10)
    ctk.CTkButton(botones, text="⬅️ Volver", command=app.volver_menu, width=120).pack(side="left", padx=10)


