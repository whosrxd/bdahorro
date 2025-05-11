# Importamos todo lo necesario de Tkinter y ttk para crear la interfaz
from tkinter import Tk, Label, Entry, Frame, BOTH, ttk, messagebox
from tkinter.ttk import Button, Notebook
from validaciones import validar_puesto, validar_nombre, validar_correo, validar_telefono, validar_id, validar_fecha, validar_especialidad, mostrar_mensaje_error

# Configuración de la ventana principal
ventana = Tk()  # Crea la ventana principal
ventana.title("CRUD")  # Título de la ventana
ventana.attributes('-fullscreen', True)  # La pone en pantalla completa
ventana.configure(bg = "#E3F2FD")  # Color de fondo

# Pestañas
notebook = Notebook(ventana)  # Crea el contenedor para pestañas
notebook.pack(fill = BOTH, expand = True)  # Lo ajusta al tamaño de la ventana

# Estilos de los Entry y Labels
entry_config = {
    "bg": "#BBDEFB", "fg": "black", "relief": "flat", "highlightthickness": 0,
    "bd": 0, "font": ("Arial", 16), "width": 25
}
label_config = {"bg": "#E3F2FD", "fg": "black", "font": ("Arial", 14)}
label_titulo_config = {"bg": "#E3F2FD", "fg": "black", "font": ("Arial", 18, "bold")}

# ===================== PESTAÑA 1: Categoría =====================
pestana_categoria = Frame(notebook, bg = "#E3F2FD")  # Crea una pestaña
notebook.add(pestana_categoria, text = "Categoría")  # La añade al notebook

# Funciones CRUD

# Añadir nueva categoría a la tabla
def agregar_categoria():
    id_categoria = entry_id.get()
    nombre_categoria = entry_nombre.get()
    
    # Validaciones

    if not id_categoria or not nombre_categoria:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Verifica si ya existe una categoría con ese ID
    for item in tabla_categoria.get_children():
        if tabla_categoria.item(item, "values")[0] == id_categoria:
            messagebox.showerror("Error", "Ya existe una categoría con ese ID.")
            return
        
    if not validar_nombre(nombre_categoria):
        messagebox.showerror("Error", mostrar_mensaje_error("nombre"))
        return
    
    if not validar_id(id_categoria):
        messagebox.showerror("Error", mostrar_mensaje_error("id"))
        return

    nuevo_item_categoria = tabla_categoria.insert("", "end", values=(id_categoria, nombre_categoria))
    items_categorias.append(nuevo_item_categoria)  # 👈 Esto es lo que faltaba
    limpiar_campos_categoria()

# Modificar la categoría seleccionada
def modificar_categoria():
    seleccion = tabla_categoria.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para modificar.")
        return

    id_categoria = entry_id.get()
    nombre_categoria = entry_nombre.get()

    if not id_categoria or not nombre_categoria:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    tabla_categoria.item(seleccion, values=(id_categoria, nombre_categoria))
    limpiar_campos_categoria()

# Eliminar la categoría seleccionada
def eliminar_categoria():
    seleccion = tabla_categoria.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para eliminar.")
        return

    tabla_categoria.delete(seleccion)
    limpiar_campos_categoria()

# Cuando seleccionas una fila de la tabla, se pasan los datos a los Entry
def seleccionar_fila_categoria(event):
    seleccion = tabla_categoria.selection()
    if seleccion:
        valores = tabla_categoria.item(seleccion[0], "values")
        entry_id.delete(0, "end")
        entry_nombre.delete(0, "end")
        entry_id.insert(0, valores[0])
        entry_nombre.insert(0, valores[1])

# Limpia los campos de texto
def limpiar_campos_categoria():
    entry_id.delete(0, "end")
    entry_nombre.delete(0, "end")
    
# Guardamos los IDs de cada fila al momento de insertar los datos
items_categorias = []

def buscar_categoria():
    termino = entry_busqueda_categoria.get().lower().strip()
    if not termino:
        mostrar_categoria()
        return

    for item in items_categorias:
        valores = tabla_categoria.item(item, "values")
        if termino not in valores[0].lower():  # ahora busca por ID
            tabla_categoria.detach(item)
        else:
            tabla_categoria.reattach(item, '', 'end')

def mostrar_categoria():
    for item in items_categorias:
        tabla_categoria.reattach(item, '', 'end')
    entry_busqueda_categoria.delete(0, "end")

# Estilo de botones
style = ttk.Style()
style.theme_use("default")  # Usamos el tema base de ttk

# Estilo de la tabla
style.configure("Treeview",
    background = "white",
    foreground = "black",
    rowheight = 35,
    font = ("Arial", 13),
    fieldbackground = "white"
)
style.configure("Treeview.Heading",
    background = "#90CAF9",
    foreground = "black",
    font = ("Arial", 14, "bold")
)
style.map("Treeview", background = [("selected", "#64B5F6")])  # Color cuando seleccionas fila

# Creamos un nuevo estilo llamado "BotonAzul.TButton"
style.configure("BotonAzul.TButton",
    background = "#64B5F6",  # Color normal
    foreground = "black",
    borderwidth = 0,
    font = ("Arial", 12, "bold"),
    padding = (10, 10),
    relief = "flat"
)
style.map("BotonAzul.TButton", background = [("active", "#42A5F5")])  # Color al pasar el mouse

# Contenedor para los Labels y Entrys
frame_categoria = Frame(pestana_categoria, bg="#E3F2FD")
frame_categoria.pack(expand=True)

# Título del formulario
Label(frame_categoria, text = "Categoría", **label_titulo_config).grid(row = 0, column = 0, columnspan = 2, pady = 20)

# ID Categoría
Label(frame_categoria, text = "ID Categoría", **label_config).grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 5)
entry_id = Entry(frame_categoria, **entry_config)
entry_id.grid(row = 1, column = 1, padx = 10, pady = 5)

# Nombre Categoría
Label(frame_categoria, text = "Nombre", **label_config).grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 5)
entry_nombre = Entry(frame_categoria, **entry_config)
entry_nombre.grid(row = 2, column = 1, padx = 10, pady = 5)

# Frame que contiene los botones
botones_frame = Frame(frame_categoria, bg = "#E3F2FD")
botones_frame.grid(row = 3, column = 0, columnspan = 2, pady = 20)

# Botones con su respectivo comando
Button(botones_frame, text = "Agregar", style = "BotonAzul.TButton", command = agregar_categoria).pack(side = "left", padx = 10)
Button(botones_frame, text = "Modificar", style = "BotonAzul.TButton", command = modificar_categoria).pack(side = "left", padx = 10)
Button(botones_frame, text = "Eliminar", style = "BotonAzul.TButton", command = eliminar_categoria).pack(side = "left", padx = 10)

# Frame para la búsqueda
frame_busqueda_categoria = Frame(pestana_categoria, bg="#E3F2FD")
frame_busqueda_categoria.pack(pady=10)

# Buscar ID Categoría
# Label + Entry
Label(frame_busqueda_categoria, text="Buscar:", **label_config).pack(side="left", padx=5)
entry_busqueda_categoria = Entry(frame_busqueda_categoria, **entry_config)
entry_busqueda_categoria.pack(side="left", padx=5)
entry_busqueda_categoria.bind("<KeyRelease>", lambda event: buscar_categoria())

# Creamos la tabla con dos columnas
tabla_categoria = ttk.Treeview(pestana_categoria, columns = ("idcategoria", "nombre"), show="headings")
tabla_categoria.pack(pady = 20, padx = 100, fill = BOTH, expand = True)

# Encabezados de columna
tabla_categoria.heading("idcategoria", text = "ID Categoría")
tabla_categoria.heading("nombre", text = "Nombre")

# Centrado de columnas
tabla_categoria.column("idcategoria", anchor = "center")
tabla_categoria.column("nombre", anchor = "center")

# Evento para que se llenen los Entry al seleccionar una fila
tabla_categoria.bind("<<TreeviewSelect>>", seleccionar_fila_categoria)

# ===================== PESTAÑA 2: Cliente =====================
pestana_cliente = Frame(notebook, bg = "#E3F2FD")
notebook.add(pestana_cliente, text = "Cliente")

# Funciones CRUD

# Añadir nuevo cliente a la tabla
def agregar_cliente():
    id_cliente = entry_idcli.get()
    nombre_clientes = entry_nombrecli.get() 
    telefono_clientes = entry_telcli.get()
    direccion_clientes = entry_dircli.get()
    correo_clientes = entry_correocli.get() 
    
    # Validaciones
    
    if not validar_id(id_cliente):
        messagebox.showerror("Error", mostrar_mensaje_error("id"))
        return
    
    if not validar_nombre(nombre_clientes):
        messagebox.showerror("Error", mostrar_mensaje_error("nombre"))
        return
    
    if not validar_telefono(telefono_clientes):
        messagebox.showerror("Error", mostrar_mensaje_error("telefono"))
        return

    if not validar_correo(correo_clientes):
        messagebox.showerror("Error", mostrar_mensaje_error("correo"))
        return

    if not id_cliente or not nombre_clientes or not telefono_clientes or not direccion_clientes or not correo_clientes:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Verifica si ya existe un cliente con ese ID
    for item in tabla_clientes.get_children():
        if tabla_clientes.item(item, "values")[0] == id_cliente:
            messagebox.showerror("Error", "Ya existe un cliente con ese ID.")
            return

    nuevo_item_clientes = tabla_clientes.insert("", "end", values=(id_cliente, nombre_clientes, telefono_clientes, direccion_clientes, correo_clientes))
    items_clientes.append(nuevo_item_clientes)  # 👈 Esto es lo que faltaba
    limpiar_campos_cliente()

# Modificar el cliente seleccionado
def modificar_cliente():
    seleccion = tabla_clientes.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para modificar.")
        return

    id_cliente = entry_idcli.get()
    nombre_clientes = entry_nombrecli.get()
    telefono_clientes = entry_telcli.get()
    direccion_clientes = entry_dircli.get()
    correo_clientes = entry_correocli.get()

    if not id_cliente or not nombre_clientes or not telefono_clientes or not direccion_clientes or not correo_clientes:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    tabla_clientes.item(seleccion, values=(id_cliente, nombre_clientes, telefono_clientes, direccion_clientes, correo_clientes))
    limpiar_campos_cliente()

# Eliminar el cliente seleccionado
def eliminar_cliente():
    seleccion = tabla_clientes.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para eliminar.")
        return

    tabla_clientes.delete(seleccion)
    limpiar_campos_cliente()

# Cuando seleccionas una fila de la tabla, se pasan los datos a los Entry
def seleccionar_fila_cliente(event):
    seleccion = tabla_clientes.selection()
    if seleccion:
        valores = tabla_clientes.item(seleccion[0], "values")
        entry_idcli.delete(0, "end")
        entry_nombrecli.delete(0, "end")
        entry_telcli.delete(0, "end")
        entry_dircli.delete(0, "end")
        entry_correocli.delete(0, "end")

        entry_idcli.insert(0, valores[0])
        entry_nombrecli.insert(0, valores[1])
        entry_telcli.insert(0, valores[2])
        entry_dircli.insert(0, valores[3])
        entry_correocli.insert(0, valores[4])

# Limpia los campos de texto
def limpiar_campos_cliente():
    entry_idcli.delete(0, "end")
    entry_nombrecli.delete(0, "end")
    entry_telcli.delete(0, "end")
    entry_dircli.delete(0, "end")
    entry_correocli.delete(0, "end")
    
items_clientes = []

def buscar_cliente():
    termino = entry_busqueda_cliente.get().lower().strip()
    if not termino:
        mostrar_clientes()
        return

    for item in items_clientes:
        valores = tabla_clientes.item(item, "values")
        if termino not in valores[0].lower():  # ahora busca por ID
            tabla_clientes.detach(item)
        else:
            tabla_clientes.reattach(item, '', 'end')

def mostrar_clientes():
    for item in items_clientes:
        tabla_clientes.reattach(item, '', 'end')
    entry_busqueda_cliente.delete(0, "end")

# Contenedor para los Labels y Entrys
frame_cliente = Frame(pestana_cliente, bg = "#E3F2FD")
frame_cliente.pack(expand = True)

# Título del formulario
Label(frame_cliente, text = "Cliente", **label_titulo_config).grid(row = 0, column = 0, columnspan = 4, pady = 20)

# ID Cliente
Label(frame_cliente, text = "ID Cliente", **label_config).grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 5)
entry_idcli = Entry(frame_cliente, **entry_config)
entry_idcli.grid(row = 1, column = 1, padx = 10, pady = 5)

# Nombre Cliente
Label(frame_cliente, text = "Nombre", **label_config).grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 5)
entry_nombrecli = Entry(frame_cliente, **entry_config)
entry_nombrecli.grid(row = 2, column = 1, padx = 10, pady = 5)

# Teléfono Cliente
Label(frame_cliente, text = "Teléfono", **label_config).grid(row = 3, column = 0, sticky = "e", padx = 10, pady = 5)
entry_telcli = Entry(frame_cliente, **entry_config)
entry_telcli.grid(row = 3, column = 1, padx = 10, pady = 5)

# Dirección Cliente
Label(frame_cliente, text="Dirección", **label_config).grid(row = 1, column = 2, sticky = "e", padx = 10, pady = 5)
entry_dircli = Entry(frame_cliente, **entry_config)
entry_dircli.grid(row = 1, column = 3, padx = 10, pady = 5)

# Correo Cliente
Label(frame_cliente, text = "Correo", **label_config).grid(row = 2, column = 2, sticky = "e", padx = 10, pady = 5)
entry_correocli = Entry(frame_cliente, **entry_config)
entry_correocli.grid(row = 2, column = 3, padx = 10, pady = 5)

# Frame que contiene los botones
botones_cli_frame = Frame(frame_cliente, bg = "#E3F2FD")
botones_cli_frame.grid(row = 4, column = 0, columnspan = 4, pady = 20)

# Botones con su respectivo comando
Button(botones_cli_frame, text = "Agregar", style = "BotonAzul.TButton", command = agregar_cliente).pack(side = "left", padx=10)
Button(botones_cli_frame, text = "Modificar", style = "BotonAzul.TButton", command = modificar_cliente).pack(side = "left", padx=10)
Button(botones_cli_frame, text = "Eliminar", style = "BotonAzul.TButton", command = eliminar_cliente).pack(side = "left", padx=10)

# Frame para la búsqueda
frame_busqueda_cliente = Frame(pestana_cliente, bg="#E3F2FD")
frame_busqueda_cliente.pack(pady=10)

# Label + Entry
Label(frame_busqueda_cliente, text="Buscar:", **label_config).pack(side="left", padx=5)
entry_busqueda_cliente = Entry(frame_busqueda_cliente, **entry_config)
entry_busqueda_cliente.pack(side="left", padx=5)
entry_busqueda_cliente.bind("<KeyRelease>", lambda event: buscar_cliente())  # 🔥 Real-time search

# Creamos la tabla con cinco columnas
tabla_clientes = ttk.Treeview(pestana_cliente, columns = ("idcliente", "nombre", "telefono", "direccion", "correo"), show = "headings")
tabla_clientes.pack(pady = 20, padx = 100, fill = BOTH, expand = True)

# Encabezados de columna
tabla_clientes.heading("idcliente", text = "ID Cliente")
tabla_clientes.heading("nombre", text = "Nombre")
tabla_clientes.heading("telefono", text = "Teléfono")
tabla_clientes.heading("direccion", text = "Dirección")
tabla_clientes.heading("correo", text = "Correo")

# Centrado de columnas
tabla_clientes.column("idcliente", width = 80, anchor = "center")
tabla_clientes.column("nombre", width = 120, anchor = "center")
tabla_clientes.column("telefono", width = 90, anchor = "center")
tabla_clientes.column("direccion", width = 130, anchor = "center")
tabla_clientes.column("correo", width = 140, anchor = "center")

# Evento para que se llenen los Entry al seleccionar una fila
tabla_clientes.bind("<<TreeviewSelect>>", seleccionar_fila_cliente)

# ===================== PESTAÑA 3: Empleados =====================
pestana_empleados = Frame(notebook, bg = "#E3F2FD")
notebook.add(pestana_empleados, text = "Empleado")

# Funciones CRUD

# Añadir nuevo empleado a la tabla
def agregar_empleado():
    id_empleado = entry_idemp.get()
    nombre_empleado = entry_nombreemp.get() 
    telefono_empleado = entry_telemp.get()
    direccion_empleado = entry_diremp.get()
    puesto_empleado = entry_puestoemp.get() 
    fecha_empleado = entry_fechaemp.get()
    
    # Validaciones
    
    if not validar_id(id_empleado):
        messagebox.showerror("Error", mostrar_mensaje_error("id"))
        return
    
    if not validar_nombre(nombre_empleado):
        messagebox.showerror("Error", mostrar_mensaje_error("nombre"))
        return
    
    if not validar_telefono(telefono_empleado):
        messagebox.showerror("Error", mostrar_mensaje_error("telefono"))
        return
    
    if not validar_puesto(puesto_empleado):
        messagebox.showerror("Error", mostrar_mensaje_error("puesto"))
        return
    
    if not validar_fecha(fecha_empleado):
        messagebox.showerror("Error", mostrar_mensaje_error("fecha"))
        return

    if not id_empleado or not nombre_empleado or not telefono_empleado or not direccion_empleado or not puesto_empleado or not fecha_empleado:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Verifica si ya existe un empleado con ese ID
    for item in tabla_empleados.get_children():
        if tabla_empleados.item(item, "values")[0] == id_empleado:
            messagebox.showerror("Error", "Ya existe un empleado con ese ID.")
            return

    nuevo_item_empleados = tabla_empleados.insert("", "end", values=(id_empleado, nombre_empleado, telefono_empleado, direccion_empleado, puesto_empleado, fecha_empleado))
    items_empleados.append(nuevo_item_empleados)  # 👈 Esto es lo que faltaba
    limpiar_campos_empleado()

# Modificar el empleado seleccionado
def modificar_empleado():
    seleccion = tabla_empleados.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para modificar.")
        return

    id_empleado = entry_idemp.get()
    nombre_empleado = entry_nombreemp.get() 
    telefono_empleado = entry_telemp.get()
    direccion_empleado = entry_diremp.get()
    puesto_empleado = entry_puestoemp.get() 
    fecha_empleado = entry_fechaemp.get()

    if not id_empleado or not nombre_empleado or not telefono_empleado or not direccion_empleado or not puesto_empleado or not fecha_empleado:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    tabla_empleados.item(seleccion, values=(id_empleado, nombre_empleado, telefono_empleado, direccion_empleado, puesto_empleado, fecha_empleado))
    limpiar_campos_empleado()

# Eliminar el cliente seleccionado
def eliminar_empleado():
    seleccion = tabla_empleados.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para eliminar.")
        return

    tabla_empleados.delete(seleccion)
    limpiar_campos_empleado()

# Cuando seleccionas una fila de la tabla, se pasan los datos a los Entry
def seleccionar_fila_empleado(event):
    seleccion = tabla_empleados.selection()
    if seleccion:
        valores = tabla_empleados.item(seleccion[0], "values")
        entry_idemp.delete(0, "end")
        entry_nombreemp.delete(0, "end")
        entry_telemp.delete(0, "end")
        entry_diremp.delete(0, "end")
        entry_puestoemp.delete(0, "end")
        entry_fechaemp.delete(0, "end")

        entry_idemp.insert(0, valores[0])
        entry_nombreemp.insert(0, valores[1])
        entry_telemp.insert(0, valores[2])
        entry_diremp.insert(0, valores[3])
        entry_puestoemp.insert(0, valores[4])
        entry_fechaemp.insert(0, valores[5])

# Limpia los campos de texto
def limpiar_campos_empleado():
    entry_idemp.delete(0, "end")
    entry_nombreemp.delete(0, "end")
    entry_telemp.delete(0, "end")
    entry_diremp.delete(0, "end")
    entry_puestoemp.delete(0, "end")
    entry_fechaemp.delete(0, "end")
    
items_empleados = []

def buscar_empleado():
    termino = entry_busqueda_empleado.get().lower().strip()
    if not termino:
        mostrar_empleado()
        return

    for item in items_empleados:
        valores = tabla_empleados.item(item, "values")
        if termino not in valores[0].lower():  # ahora busca por ID
            tabla_empleados.detach(item)
        else:
            tabla_empleados.reattach(item, '', 'end')

def mostrar_empleado():
    for item in items_empleados:
        tabla_empleados.reattach(item, '', 'end')
    entry_busqueda_empleado.delete(0, "end")

# Contenedor para los Labels y Entrys
frame_empleado = Frame(pestana_empleados, bg = "#E3F2FD")
frame_empleado.pack(expand = True)

# Título del formulario
Label(frame_empleado, text = "Empleados", **label_titulo_config).grid(row = 0, column = 0, columnspan = 4, pady = 20)

# ID Empleado
Label(frame_empleado, text = "ID Empleado", **label_config).grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 5)
entry_idemp = Entry(frame_empleado, **entry_config)
entry_idemp.grid(row = 1, column = 1, padx = 10, pady = 5)

# Nombre Empleado
Label(frame_empleado, text = "Nombre", **label_config).grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 5)
entry_nombreemp = Entry(frame_empleado, **entry_config)
entry_nombreemp.grid(row = 2, column = 1, padx = 10, pady = 5)

# Teléfono Empleado
Label(frame_empleado, text = "Teléfono", **label_config).grid(row = 3, column = 0, sticky = "e", padx = 10, pady = 5)
entry_telemp = Entry(frame_empleado, **entry_config)
entry_telemp.grid(row = 3, column = 1, padx = 10, pady = 5)

# Dirección Cliente
Label(frame_empleado, text="Dirección", **label_config).grid(row = 1, column = 2, sticky = "e", padx = 10, pady = 5)
entry_diremp = Entry(frame_empleado, **entry_config)
entry_diremp.grid(row = 1, column = 3, padx = 10, pady = 5)

# Puesto Empleado
Label(frame_empleado, text = "Puesto", **label_config).grid(row = 2, column = 2, sticky = "e", padx = 10, pady = 5)
entry_puestoemp = Entry(frame_empleado, **entry_config)
entry_puestoemp.grid(row = 2, column = 3, padx = 10, pady = 5)

# Fecha Empleado
Label(frame_empleado, text = "Fecha", **label_config).grid(row = 3, column = 2, sticky = "e", padx = 10, pady = 5)
entry_fechaemp = Entry(frame_empleado, **entry_config)
entry_fechaemp.grid(row = 3, column = 3, padx = 10, pady = 5)

# Frame que contiene los botones
botones_emp_frame = Frame(frame_empleado, bg = "#E3F2FD")
botones_emp_frame.grid(row = 4, column = 0, columnspan = 4, pady = 20)

# Botones con su respectivo comando
Button(botones_emp_frame, text = "Agregar", style = "BotonAzul.TButton", command = agregar_empleado).pack(side = "left", padx=10)
Button(botones_emp_frame, text = "Modificar", style = "BotonAzul.TButton", command = modificar_empleado).pack(side = "left", padx=10)
Button(botones_emp_frame, text = "Eliminar", style = "BotonAzul.TButton", command = eliminar_empleado).pack(side = "left", padx=10)

# Frame para la búsqueda
frame_busqueda_empleado = Frame(pestana_empleados, bg="#E3F2FD")
frame_busqueda_empleado.pack(pady=10)

# Label + Entry
Label(frame_busqueda_empleado, text="Buscar:", **label_config).pack(side="left", padx=5)
entry_busqueda_empleado = Entry(frame_busqueda_empleado, **entry_config)
entry_busqueda_empleado.pack(side="left", padx=5)
entry_busqueda_empleado.bind("<KeyRelease>", lambda event: buscar_empleado())  # 🔥 Real-time search

# Creamos la tabla con cinco columnas
tabla_empleados = ttk.Treeview(pestana_empleados, columns = ("idempleado", "nombre", "telefono", "direccion", "puesto", "fecha"), show = "headings")
tabla_empleados.pack(pady = 20, padx = 100, fill = BOTH, expand = True)

# Encabezados de columna
tabla_empleados.heading("idempleado", text = "ID Empleado")
tabla_empleados.heading("nombre", text = "Nombre")
tabla_empleados.heading("telefono", text = "Teléfono")
tabla_empleados.heading("direccion", text = "Dirección")
tabla_empleados.heading("puesto", text = "Puesto")
tabla_empleados.heading("fecha", text = "Fecha de Contratación")

# Centrado de columnas
tabla_empleados.column("idempleado", width = 90, anchor = "center")
tabla_empleados.column("nombre", width = 100, anchor = "center")
tabla_empleados.column("telefono", width = 90, anchor = "center")
tabla_empleados.column("direccion", width = 110, anchor = "center")
tabla_empleados.column("puesto", width = 80, anchor = "center")
tabla_empleados.column("fecha", width = 90, anchor = "center")

# Evento para que se llenen los Entry al seleccionar una fila
tabla_empleados.bind("<<TreeviewSelect>>", seleccionar_fila_empleado)

# ===================== PESTAÑA 4: Médicos =====================
pestana_medicos = Frame(notebook, bg = "#E3F2FD")
notebook.add(pestana_medicos, text = "Médicos")

# Funciones CRUD

# Añadir nuevo médico a la tabla
def agregar_medico():
    id_medico = entry_idmed.get()
    nombre_medico = entry_nombremed.get() 
    especialidad_medico = entry_especialidadmed.get()
    telefono_medico = entry_telefonomed.get()
    
    # Validaciones
    
    if not validar_id(id_medico):
        messagebox.showerror("Error", mostrar_mensaje_error("id"))
        return
    
    if not validar_nombre(nombre_medico):
        messagebox.showerror("Error", mostrar_mensaje_error("nombre"))
        return
    
    if not validar_telefono(telefono_medico):
        messagebox.showerror("Error", mostrar_mensaje_error("telefono"))
        return
    
    if not validar_especialidad(especialidad_medico):
        messagebox.showerror("Error", mostrar_mensaje_error("especialidad"))
        return
 
    if not id_medico or not nombre_medico or not especialidad_medico or not telefono_medico:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Verifica si ya existe un médico con ese ID
    for item in tabla_medicos.get_children():
        if tabla_medicos.item(item, "values")[0] == id_medico:
            messagebox.showerror("Error", "Ya existe un médico con ese ID.")
            return

    nuevo_item_medicos = tabla_medicos.insert("", "end", values=(id_medico, nombre_medico, especialidad_medico, telefono_medico))
    items_medicos.append(nuevo_item_medicos)  # 👈 Esto es lo que faltaba
    limpiar_campos_medico()

# Modificar el médico seleccionado
def modificar_medico():
    seleccion = tabla_medicos.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para modificar.")
        return

    id_medico = entry_idmed.get()
    nombre_medico = entry_nombremed.get()
    especialidad_medico = entry_especialidadmed.get()
    telefono_medico = entry_telefonomed.get()

    if not id_medico or not nombre_medico or not especialidad_medico or not telefono_medico:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    tabla_medicos.item(seleccion, values=(id_medico, nombre_medico, especialidad_medico, telefono_medico))
    limpiar_campos_medico()

# Eliminar el médico seleccionado
def eliminar_medico():
    seleccion = tabla_medicos.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para eliminar.")
        return

    tabla_medicos.delete(seleccion)
    limpiar_campos_medico()

# Cuando seleccionas una fila de la tabla, se pasan los datos a los Entry
def seleccionar_fila_medico(event):
    seleccion = tabla_medicos.selection()
    if seleccion:
        valores = tabla_medicos.item(seleccion[0], "values")
        entry_idmed.delete(0, "end")
        entry_nombremed.delete(0, "end")
        entry_especialidadmed.delete(0, "end")
        entry_telefonomed.delete(0, "end")


        entry_idmed.insert(0, valores[0])
        entry_nombremed.insert(0, valores[1])
        entry_especialidadmed.insert(0, valores[2])
        entry_telefonomed.insert(0, valores[3])

# Limpia los campos de texto
def limpiar_campos_medico():
    entry_idmed.delete(0, "end")
    entry_nombremed.delete(0, "end")
    entry_especialidadmed.delete(0, "end")
    entry_telefonomed.delete(0, "end")
    
items_medicos = []

def buscar_medico():
    termino = entry_busqueda_medico.get().lower().strip()
    if not termino:
        mostrar_medico()
        return

    for item in items_medicos:
        valores = tabla_medicos.item(item, "values")
        if termino not in valores[0].lower():  # ahora busca por ID
            tabla_medicos.detach(item)
        else:
            tabla_medicos.reattach(item, '', 'end')

def mostrar_medico():
    for item in items_medicos:
        tabla_medicos.reattach(item, '', 'end')
    entry_busqueda_medico.delete(0, "end")

# Contenedor para los Labels y Entrys
frame_medico = Frame(pestana_medicos, bg = "#E3F2FD")
frame_medico.pack(expand = True)

# Título del formulario
Label(frame_medico, text = "Médicos", **label_titulo_config).grid(row = 0, column = 0, columnspan = 4, pady = 20)

# ID Médico
Label(frame_medico, text = "ID Médico", **label_config).grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 5)
entry_idmed = Entry(frame_medico, **entry_config)
entry_idmed.grid(row = 1, column = 1, padx = 10, pady = 5)

# Nombre Médico
Label(frame_medico, text = "Nombre", **label_config).grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 5)
entry_nombremed = Entry(frame_medico, **entry_config)
entry_nombremed.grid(row = 2, column = 1, padx = 10, pady = 5)

# Especialidad Médico
Label(frame_medico, text = "Especialidad", **label_config).grid(row = 1, column = 2, sticky = "e", padx = 10, pady = 5)
entry_especialidadmed = Entry(frame_medico, **entry_config)
entry_especialidadmed.grid(row = 1, column = 3, padx = 10, pady = 5)

# Teléfono Médico
Label(frame_medico, text="Teléfono", **label_config).grid(row = 2, column = 2, sticky = "e", padx = 10, pady = 5)
entry_telefonomed = Entry(frame_medico, **entry_config)
entry_telefonomed.grid(row = 2, column = 3, padx = 10, pady = 5)

# Frame que contiene los botones
botones_med_frame = Frame(frame_medico, bg = "#E3F2FD")
botones_med_frame.grid(row = 4, column = 0, columnspan = 4, pady = 20)

# Botones con su respectivo comando
Button(botones_med_frame, text = "Agregar", style = "BotonAzul.TButton", command = agregar_medico).pack(side = "left", padx=10)
Button(botones_med_frame, text = "Modificar", style = "BotonAzul.TButton", command = modificar_medico).pack(side = "left", padx=10)
Button(botones_med_frame, text = "Eliminar", style = "BotonAzul.TButton", command = eliminar_medico).pack(side = "left", padx=10)

# Frame para la búsqueda
frame_busqueda_medico = Frame(pestana_medicos, bg="#E3F2FD")
frame_busqueda_medico.pack(pady=10)

# Label + Entry
Label(frame_busqueda_medico, text="Buscar:", **label_config).pack(side="left", padx=5)
entry_busqueda_medico = Entry(frame_busqueda_medico, **entry_config)
entry_busqueda_medico.pack(side="left", padx=5)
entry_busqueda_medico.bind("<KeyRelease>", lambda event: buscar_medico())  # 🔥 Real-time search

# Creamos la tabla con cinco columnas
tabla_medicos = ttk.Treeview(pestana_medicos, columns = ("idmedico", "nombre", "especialidad", "telefono"), show = "headings")
tabla_medicos.pack(pady = 20, padx = 100, fill = BOTH, expand = True)

# Encabezados de columna
tabla_medicos.heading("idmedico", text = "ID Médico")
tabla_medicos.heading("nombre", text = "Nombre")
tabla_medicos.heading("especialidad", text = "Especialidad")
tabla_medicos.heading("telefono", text = "Teléfono")

# Centrado de columnas
tabla_medicos.column("idmedico", width = 80, anchor = "center")
tabla_medicos.column("nombre", width = 120, anchor = "center")
tabla_medicos.column("especialidad", width = 90, anchor = "center")
tabla_medicos.column("telefono", width = 130, anchor = "center")

# Evento para que se llenen los Entry al seleccionar una fila
tabla_medicos.bind("<<TreeviewSelect>>", seleccionar_fila_medico)

# ===================== PESTAÑA 5: Proveedores =====================
pestana_proveedores = Frame(notebook, bg = "#E3F2FD")
notebook.add(pestana_proveedores, text = "Proveedores")

# Funciones CRUD

# Añadir nuevo proveedor a la tabla
def agregar_proveedor():
    id_proveedor = entry_idpro.get()
    nombre_proveedor = entry_nombrepro.get() 
    telefono_proveedor = entry_telefonopro.get()
    contacto_proveedor = entry_contactopro.get()
    
    if not validar_id(id_proveedor):
        messagebox.showerror("Error", mostrar_mensaje_error("id"))
        return
    
    if not validar_nombre(nombre_proveedor):
        messagebox.showerror("Error", mostrar_mensaje_error("nombre"))
        return
    
    if not validar_telefono(telefono_proveedor):    
        messagebox.showerror("Error", mostrar_mensaje_error("telefono"))
        return
 
    if not id_proveedor or not nombre_proveedor or not telefono_proveedor or not contacto_proveedor:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Verifica si ya existe un cliente con ese ID
    for item in tabla_proveedores.get_children():
        if tabla_proveedores.item(item, "values")[0] == id_proveedor:
            messagebox.showerror("Error", "Ya existe un proveedor con ese ID.")
            return

    nuevo_item_proveedores = tabla_proveedores.insert("", "end", values=(id_proveedor, nombre_proveedor, telefono_proveedor, contacto_proveedor))
    items_proveedores.append(nuevo_item_proveedores)  # 👈 Esto es lo que faltaba
    limpiar_campos_proveedor()

# Modificar el cliente seleccionado
def modificar_proveedor():
    seleccion = tabla_proveedores.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para modificar.")
        return

    id_proveedor = entry_idpro.get()
    nombre_proveedor = entry_nombrepro.get()
    telefono_proveedor = entry_telefonopro.get()
    contacto_proveedor = entry_contactopro.get()

    if not id_proveedor or not nombre_proveedor or not telefono_proveedor or not contacto_proveedor:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    tabla_proveedores.item(seleccion, values=(id_proveedor, nombre_proveedor, telefono_proveedor, contacto_proveedor))
    limpiar_campos_proveedor()

# Eliminar el cliente seleccionado
def eliminar_proveedor():
    seleccion = tabla_proveedores.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para eliminar.")
        return

    tabla_proveedores.delete(seleccion)
    limpiar_campos_proveedor()

# Cuando seleccionas una fila de la tabla, se pasan los datos a los Entry
def seleccionar_fila_proveedor(event):
    seleccion = tabla_proveedores.selection()
    if seleccion:
        valores = tabla_proveedores.item(seleccion[0], "values")
        entry_idpro.delete(0, "end")
        entry_nombrepro.delete(0, "end")
        entry_telefonopro.delete(0, "end")
        entry_contactopro.delete(0, "end")


        entry_idpro.insert(0, valores[0])
        entry_nombrepro.insert(0, valores[1])
        entry_telefonopro.insert(0, valores[2])
        entry_contactopro.insert(0, valores[3])

# Limpia los campos de texto
def limpiar_campos_proveedor():
    entry_idpro.delete(0, "end")
    entry_nombrepro.delete(0, "end")
    entry_telefonopro.delete(0, "end")
    entry_contactopro.delete(0, "end")
    
items_proveedores = []

def buscar_proveedor():
    termino = entry_busqueda_proveedor.get().lower().strip()
    if not termino:
        mostrar_proveedor()
        return

    for item in items_proveedores:
        valores = tabla_proveedores.item(item, "values")
        if termino not in valores[0].lower():  # ahora busca por ID
            tabla_proveedores.detach(item)
        else:
            tabla_proveedores.reattach(item, '', 'end')

def mostrar_proveedor():
    for item in items_proveedores:
        tabla_proveedores.reattach(item, '', 'end')
    entry_busqueda_proveedor.delete(0, "end")

# Contenedor para los Labels y Entrys
frame_proveedor = Frame(pestana_proveedores, bg = "#E3F2FD")
frame_proveedor.pack(expand = True)

# Título del formulario
Label(frame_proveedor, text = "Proveedores", **label_titulo_config).grid(row = 0, column = 0, columnspan = 4, pady = 20)

# ID Proveedor
Label(frame_proveedor, text = "ID Proveedor", **label_config).grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 5)
entry_idpro = Entry(frame_proveedor, **entry_config)
entry_idpro.grid(row = 1, column = 1, padx = 10, pady = 5)

# Nombre Proveedor
Label(frame_proveedor, text = "Nombre", **label_config).grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 5)
entry_nombrepro = Entry(frame_proveedor, **entry_config)
entry_nombrepro.grid(row = 2, column = 1, padx = 10, pady = 5)

# Teléfono Proveedor
Label(frame_proveedor, text = "Teléfono", **label_config).grid(row = 1, column = 2, sticky = "e", padx = 10, pady = 5)
entry_telefonopro = Entry(frame_proveedor, **entry_config)
entry_telefonopro.grid(row = 1, column = 3, padx = 10, pady = 5)

# Contacto Proveedor
Label(frame_proveedor, text="Contacto", **label_config).grid(row = 2, column = 2, sticky = "e", padx = 10, pady = 5)
entry_contactopro = Entry(frame_proveedor, **entry_config)
entry_contactopro.grid(row = 2, column = 3, padx = 10, pady = 5)

# Frame que contiene los botones
botones_pro_frame = Frame(frame_proveedor, bg = "#E3F2FD")
botones_pro_frame.grid(row = 4, column = 0, columnspan = 4, pady = 20)

# Botones con su respectivo comando
Button(botones_pro_frame, text = "Agregar", style = "BotonAzul.TButton", command = agregar_proveedor).pack(side = "left", padx=10)
Button(botones_pro_frame, text = "Modificar", style = "BotonAzul.TButton", command = modificar_proveedor).pack(side = "left", padx=10)
Button(botones_pro_frame, text = "Eliminar", style = "BotonAzul.TButton", command = eliminar_proveedor).pack(side = "left", padx=10)

# Frame para la búsqueda
frame_busqueda_proveedor = Frame(pestana_proveedores, bg="#E3F2FD")
frame_busqueda_proveedor.pack(pady=10)

# Label + Entry
Label(frame_busqueda_proveedor, text="Buscar:", **label_config).pack(side="left", padx=5)
entry_busqueda_proveedor = Entry(frame_busqueda_proveedor, **entry_config)
entry_busqueda_proveedor.pack(side="left", padx=5)
entry_busqueda_proveedor.bind("<KeyRelease>", lambda event: buscar_proveedor())  # 🔥 Real-time search

# Creamos la tabla con cinco columnas
tabla_proveedores = ttk.Treeview(pestana_proveedores, columns = ("idproveedor", "nombre", "telefono", "contacto"), show = "headings")
tabla_proveedores.pack(pady = 20, padx = 100, fill = BOTH, expand = True)

# Encabezados de columna
tabla_proveedores.heading("idproveedor", text = "ID Proveedor")
tabla_proveedores.heading("nombre", text = "Nombre")
tabla_proveedores.heading("telefono", text = "Teléfono")
tabla_proveedores.heading("contacto", text = "Contacto")

# Centrado de columnas
tabla_proveedores.column("idproveedor", width = 100, anchor = "center")
tabla_proveedores.column("nombre", width = 150, anchor = "center")
tabla_proveedores.column("telefono", width = 150, anchor = "center")
tabla_proveedores.column("contacto", width = 150, anchor = "center")

# Evento para que se llenen los Entry al seleccionar una fila
tabla_proveedores.bind("<<TreeviewSelect>>", seleccionar_fila_proveedor)

# ===================== PESTAÑA 6: Unidades =====================
pestana_unidades = Frame(notebook, bg = "#E3F2FD")  # Crea una pestaña
notebook.add(pestana_unidades, text = "Unidades")  # La añade al notebook

# Funciones CRUD

# Añadir nueva categoría a la tabla
def agregar_unidad():
    id_unidad = entry_iduni.get()
    nombre_unidad = entry_nombreuni.get()
    
    # Validaciones
    
    if not validar_id(id_unidad):
        messagebox.showerror("Error", mostrar_mensaje_error("id"))
        return
    
    if not validar_nombre(nombre_unidad):
        messagebox.showerror("Error", mostrar_mensaje_error("nombre"))
        return

    if not id_unidad or not nombre_unidad:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    # Verifica si ya existe una unidad con ese ID
    for item in tabla_unidades.get_children():
        if tabla_unidades.item(item, "values")[0] == id_unidad:
            messagebox.showerror("Error", "Ya existe una categoría con ese ID.")
            return

    nuevo_item_unidades = tabla_unidades.insert("", "end", values=(id_unidad, nombre_unidad))
    items_unidades.append(nuevo_item_unidades)  # 👈 Esto es lo que faltaba
    limpiar_campos_unidad()

# Modificar la categoría seleccionada
def modificar_unidad():
    seleccion = tabla_unidades.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para modificar.")
        return

    id_unidad = entry_id.get()
    nombre_unidad = entry_nombre.get()

    if not id_unidad or not nombre_unidad:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos.")
        return

    tabla_unidades.item(seleccion, values=(id_unidad, nombre_unidad))
    limpiar_campos_unidad()

# Eliminar la categoría seleccionada
def eliminar_unidad():
    seleccion = tabla_unidades.selection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Selecciona una fila para eliminar.")
        return

    tabla_unidades.delete(seleccion)
    limpiar_campos_unidad()

# Cuando seleccionas una fila de la tabla, se pasan los datos a los Entry
def seleccionar_fila_unidad(event):
    seleccion = tabla_unidades.selection()
    if seleccion:
        valores = tabla_unidades.item(seleccion[0], "values")
        entry_iduni.delete(0, "end")
        entry_nombreuni.delete(0, "end")
        entry_iduni.insert(0, valores[0])
        entry_nombreuni.insert(0, valores[1])

# Limpia los campos de texto
def limpiar_campos_unidad():
    entry_iduni.delete(0, "end")
    entry_nombreuni.delete(0, "end")
    
items_unidades = []

def buscar_unidad():
    termino = entry_busqueda_unidad.get().lower().strip()
    if not termino:
        mostrar_unidad()
        return

    for item in items_unidades:
        valores = tabla_unidades.item(item, "values")
        if termino not in valores[0].lower():  # ahora busca por ID
            tabla_unidades.detach(item)
        else:
            tabla_unidades.reattach(item, '', 'end')

def mostrar_unidad():
    for item in items_unidades:
        tabla_unidades.reattach(item, '', 'end')
    entry_busqueda_unidad.delete(0, "end")

# Estilo de botones
style = ttk.Style()
style.theme_use("default")  # Usamos el tema base de ttk

# Estilo de la tabla
style.configure("Treeview",
    background = "white",
    foreground = "black",
    rowheight = 35,
    font = ("Arial", 13),
    fieldbackground = "white"
)
style.configure("Treeview.Heading",
    background = "#90CAF9",
    foreground = "black",
    font = ("Arial", 14, "bold")
)
style.map("Treeview", background = [("selected", "#64B5F6")])  # Color cuando seleccionas fila

# Creamos un nuevo estilo llamado "BotonAzul.TButton"
style.configure("BotonAzul.TButton",
    background = "#64B5F6",  # Color normal
    foreground = "black",
    borderwidth = 0,
    font = ("Arial", 12, "bold"),
    padding = (10, 10),
    relief = "flat"
)
style.map("BotonAzul.TButton", background = [("active", "#42A5F5")])  # Color al pasar el mouse

# Contenedor para los Labels y Entrys
frame_unidades = Frame(pestana_unidades, bg="#E3F2FD")
frame_unidades.pack(expand=True)

# Título del formulario
Label(frame_unidades, text = "Unidades", **label_titulo_config).grid(row = 0, column = 0, columnspan = 2, pady = 20)

# ID Unidad
Label(frame_unidades, text = "ID Unidad", **label_config).grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 5)
entry_iduni = Entry(frame_unidades, **entry_config)
entry_iduni.grid(row = 1, column = 1, padx = 10, pady = 5)

# Nombre Unidad
Label(frame_unidades, text = "Nombre", **label_config).grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 5)
entry_nombreuni = Entry(frame_unidades, **entry_config)
entry_nombreuni.grid(row = 2, column = 1, padx = 10, pady = 5)

# Frame que contiene los botones
botones_uni_frame = Frame(frame_unidades, bg = "#E3F2FD")
botones_uni_frame.grid(row = 3, column = 0, columnspan = 2, pady = 20)

# Botones con su respectivo comando
Button(botones_uni_frame, text = "Agregar", style = "BotonAzul.TButton", command = agregar_unidad).pack(side = "left", padx = 10)
Button(botones_uni_frame, text = "Modificar", style = "BotonAzul.TButton", command = modificar_unidad).pack(side = "left", padx = 10)
Button(botones_uni_frame, text = "Eliminar", style = "BotonAzul.TButton", command = eliminar_unidad).pack(side = "left", padx = 10)

# Frame para la búsqueda
frame_busqueda_unidad = Frame(pestana_unidades, bg="#E3F2FD")
frame_busqueda_unidad.pack(pady=10)

# Label + Entry
Label(frame_busqueda_unidad, text="Buscar:", **label_config).pack(side="left", padx=5)
entry_busqueda_unidad = Entry(frame_busqueda_unidad, **entry_config)
entry_busqueda_unidad.pack(side="left", padx=5)
entry_busqueda_unidad.bind("<KeyRelease>", lambda event: buscar_unidad())  # 🔥 Real-time search

# Creamos la tabla con dos columnas
tabla_unidades = ttk.Treeview(pestana_unidades, columns = ("idunidad", "nombre"), show="headings")
tabla_unidades.pack(pady = 20, padx = 100, fill = BOTH, expand = True)

# Encabezados de columna
tabla_unidades.heading("idunidad", text = "ID Unidad")
tabla_unidades.heading("nombre", text = "Nombre")

# Centrado de columnas
tabla_unidades.column("idunidad", anchor = "center")
tabla_unidades.column("nombre", anchor = "center")

# Evento para que se llenen los Entry al seleccionar una fila
tabla_unidades.bind("<<TreeviewSelect>>", seleccionar_fila_unidad)

# Esencial para la ejecución
ventana.mainloop()