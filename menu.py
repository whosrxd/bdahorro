# menu.py
import tkinter as tk
from tkinter import Frame  # <-- Frame clásico, acepta height
from tkinter.ttk import Button, Style
from clientes import clientes_app
from proveedores import proveedores_app
from empleados import empleados_app
from medicos import medicos_app
from unidades import unidades_app
from categoria import categoria_app
from datetime import datetime
import locale

class PuntoDeVenta:
    def __init__(self, usuario="Administrador"):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title("Punto de Venta - Farma Ahorro")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#E3F2FD")

        # Estilos globales
        style = Style()
        style.theme_use("default")
        style.configure("BotonAzul.TButton",
                        background="#64B5F6", foreground="black",
                        font=("Arial",12,"bold"), padding=(10,8))
        style.map("BotonAzul.TButton",
                  background=[("active", "#42A5F5")])

    def _limpiar(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def on_ventas(self):
        self._limpiar()


    def on_clientes(self):
        self._limpiar()
        clientes_app(self.contenedor)

    def on_proveedores(self):
        self._limpiar()
        proveedores_app(self.contenedor)

    def on_empleados(self):
        self._limpiar()
        empleados_app(self.contenedor)

    def on_medicos(self):
        self._limpiar()
        medicos_app(self.contenedor)

    def on_unidades(self):
        self._limpiar()
        unidades_app(self.contenedor)

    def on_categorias(self):
        self._limpiar()
        categoria_app(self.contenedor)

    def on_configuracion(self):
        if self.usuario != "Administrador":
            tk.messagebox.showinfo("Acceso Denegado", "Solo Administrador.")
            return
        self._limpiar()


    def on_reportes(self):
        self._limpiar()
        tk.Label(self.contenedor, text="Módulo Reportes",
                 font=("Arial",16), bg="white").pack(pady=50)

    def cambiar_usuario(self):
        # Lógica de logout/login
        pass

    def salir(self):
        self.root.destroy()

    def _actualizar_horario(self):
        try:
            locale.setlocale(locale.LC_TIME, "Spanish_Spain.1252")
        except:
            pass
        ahora = datetime.now()
        fecha = ahora.strftime("%A %d de %B de %Y").capitalize()
        hora  = ahora.strftime("%I:%M:%S %p")
        self.lbl_fecha.config(text=fecha)
        self.lbl_hora.config(text=hora)
        self.root.after(1000, self._actualizar_horario)

    def main(self):
        # Cabecera (ahora con tk.Frame)
        cabecera = Frame(self.root, bg="#ECECEC", height=30)
        cabecera.pack(fill=tk.X)
        tk.Label(cabecera, text="Punto de Venta Farma Ahorro",
                 bg="#ECECEC", font=("Arial",10,"bold")).pack(side=tk.LEFT, padx=10)
        tk.Label(cabecera, text=f"Usuario: {self.usuario}",
                 bg="#ECECEC", font=("Arial",10,"bold")).pack(side=tk.RIGHT, padx=10)

        # Menú
        menu = Frame(self.root, bg="#E3F2FD", height=50)
        menu.pack(fill=tk.X, pady=(5,0))

        opciones = [
            ("Ventas",      self.on_ventas),
            ("Clientes",    self.on_clientes),
            ("Proveedores", self.on_proveedores),
            ("Empleados",   self.on_empleados),
            ("Médicos",     self.on_medicos),
            ("Unidades",    self.on_unidades),
            ("Categorías",  self.on_categorias),
            ("Configuración", self.on_configuracion),
            ("Reportes",    self.on_reportes),
        ]
        for texto, cmd in opciones:
            Button(menu, text=texto, style="BotonAzul.TButton",
                   command=cmd).pack(side=tk.LEFT, padx=5, pady=5)

        Button(menu, text="Cambiar Usuario", style="BotonAzul.TButton",
               command=self.cambiar_usuario).pack(side=tk.RIGHT, padx=5)
        Button(menu, text="Salir", style="BotonAzul.TButton",
               command=self.salir).pack(side=tk.RIGHT, padx=5)

        # Contenedor principal
        self.contenedor = Frame(self.root, bg="white")
        self.contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pie con fecha y hora (tk.Frame)
        pie = Frame(self.root, bg="black", height=40)
        pie.pack(fill=tk.X)
        self.lbl_fecha = tk.Label(pie, bg="black", fg="white", font=("Arial",12))
        self.lbl_fecha.pack(side=tk.LEFT, padx=10)
        self.lbl_hora  = tk.Label(pie, bg="black", fg="white", font=("Arial",12))
        self.lbl_hora.pack(side=tk.RIGHT, padx=10)
        self._actualizar_horario()

        # Vista inicial
        self.on_ventas()
        self.root.mainloop()

if __name__ == "__main__":
    app = PuntoDeVenta()
    app.main()
