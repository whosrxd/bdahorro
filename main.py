from tkinter import Canvas, Frame, Tk, NW, Button, Label
from PIL import Image, ImageTk
from categorias import categorias_app
from clientes import clientes_app
from empleados import empleados_app
from medicos import medicos_app
from proveedores import proveedores_app
from unidades import unidades_app
from medicamentos import medicamentos_app
from ventas import ventas_app
from compras import compras_app
from consultas import consultas_app
from recetas import recetas_app
from detalle_recetas import detalle_recetas_app
from detalle_compras import detalle_compras_app
from detalle_ventas import detalle_ventas_app

def interfaz():
    def seleccionar_boton(indice):
        for i, btn in enumerate(botones):
            if i == indice:
                btn.config(
                    bg="#FF3131", fg="red",
                    activebackground="#FF3131", activeforeground="#FF3131",
                    highlightbackground="#FF3131", highlightcolor="white",
                    highlightthickness=2, bd=0, relief="flat"
                )
            else:
                btn.config(
                    bg="white", fg="#FF3131",
                    activebackground="white",
                    activeforeground="#FF3131",
                    highlightbackground="#FF3131",
                    highlightthickness=0,
                    bd=0,
                    relief="flat"
                )
                
    ventana = Tk()
    ventana.title("Farmacias del Ahorro - DB")
    ventana.attributes('-fullscreen', True)

    ventana.grid_columnconfigure(0, weight=0)
    ventana.grid_columnconfigure(1, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    sidebar = Frame(ventana, bg="#FF3131", width=250)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)

    contenido = Frame(ventana, bg="#FFFFFF")
    contenido.grid(row=0, column=1, sticky="nsew")

    sidebar_contenido = Frame(sidebar, bg="#FF3131")
    sidebar_contenido.pack(pady=65, fill="x")

    imagen_ruta = "assets/ahorro.png"
    imagen = Image.open(imagen_ruta).resize((150, 150))
    imagen_tk = ImageTk.PhotoImage(imagen)
    canvas = Canvas(sidebar_contenido, width=250, height=150, bg="#FF3131", highlightthickness=0)
    canvas.create_image(50, 0, anchor=NW, image=imagen_tk)
    canvas.pack()

    label_titulos = {"bg": "#FF3131", "fg": "#FFFFFF", "font": ("Arial", 35, "bold")}
    Label(sidebar_contenido, text="Farmacias", **label_titulos).pack()
    Label(sidebar_contenido, text="del Ahorro", **label_titulos).pack(pady=(0, 30))

    botones_texto = [
        ("Categorías", lambda: categorias_app(contenido)),
        ("Clientes", lambda: clientes_app(contenido)),
        ("Compras", lambda: compras_app(contenido)),
        ("Consultas", lambda: consultas_app(contenido)),
        ("Detalle Compras", lambda: detalle_compras_app(contenido)),
        ("Detalle Recetas", lambda: detalle_recetas_app(contenido)),
        ("Detalle Ventas", lambda: detalle_ventas_app(contenido)),
        ("Empleados", lambda: empleados_app(contenido)),
        ("Medicamentos", lambda: medicamentos_app(contenido)),
        ("Médicos", lambda: medicos_app(contenido)),
        ("Proveedores", lambda: proveedores_app(contenido)),
        ("Recetas", lambda: recetas_app(contenido)),
        ("Unidades", lambda: unidades_app(contenido)),
        ("Ventas", lambda: ventas_app(contenido)),
        ("Salir", ventana.quit)
    ]

    botones_frame = Frame(sidebar_contenido, bg="#FF3131")
    botones_frame.pack(pady=60, fill="x")

    botones = []
    for i, (texto, funcion) in enumerate(botones_texto):
        btn = Button(
            botones_frame, text=texto, font=("Arial", 12),
            bg="white", fg="#FF3131",
            relief="flat", bd=0,
            activebackground="white",
            activeforeground="#FF3131",
            highlightthickness=0,
            command=funcion
        )
        btn.pack(fill="x", padx=5, pady=3)
        btn.config(width=20)
        btn.bind("<Button-1>", lambda e, index=i: seleccionar_boton(index))
        botones.append(btn)
        
        seleccionar_boton(0)
        
    ventana.mainloop()