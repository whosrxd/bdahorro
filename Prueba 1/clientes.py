from tkinter import Tk, Label, Entry, ttk
from tkinter.ttk import Button

ventana = Tk()
ventana.title("Catálogo General")
ventana.geometry("640x600")
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

# Estilo del botón tipo Bootstrap
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

# ===== Cliente (FORMULARIO ARRIBA) =====
Label(ventana, text="Cliente", **label_titulo_config).place(x=20, y=10)

# Columna izquierda (3 campos)
Label(ventana, text="ID Cliente", **label_config).place(x=40, y=40)
Entry(ventana, **entry_config).place(x=130, y=40, width=180)

Label(ventana, text="Nombre", **label_config).place(x=40, y=80)
Entry(ventana, **entry_config).place(x=130, y=80, width=180)

Label(ventana, text="Teléfono", **label_config).place(x=40, y=120)
Entry(ventana, **entry_config).place(x=130, y=120, width=180)

# Columna derecha (2 campos)
Label(ventana, text="Dirección", **label_config).place(x=340, y=40)
Entry(ventana, **entry_config).place(x=430, y=40, width=170)

Label(ventana, text="Correo", **label_config).place(x=340, y=80)
Entry(ventana, **entry_config).place(x=430, y=80, width=170)

# ===== Botones =====
Button(ventana, text="Agregar", style="BotonAzul.TButton").place(x=170, y=160, width=90)
Button(ventana, text="Modificar", style="BotonAzul.TButton").place(x=275, y=160, width=90)
Button(ventana, text="Eliminar", style="BotonAzul.TButton").place(x=380, y=160, width=90)

# ===== Tabla de Cliente =====
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

tabla = ttk.Treeview(ventana, columns=("idcliente", "nombre", "telefono", "direccion", "correo"), show="headings")
tabla.place(x=40, y=210, width=560, height=360)

tabla.heading("idcliente", text="ID Cliente")
tabla.heading("nombre", text="Nombre")
tabla.heading("telefono", text="Teléfono")
tabla.heading("direccion", text="Dirección")
tabla.heading("correo", text="Correo")

tabla.column("idcliente", width=80, anchor="center")
tabla.column("nombre", width=120, anchor="center")
tabla.column("telefono", width=90, anchor="center")
tabla.column("direccion", width=130, anchor="center")
tabla.column("correo", width=140, anchor="center")

ventana.mainloop()