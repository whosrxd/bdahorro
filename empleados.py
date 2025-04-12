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

# ===== Empleados (FORMULARIO ARRIBA) =====
Label(ventana, text="Empleados", **label_titulo_config).place(x=20, y=10)

# Columna 1 (izquierda)
Label(ventana, text="ID Empleado", **label_config).place(x=40, y=40)
Entry(ventana, **entry_config).place(x=150, y=40, width=180)

Label(ventana, text="Nombre", **label_config).place(x=40, y=70)
Entry(ventana, **entry_config).place(x=150, y=70, width=180)

Label(ventana, text="Teléfono", **label_config).place(x=40, y=100)
Entry(ventana, **entry_config).place(x=150, y=100, width=180)

# Columna 2 (derecha)
Label(ventana, text="Dirección", **label_config).place(x=360, y=40)
Entry(ventana, **entry_config).place(x=470, y=40, width=150)

Label(ventana, text="Puesto", **label_config).place(x=360, y=70)
Entry(ventana, **entry_config).place(x=470, y=70, width=150)

Label(ventana, text="Fecha Contratación", **label_config).place(x=360, y=100)
Entry(ventana, **entry_config).place(x=470, y=100, width=150)

# ===== Botones =====
Button(ventana, text="Agregar", style="BotonAzul.TButton").place(x=170, y=140, width=90)
Button(ventana, text="Modificar", style="BotonAzul.TButton").place(x=275, y=140, width=90)
Button(ventana, text="Eliminar", style="BotonAzul.TButton").place(x=380, y=140, width=90)

# ===== Tabla de Empleados =====
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

tabla = ttk.Treeview(ventana, columns=("idempleado", "nombre", "telefono", "direccion", "puesto", "fecha_contratacion"), show="headings")
tabla.place(x=40, y=190, width=560, height=300)

tabla.heading("idempleado", text="ID Empleado")
tabla.heading("nombre", text="Nombre")
tabla.heading("telefono", text="Teléfono")
tabla.heading("direccion", text="Dirección")
tabla.heading("puesto", text="Puesto")
tabla.heading("fecha_contratacion", text="Fecha Contratación")

tabla.column("idempleado", width=90, anchor="center")
tabla.column("nombre", width=100, anchor="center")
tabla.column("telefono", width=90, anchor="center")
tabla.column("direccion", width=110, anchor="center")
tabla.column("puesto", width=80, anchor="center")
tabla.column("fecha_contratacion", width=90, anchor="center")

ventana.mainloop()