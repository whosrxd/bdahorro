from tkinter import Tk, Label, Entry, ttk

ventana = Tk()
ventana.title("Catálogo General")
ventana.geometry("640x500")
ventana.configure(bg="#E3F2FD")  # Fondo azul muy claro

# Estilo para los Entry
entry_config = {
    "bg": "#BBDEFB",
    "fg": "black",
    "relief": "flat",
    "highlightthickness": 0,
    "bd": 0
}

# Estilo para Labels normales
label_config = {
    "bg": "#E3F2FD",
    "fg": "black",
    "font": ("Arial", 10)
}

# Estilo para Labels de título (negrita)
label_titulo_config = {
    "bg": "#E3F2FD",
    "fg": "black",
    "font": ("Arial", 10, "bold")
}

# ===== Estilo del botón tipo Bootstrap =====
style = ttk.Style()
style.theme_use("default")

style.configure("BotonAzul.TButton",
                background="#64B5F6",
                foreground="black",
                borderwidth=0,
                focusthickness=0,
                focuscolor="",
                font=("Arial", 10))
style.map("BotonAzul.TButton",
          background=[("active", "#42A5F5")])

# ===== Categoría =====
Label(ventana, text="Categoría", **label_titulo_config).place(x=20, y=10)

Label(ventana, text="ID Categoría", **label_config).place(x=40, y=40)
entry_id = Entry(ventana, **entry_config)
entry_id.place(x=150, y=40, width=200)

Label(ventana, text="Nombre", **label_config).place(x=40, y=70)
entry_nombre = Entry(ventana, **entry_config)
entry_nombre.place(x=150, y=70, width=200)

ttk.Button(ventana, text="Agregar", style="BotonAzul.TButton").place(x=370, y=55, width=80)
ttk.Button(ventana, text="Modificar", style="BotonAzul.TButton").place(x=460, y=55, width=80)
ttk.Button(ventana, text="Eliminar", style="BotonAzul.TButton").place(x=550, y=55, width=80)

# ===== Tabla de Categoría =====
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white",
                bordercolor="black",
                borderwidth=1)

style.configure("Treeview.Heading",
                background="#90CAF9",
                foreground="black",
                font=("Arial", 10, "bold"))

style.map("Treeview", background=[("selected", "#64B5F6")])

tabla = ttk.Treeview(ventana, columns=("idcategoria", "nombre"), show="headings")
tabla.place(x=40, y=120, width=560, height=300)

tabla.heading("idcategoria", text="ID Categoría")
tabla.heading("nombre", text="Nombre")

tabla.column("idcategoria", width=200, anchor="center")
tabla.column("nombre", width=350, anchor="center")

ventana.mainloop()