import customtkinter as ctk
import random, json, os, time

JUEGOS_FILE = "juegos.json"

# Usamos emojis simples (pueden reemplazarse por imágenes más adelante)
iconos = ["🍎", "🍌", "🍇", "🍓", "🍒", "🍊"]

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

    ctk.CTkLabel(app, text="🧠 Encuentra las parejas iguales", font=("Arial Rounded MT Bold", 20)).pack(pady=20)

    # Crear las cartas duplicadas y mezcladas
    cartas = iconos[:3] * 2  # 3 pares = 6 cartas
    random.shuffle(cartas)

    frame_cartas = ctk.CTkFrame(app)
    frame_cartas.pack(pady=10)

    botones = []
    seleccionadas = []
    descubiertas = set()
    resultado = ctk.CTkLabel(app, text="", font=("Arial", 16))
    resultado.pack(pady=10)

    def mostrar_icono(i):
        if i in descubiertas or len(seleccionadas) == 2:
            return

        botones[i].configure(text=cartas[i])
        seleccionadas.append(i)

        if len(seleccionadas) == 2:
            app.after(800, verificar_pareja)

    def verificar_pareja():
        i1, i2 = seleccionadas
        if cartas[i1] == cartas[i2]:
            resultado.configure(text="✅ ¡Bien hecho!", text_color="green")
            descubiertas.update(seleccionadas)
            guardar_puntaje("memoria", 1)
            if len(descubiertas) == len(cartas):
                resultado.configure(text="🎉 ¡Completaste todas las parejas!", text_color="blue")
        else:
            resultado.configure(text="❌ Intenta de nuevo", text_color="red")
            botones[i1].configure(text="❓")
            botones[i2].configure(text="❓")
        seleccionadas.clear()

    # Crear los botones de las cartas
    for i, _ in enumerate(cartas):
        b = ctk.CTkButton(
            frame_cartas, text="❓", width=80, height=60, 
            font=("Arial", 24), command=lambda i=i: mostrar_icono(i)
        )
        b.grid(row=i//3, column=i%3, padx=10, pady=10)
        botones.append(b)

    # Botones inferiores
    contenedor_botones = ctk.CTkFrame(app)
    contenedor_botones.pack(pady=20)

    ctk.CTkButton(contenedor_botones, text="🔁 Reiniciar", command=lambda: mostrar(app), width=100).pack(side="left", padx=10)
    ctk.CTkButton(contenedor_botones, text="⬅️ Volver", command=app.volver_menu, width=120).pack(side="left", padx=10)


