import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, colorchooser
from PIL import Image, ImageTk
import json, os, sys, random, winsound
from juegos import juego1_colores, juego2_emociones, juego3_memoria, juego4_sonidos
import customtkinter as ctk

def resource_path(relative_path):
    """Devuelve la ruta correcta del recurso, tanto en .exe como en modo desarrollo."""
    try:
        base_path = sys._MEIPASS  # Ruta temporal creada por PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # En modo desarrollo
    return os.path.join(base_path, relative_path)

# ---------- CONFIGURACIÓN GUARDADA ----------
CONFIG_FILE = "config.json"

def cargar_configuracion():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "color_fondo": "#e6f2ff",
        "tam_fuente": 15,
        "modo_oscuro": False,
        "sonido": True,
        "puntos": 0
    }

def guardar_configuracion(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# ---------- FUNCIONES JSON GENERALES ----------
def cargar_json(nombre, defecto):
    if os.path.exists(nombre):
        with open(nombre, "r") as f:
            return json.load(f)
    return defecto

def guardar_json(nombre, datos):
    with open(nombre, "w") as f:
        json.dump(datos, f, indent=4)

config = cargar_configuracion()
MENSAJES_FILE = "mensajes.json"
mensajes = cargar_json(MENSAJES_FILE, [])

# ---------- FUNCIONES GENERALES ----------
def reproducir_sonido():
    if config.get("sonido", True):
        winsound.MessageBeep()

def mostrar_alerta(mensaje, duracion=4000):
    lbl_alertas.config(text=f"🔔 {mensaje}")
    lbl_alertas.after(duracion, lambda: lbl_alertas.config(text=""))

# ---------- INTERFAZ PRINCIPAL ----------
ventana = tk.Tk()
ventana.title("TEA-yudamos")
ventana.geometry("1080x920")
ventana.resizable(False, False)

contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True)

frames = {}

# ---------- CAMBIO DE FRAMES ----------
def mostrar_frame(nombre):
    for f in frames.values():
        f.pack_forget()
    frames[nombre].pack(fill="both", expand=True)
    reproducir_sonido()

# ---------- FUNCIONES GENERALES ----------
def mostrar_frame(nombre):
    for frame in frames.values():
        frame.pack_forget()
    frames[nombre].pack(fill="both", expand=True)


def mostrar_pictogramas():
    mostrar_frame("pictogramas")

# ---------- ENCABEZADO GLOBAL ----------
frame_superior = tk.Frame(ventana, bg="#ffffff")
frame_superior.place(relx=0, rely=0, relwidth=1, height=20)

lbl_alertas = tk.Label(frame_superior, text="", bg="#ffffff", font=("Comic Sans MS", 10, "bold"))
lbl_alertas.pack(side="right", padx=10)

# ---------- FRAME INICIO ----------
frame_inicio = tk.Frame(contenedor, bg=config["color_fondo"])
frames["inicio"] = frame_inicio

titulo = tk.Label(frame_inicio, text="TEA-yudamos", font=("Comic Sans MS", 28, "bold"), bg=config["color_fondo"])
titulo.pack(pady=30)

botones = [
    ("🗓 Agenda Visual", lambda: mostrar_frame("agenda"), "#92baee"),
    ("🖼 Pictogramas", lambda: mostrar_frame("pictogramas"), "#eabee7"),
    ("🎮 Juegos", lambda: mostrar_frame("juegos"), "#eef4a8"),
    ("🤝 Familias y Profesionales", lambda: mostrar_frame("conexion"), "#b698ec"),
    ("⚙ Configuración", lambda: mostrar_frame("config"), "#f0aeae")
]

for texto, comando, color in botones:
    ctk.CTkButton(
        frame_inicio, text=texto, command=comando,
        width=260, height=70, corner_radius=15,
        fg_color=color, hover_color="#cccccc",
        text_color="black", font=("Comic Sans MS", config["tam_fuente"], "bold")
    ).pack(pady=10)

# ---------- FRAME AGENDA ----------
frame_agenda = tk.Frame(contenedor, bg="#92baee")
frames["agenda"] = frame_agenda

tk.Label(frame_agenda, text="Agenda Visual", font=("Comic Sans MS", 20, "bold"), bg="#92baee").pack(pady=60)

tareas = cargar_json("tareas.json", [])

lista_agenda = tk.Listbox(frame_agenda, font=("Comic Sans MS", 12), width=40, height=10)
lista_agenda.pack(pady=5)
for t in tareas:
    lista_agenda.insert("end", t)

entry_tarea = tk.Entry(frame_agenda, font=("Comic Sans MS", 12))
entry_tarea.pack(pady=5)

def agregar_tarea():
    tarea = entry_tarea.get().strip()
    if tarea:
        lista_agenda.insert("end", tarea)
        tareas.append(tarea)
        guardar_json("tareas.json", tareas)
        entry_tarea.delete(0, "end")

def eliminar_tarea():
    sel = lista_agenda.curselection()
    if sel:
        tareas.pop(sel[0])
        lista_agenda.delete(sel[0])
        guardar_json("tareas.json", tareas)

tk.Button(frame_agenda, text="Agregar", bg="#ffffff", command=agregar_tarea).pack(pady=2)
tk.Button(frame_agenda, text="Eliminar", bg="#ffffff", command=eliminar_tarea).pack(pady=2)
tk.Button(frame_agenda, text="⬅ Volver  al inicio", bg="#ffffff", command=lambda: mostrar_frame("inicio")).pack(pady=10)
mostrar_alerta("Agenda Visual lista para usar")

# ---------- FRAME JUEGOS ----------
frame_juegos = tk.Frame(contenedor, bg="#eef4a8")
frames["juegos"] = frame_juegos

ctk.CTkLabel(frame_juegos, text="🎯 Juegos Educativos", font=("Comic Sans MS", 24, "bold")).pack(pady=20)

def mostrar_menu_juegos():
    # Limpia el frame de juegos
    for widget in frame_juegos.winfo_children():
        widget.destroy()

    # Título
    ctk.CTkLabel(frame_juegos, text="🎯 Juegos Educativos", font=("Comic Sans MS", 24, "bold")).pack(pady=20)

    # Botones de juegos
    botones = [
        ("🎨 Colores", lambda: abrir_juego(juego1_colores)),
        ("😊 Emociones", lambda: abrir_juego(juego2_emociones)),
        ("🧠 Memoria", lambda: abrir_juego(juego3_memoria)),
        ("🔊 Sonidos", lambda: abrir_juego(juego4_sonidos)),
    ]

    for texto, comando in botones:
        ctk.CTkButton(
            frame_juegos, text=texto, command=comando,
            width=220, height=60,
            fg_color="#fff8c2", text_color="black",
            font=("Comic Sans MS", 16, "bold")
        ).pack(pady=10)

    tk.Button(frame_juegos, text="⬅ Volver al Inicio", bg="#ffffff",
              command=lambda: mostrar_frame("inicio")).pack(pady=30)

def abrir_juego(modulo):
    # Limpia el frame de juegos
    for widget in frame_juegos.winfo_children():
        widget.destroy()

    # Crea un contenedor donde se mostrará el juego
    contenedor_juego = ctk.CTkFrame(frame_juegos, fg_color="#ffffff")
    contenedor_juego.pack(fill="both", expand=True, pady=20, padx=20)

    # --- función para volver al menú de juegos ---
    def volver_al_menu_juegos():
        mostrar_menu_juegos()

    # Agregamos la referencia dentro del contenedor, para que el juego pueda acceder
    contenedor_juego.volver_menu = volver_al_menu_juegos

    # Carga el juego dentro del contenedor
    modulo.mostrar(contenedor_juego)

    # Agrega el botón de volver
    ctk.CTkButton(
        frame_juegos,
        text="⬅ Volver al menú de juegos",
        command=volver_al_menu_juegos,
        fg_color="#fff8c2",
        text_color="black",
        font=("Comic Sans MS", 14, "bold"),
        height=45,
        width=250
    ).pack(pady=15)



# Botones de juegos
botones = [
    ("🎨 Colores", lambda: abrir_juego(juego1_colores)),
    ("😊 Emociones", lambda: abrir_juego(juego2_emociones)),
    ("🧠 Memoria", lambda: abrir_juego(juego3_memoria)),
    ("🔊 Sonidos", lambda: abrir_juego(juego4_sonidos)),
]

for texto, comando in botones:
    ctk.CTkButton(frame_juegos, text=texto, command=comando, width=220, height=60,
                  fg_color="#fff8c2", text_color="black",
                  font=("Comic Sans MS", 16, "bold")).pack(pady=10)

# Botón volver
tk.Button(frame_juegos, text="⬅ Volver al Inicio", bg="#ffffff",
          command=lambda: mostrar_frame("inicio")).pack(pady=30)


# ---------- FRAME CONEXIÓN ----------
frame_conexion = tk.Frame(contenedor, bg="#b698ec")
frames["conexion"] = frame_conexion

tk.Label(frame_conexion, text="Familias y Profesionales 🤝", font=("Comic Sans MS", 20, "bold"), bg="#b698ec").pack(pady=20)
tk.Label(frame_conexion, text="Espacio de comunicación, información y apoyo mutuo.", font=("Comic Sans MS", 13), bg="#b698ec").pack(pady=5)

tab_view = ctk.CTkTabview(frame_conexion, width=700, height=450, fg_color="#857ec1", segmented_button_fg_color="#c78ca7")
tab_view.pack(pady=10, padx=10)

tab_view.add("Información TEA")
tab_view.add("Consejos de Apoyo")
tab_view.add("Mensajes")
tab_view.set("Información TEA") # Pestaña inicial

# --- PESTAÑA INFORMACIÓN TEA ---
info_tea_frame = tab_view.tab("Información TEA")
info_tea_frame.configure(fg_color="#e0d8f0")

tk.Label(info_tea_frame, text="¿Qué es el Trastorno del Espectro Autista (TEA)?", font=("Comic Sans MS", 14, "bold"), bg="#e0d8f0").pack(pady=10)
tk.Label(info_tea_frame, text="Es una condición del neurodesarrollo que acompaña a la persona a lo largo de toda su vida. Se caracteriza por dificultades en dos áreas principales:", justify="left", wraplength=650, bg="#e0d8f0").pack(padx=10)

tk.Label(info_tea_frame, text="  • Comunicación e interacción social: Dificultad para entender señales sociales, contacto visual, o mantener conversaciones.", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15)
tk.Label(info_tea_frame, text="  • Patrones de comportamiento o intereses restringidos y repetitivos: Resistencia a cambios de rutina, intereses muy intensos o movimientos repetitivos (estereotipias).", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15)

tk.Label(info_tea_frame, text="\nCondiciones Concomitantes (Comorbilidades):", font=("Comic Sans MS", 14, "bold"), bg="#e0d8f0").pack()
tk.Label(info_tea_frame, text="El TEA a menudo coexiste con otras condiciones, lo cual es fundamental para el apoyo:", justify="left", wraplength=650, bg="#e0d8f0").pack(padx=10)
tk.Label(info_tea_frame, text="  • Trastornos de Ansiedad y Depresión: Son frecuentes, afectando hasta a un 50% de los casos.", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15)
tk.Label(info_tea_frame, text="  • Trastorno por Déficit de Atención con Hiperactividad (TDAH).", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15)
tk.Label(info_tea_frame, text="  • Problemas de Alimentación: Pueden surgir debido a la exacerbada sensibilidad gustativa.", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15)

tk.Label(info_tea_frame, text="Recuerda: El TEA se manifiesta de forma diferente en cada persona, de leves a graves, lo que subraya la importancia de la neurodiversidad.", justify="left", wraplength=650, font=("Comic Sans MS", 10, "italic"), bg="#e0d8f0").pack(pady=10, padx=10)

# --- PESTAÑA CONSEJOS DE APOYO ---
consejos_frame = tab_view.tab("Consejos de Apoyo")
consejos_frame.configure(fg_color="#e0d8f0")

tk.Label(consejos_frame, text="Estrategias Prácticas de Apoyo", font=("Comic Sans MS", 14, "bold"), bg="#e0d8f0").pack(pady=10)
tk.Label(consejos_frame, text="La Comprensión y la anticipación son claves en el apoyo a personas con TEA.", justify="left", wraplength=650, bg="#e0d8f0").pack(padx=10)

tk.Label(consejos_frame, text="  • Rutinas y Horarios Visuales: Crea rutinas claras y usa pictogramas o listados escritos para ayudar a estructurar el día y anticipar actividades. Esto reduce la ansiedad.", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15, pady=2)
tk.Label(consejos_frame, text="  • Comunicación Clara: Usa frases cortas, sencillas y directas. Explica con detalle si hay cambios de rutina, dándole tiempo para procesar.", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15, pady=2)
tk.Label(consejos_frame, text="  • Entorno Estructurado: Mantén un ambiente ordenado y crea una 'zona de la calma' o rincón tranquilo para el descanso o la autorregulación.", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15, pady=2)
tk.Label(consejos_frame, text="  • Fomentar la Inclusión: Promover la integración en la escuela y actividades extraescolares es vital para el bienestar de la persona. La familia es el principal apoyo.", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15, pady=2)
tk.Label(consejos_frame, text="  • Busca Apoyo para la Familia: No estás solo. Conéctate con otros padres y profesionales para compartir vivencias, aprender y obtener respiro.", justify="left", wraplength=650, bg="#e0d8f0").pack(anchor="w", padx=15, pady=2)

# --- PESTAÑA MENSAJES (COMUNICACIÓN) ---
mensajes_frame = tab_view.tab("Mensajes")
mensajes_frame.configure(fg_color="#e0d8f0")

lista_msgs = tk.Listbox(mensajes_frame, font=("Comic Sans MS", 12), width=60, height=12)
lista_msgs.pack(pady=10)

frame_msg = tk.Frame(mensajes_frame, bg="#e0d8f0")
frame_msg.pack(pady=10)
entry_nombre = tk.Entry(frame_msg, font=("Comic Sans MS", 12), width=15)
entry_texto = tk.Entry(frame_msg, font=("Comic Sans MS", 12), width=30)
entry_nombre.grid(row=0, column=0, padx=5)
entry_texto.grid(row=0, column=1, padx=5)

def publicar():
    n, t = entry_nombre.get().strip(), entry_texto.get().strip()
    if n and t:
        mensajes.append({"nombre": n, "texto": t})
        guardar_json(MENSAJES_FILE, mensajes)
        entry_texto.delete(0, "end")
        actualizar_lista()
    else:
        messagebox.showwarning("Atención", "Escribe nombre y mensaje.")

def actualizar_lista():
    lista_msgs.delete(0, "end")
    datos = cargar_json(MENSAJES_FILE, [])
    for m in datos:
        lista_msgs.insert("end", f"{m['nombre']}: {m['texto']}")
    if frame_conexion.winfo_ismapped():
        frame_conexion.after(3000, actualizar_lista)

tk.Button(frame_msg, text="Publicar", bg="#ffffff", command=publicar).grid(row=0, column=2, padx=5)
# Llama a actualizar_lista una vez al inicio del frame
actualizar_lista() 

def actualizar_lista():
    lista_msgs.delete(0, "end")
    datos = cargar_json(MENSAJES_FILE, [])
    for m in datos:
        lista_msgs.insert("end", f"{m['nombre']}: {m['texto']}")
    frame_conexion.after(3000, actualizar_lista)

tk.Button(frame_msg, text="Publicar", bg="#ffffff", command=publicar).grid(row=0, column=2, padx=5)
tk.Button(frame_conexion, text="⬅ Volver al inicio", command=lambda: mostrar_frame("inicio"), bg="#ffffff").pack(pady=60)
actualizar_lista()

# ---------- FRAME CONFIGURACIÓN ----------
frame_config = tk.Frame(contenedor, bg="#f0aeae")
frames["config"] = frame_config

tk.Label(frame_config, text="Configuración ⚙", font=("Comic Sans MS", 20, "bold"), bg="#f0aeae").pack(pady=60)

def cambiar_color():
    color = colorchooser.askcolor(title="Elegir color de fondo")[1]
    if color:
        config["color_fondo"] = color
        guardar_configuracion(config)
        aplicar_estilos()

tk.Button(frame_config, text="Cambiar color de fondo", command=cambiar_color, bg="#efd6d6").pack(pady=5)

tk.Label(frame_config, text="Tamaño de letra:", bg="#f0aeae").pack()
escala_fuente = tk.Scale(frame_config, from_=10, to=25, orient="horizontal", bg="#f0aeae")
escala_fuente.set(config["tam_fuente"])
escala_fuente.pack(pady=5)

modo_oscuro_var = tk.BooleanVar(value=config["modo_oscuro"])
tk.Checkbutton(frame_config, text="Modo oscuro", variable=modo_oscuro_var, bg="#f0aeae").pack(pady=5)

sonido_var = tk.BooleanVar(value=config["sonido"])
tk.Checkbutton(frame_config, text="Sonido", variable=sonido_var, bg="#f0aeae").pack(pady=5)

def aplicar_estilos():
    bg = "#2b2b2b" if config["modo_oscuro"] else config["color_fondo"]
    fg = "#ffffff" if config["modo_oscuro"] else "#000000"
    ventana.configure(bg=bg)
    for frame in frames.values():
        frame.configure(bg=bg)
    titulo.configure(bg=bg, fg=fg)

def aplicar_cambios():
    config["tam_fuente"] = escala_fuente.get()
    config["modo_oscuro"] = modo_oscuro_var.get()
    config["sonido"] = sonido_var.get()
    guardar_configuracion(config)
    aplicar_estilos()
    messagebox.showinfo("Configuración", "Cambios aplicados con éxito.")

tk.Button(frame_config, text="Aplicar cambios", command=aplicar_cambios, bg="#b0e0b0").pack(pady=10)
tk.Button(frame_config, text="⬅ Volver", command=lambda: mostrar_frame("inicio"), bg="#ffffff").pack(pady=60)

# ---------- FRAME PICTOGRAMAS ----------
frame_pictogramas = tk.Frame(contenedor, bg="#98eccc")
frames["pictogramas"] = frame_pictogramas

tk.Label(frame_pictogramas, text="Pictogramas TEA 🖼️", font=("Comic Sans MS", 20, "bold"), bg="#98eccc").pack(pady=20)
tk.Label(frame_pictogramas, text="Recursos de comunicación visual organizados por categorías.", font=("Comic Sans MS", 13), bg="#98eccc").pack(pady=5)

# Contenedor de pestañas para organizar pictogramas
tab_view_pictos = ctk.CTkTabview(frame_pictogramas, width=680, height=450, fg_color="#e6f2ff", segmented_button_fg_color="#3498db")
tab_view_pictos.pack(pady=10, padx=10)

tab_view_pictos.add("Acciones 🏃")
tab_view_pictos.add("Emociones 😄")
tab_view_pictos.add("Lugares 🏥")
tab_view_pictos.set("Acciones 🏃")

# Obtener los frames de las pestañas
frame_acciones = tab_view_pictos.tab("Acciones 🏃")
frame_emociones = tab_view_pictos.tab("Emociones 😄")
frame_lugares = tab_view_pictos.tab("Lugares 🏥")

# Función para cargar y mostrar pictogramas
def cargar_pictogramas(frame_destino, carpeta):
    for widget in frame_destino.winfo_children():
        widget.destroy()

    tk.Label(frame_destino, text=f"Categoría: {carpeta}", font=("Comic Sans MS", 14, "bold"), bg="#e6f2ff").pack(pady=10)
    
    # Scrollable frame dentro de la pestaña
    canvas = tk.Canvas(frame_destino, bg="#e6f2ff", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    
    scrollbar = ctk.CTkScrollbar(frame_destino, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    
    pictos_container = tk.Frame(canvas, bg="#e6f2ff")
    canvas.create_window((0, 0), window=pictos_container, anchor="nw")

    # ---------- CARGA DE IMÁGENES ----------
    ruta_carpeta = resource_path(os.path.join("pictogramas", carpeta))    

    # Comprueba si la carpeta de pictogramas existe
    if not os.path.isdir(ruta_carpeta):
        tk.Label(pictos_container, text=f"ERROR: No se encontró la carpeta 'pictogramas/{carpeta}'", fg="red", bg="#e6f2ff").pack(pady=50)
        return
        
    archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    columna = 0
    fila = 0
    max_columnas = 3 # Muestra 4 pictogramas por fila
    
    # Lista global para mantener las referencias de las imágenes
    if not hasattr(cargar_pictogramas, 'imagenes_referencia'):
        cargar_pictogramas.imagenes_referencia = []

    for archivo in archivos:
        try:
            ruta_imagen = os.path.join(ruta_carpeta, archivo)
            # Cargar y redimensionar imagen
            imagen_pil = Image.open(ruta_imagen)
            imagen_pil = imagen_pil.resize((190, 190), Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen_pil)
            
            # Guardar referencia de la imagen
            cargar_pictogramas.imagenes_referencia.append(imagen_tk)
            
            # Texto que aparece debajo de la imagen
            nombre_limpio = archivo.split('.')[0].replace('_', ' ').capitalize()
            
            # Label para mostrar la imagen y el texto
            label_imagen = tk.Label(pictos_container, image=imagen_tk, text=nombre_limpio, compound=tk.BOTTOM, bg="#ffffff", bd=1, relief="solid", font=("Comic Sans MS", 10))
            label_imagen.grid(row=fila, column=columna, padx=10, pady=10)
            
            # Actualizar posición
            columna += 1
            if columna >= max_columnas:
                columna = 0
                fila += 1
                
        except Exception as e:
            print(f"Error al cargar la imagen {archivo}: {e}")
            
    # Función para actualizar el scrollregion
    pictos_container.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))


# --- CARGA EL CONTENIDO ---

cargar_pictogramas(frame_acciones, "Acciones")
cargar_pictogramas(frame_emociones, "Emociones")
cargar_pictogramas(frame_lugares, "Lugares")

tk.Button(frame_pictogramas, text="⬅ Volver al Inicio", command=lambda: mostrar_frame("inicio"), bg="#ffffff").pack(pady=15)

# ---------- INICIO ----------
mostrar_frame("inicio")
ventana.configure(bg=config["color_fondo"])
ventana.mainloop()
