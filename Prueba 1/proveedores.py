from tkinter import Tk, Label, Entry, ttk
from tkinter.ttk import Button

ventana = Tk()
ventana.title("Catálogo General")
ventana.geometry("640x600")
ventana.configure(bg="#E3F2FD")  # Fondo azul muy claro

# Estilo para los Entry
entry_config = {
    "bg": "#BBDEFB",       # azul clarito
    "fg": "black",         # texto negro
    "relief": "flat",      # sin borde
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

# ===== Proveedores (FORMULARIO ARRIBA) =====
Label(ventana, text="Proveedores", **label_titulo_config).place(x=20, y=10)

Label(ventana, text="ID Proveedor", **label_config).place(x=40, y=40)
Entry(ventana, **entry_config).place(x=150, y=40, width=200)

Label(ventana, text="Nombre", **label_config).place(x=40, y=70)
Entry(ventana, **entry_config).place(x=150, y=70, width=200)

Label(ventana, text="Teléfono", **label_config).place(x=40, y=100)
Entry(ventana, **entry_config).place(x=150, y=100, width=200)

Label(ventana, text="Contacto", **label_config).place(x=40, y=130)
Entry(ventana, **entry_config).place(x=150, y=130, width=200)

# ===== Botones =====
Button(ventana, text="Agregar", style="BotonAzul.TButton").place(x=170, y=170, width=90)
Button(ventana, text="Modificar", style="BotonAzul.TButton").place(x=275, y=170, width=90)
Button(ventana, text="Eliminar", style="BotonAzul.TButton").place(x=380, y=170, width=90)

# ===== Tabla de Proveedores =====
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

tabla = ttk.Treeview(ventana, columns=("idproveedor", "nombre", "telefono", "contacto"), show="headings")
tabla.place(x=40, y=210, width=560, height=250)

tabla.heading("idproveedor", text="ID Proveedor")
tabla.heading("nombre", text="Nombre")
tabla.heading("telefono", text="Teléfono")
tabla.heading("contacto", text="Contacto")

tabla.column("idproveedor", width=100, anchor="center")
tabla.column("nombre", width=150, anchor="center")
tabla.column("telefono", width=150, anchor="center")
tabla.column("contacto", width=150, anchor="center")

ventana.mainloop()