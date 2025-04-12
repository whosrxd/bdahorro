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

# Estilo para Labels de título
label_titulo_config = {
    "bg": "#E3F2FD",
    "fg": "black",
    "font": ("Arial", 10, "bold")
}

# Estilo del botón
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

# ===== Médicos (FORMULARIO ARRIBA) =====
Label(ventana, text="Médicos", **label_titulo_config).place(x=20, y=10)

# Columna única con los 4 campos
Label(ventana, text="ID Médico", **label_config).place(x=40, y=40)
Entry(ventana, **entry_config).place(x=150, y=40, width=200)

Label(ventana, text="Nombre", **label_config).place(x=40, y=70)
Entry(ventana, **entry_config).place(x=150, y=70, width=200)

Label(ventana, text="Especialidad", **label_config).place(x=40, y=100)
Entry(ventana, **entry_config).place(x=150, y=100, width=200)

Label(ventana, text="Teléfono", **label_config).place(x=40, y=130)
Entry(ventana, **entry_config).place(x=150, y=130, width=200)

# ===== Botones =====
Button(ventana, text="Agregar", style="BotonAzul.TButton").place(x=170, y=170, width=90)
Button(ventana, text="Modificar", style="BotonAzul.TButton").place(x=275, y=170, width=90)
Button(ventana, text="Eliminar", style="BotonAzul.TButton").place(x=380, y=170, width=90)

# ===== Tabla de Médicos =====
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

tabla = ttk.Treeview(ventana, columns=("idmedico", "nombre", "especialidad", "telefono"), show="headings")
tabla.place(x=40, y=210, width=560, height=300)

tabla.heading("idmedico", text="ID Médico")
tabla.heading("nombre", text="Nombre")
tabla.heading("especialidad", text="Especialidad")
tabla.heading("telefono", text="Teléfono")

tabla.column("idmedico", width=100, anchor="center")
tabla.column("nombre", width=100, anchor="center")
tabla.column("especialidad", width=180, anchor="center")
tabla.column("telefono", width=100, anchor="center")

ventana.mainloop()