from tkinter import Tk, Label, Entry, Frame, BOTH, ttk, messagebox

ventana = Tk()
ventana.title("Catálogo General")
ventana.attributes('-fullscreen', True)
ventana.configure(bg="#E3F2FD")

def salir_pantalla_completa(event):
    ventana.attributes('-fullscreen', False)

ventana.bind("<Escape>", salir_pantalla_completa)

# ===== Funciones =====
def agregar_categoria():
    id_cat = entry_id.get()
    nombre_cat = entry_nombre.get()

    if not id_cat or not nombre_cat:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Verificar si ya existe ese ID
    for item in tabla.get_children():
        if tabla.item(item, "values")[0] == id_cat:
            messagebox.showerror("Error", "Ya existe una categoría con ese ID.")
            return

    tabla.insert("", "end", values=(id_cat, nombre_cat))
    limpiar_campos()

def modificar_categoria():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para modificar.")
        return

    id_cat = entry_id.get()
    nombre_cat = entry_nombre.get()

    if not id_cat or not nombre_cat:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    tabla.item(seleccion, values=(id_cat, nombre_cat))
    limpiar_campos()

def eliminar_categoria():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para eliminar.")
        return

    tabla.delete(seleccion)
    limpiar_campos()

def seleccionar_fila(event):
    seleccion = tabla.selection()
    if seleccion:
        valores = tabla.item(seleccion[0], "values")
        entry_id.delete(0, "end")
        entry_nombre.delete(0, "end")
        entry_id.insert(0, valores[0])
        entry_nombre.insert(0, valores[1])

def limpiar_campos():
    entry_id.delete(0, "end")
    entry_nombre.delete(0, "end")

# ===== Estilos =====
entry_config = {
    "bg": "#BBDEFB",
    "fg": "black",
    "relief": "flat",
    "highlightthickness": 0,
    "bd": 0,
    "font": ("Arial", 16),
    "width": 25
}

label_config = {
    "bg": "#E3F2FD",
    "fg": "black",
    "font": ("Arial", 14)
}

label_titulo_config = {
    "bg": "#E3F2FD",
    "fg": "black",
    "font": ("Arial", 18, "bold")
}

style = ttk.Style()
style.theme_use("default")

style.configure("BotonAzul.TButton",
                background="#64B5F6",
                foreground="black",
                borderwidth=0,
                font=("Arial", 12, "bold"),
                padding=(10, 10))

style.map("BotonAzul.TButton",
          background=[("active", "#42A5F5")])

style.configure("BotonAzul.TButton", relief="flat", focuscolor="", anchor="center")

# ===== Marco principal centrado =====
frame_contenido = Frame(ventana, bg="#E3F2FD")
frame_contenido.pack(expand=True)

Label(frame_contenido, text="Categoría", **label_titulo_config).grid(row=0, column=0, columnspan=2, pady=20)

Label(frame_contenido, text="ID Categoría", **label_config).grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_id = Entry(frame_contenido, **entry_config)
entry_id.grid(row=1, column=1, padx=10, pady=5)

Label(frame_contenido, text="Nombre", **label_config).grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_nombre = Entry(frame_contenido, **entry_config)
entry_nombre.grid(row=2, column=1, padx=10, pady=5)

botones_frame = Frame(frame_contenido, bg="#E3F2FD")
botones_frame.grid(row=3, column=0, columnspan=2, pady=20)

ttk.Button(botones_frame, text="Agregar", style="BotonAzul.TButton", command=agregar_categoria).pack(side="left", padx=10)
ttk.Button(botones_frame, text="Modificar", style="BotonAzul.TButton", command=modificar_categoria).pack(side="left", padx=10)
ttk.Button(botones_frame, text="Eliminar", style="BotonAzul.TButton", command=eliminar_categoria).pack(side="left", padx=10)

# ===== Tabla =====
tabla = ttk.Treeview(ventana, columns=("idcategoria", "nombre"), show="headings")
tabla.pack(pady=20, padx=100, fill=BOTH, expand=True)

tabla.heading("idcategoria", text="ID Categoría")
tabla.heading("nombre", text="Nombre")

tabla.column("idcategoria", anchor="center")
tabla.column("nombre", anchor="center")

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=35,
                font=("Arial", 13),
                fieldbackground="white")

style.configure("Treeview.Heading",
                background="#90CAF9",
                foreground="black",
                font=("Arial", 14, "bold"))

style.map("Treeview", background=[("selected", "#64B5F6")])

tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

ventana.mainloop()