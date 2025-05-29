from tkinter import Frame, Label, Button, NW, BOTH, messagebox, Entry
from tkinter.ttk import Treeview, Style
from tkinter import ttk
import conexion
import validaciones
from datetime import datetime

def medicamentos_app(contenido):
    # — Conexión a BD —
    conn = conexion.conectar()
    cursor = conn.cursor()
    
    # Limpiar el frame
    for widget in contenido.winfo_children():
        widget.destroy()
    
    # CRUD
    titulo = Label(contenido, text="Medicamentos", font=("Arial", 70, "bold"), bg="#FFFFFF", fg="#000000")
    titulo.pack(pady=(40, 20))

    # Función para agregar placeholder
    def agregar_placeholder(entry, texto_placeholder):
        def poner_placeholder():
            if not entry.get():
                entry.insert(0, texto_placeholder)
                entry.config(fg='grey')

        def quitar_placeholder():
            if entry.get() == texto_placeholder:
                entry.delete(0, 'end')
                entry.config(fg='#4A90E2')

        # Poner placeholder inicial
        poner_placeholder()

        def on_focus_in(event):
            quitar_placeholder()

        def on_focus_out(event):
            poner_placeholder()

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    # Función de búsqueda mejorada
    def buscar(event=None):
        texto = entry_busq.get().strip().lower()
        if texto == "" or texto == "buscar":
            mostrar_todos()
            return
        for it in items:
            vals = tbl.item(it, "values")
            if texto not in str(vals[0]).lower() and texto not in str(vals[1]).lower():
                tbl.detach(it)
            else:
                tbl.reattach(it, '', 'end')

    # Función para mostrar todos los registros (quita filtros)
    def mostrar_todos(event=None):
        for it in items:
            tbl.reattach(it, '', 'end')
        entry_busq.delete(0, "end")
        agregar_placeholder(entry_busq, "Buscar")

    # Frame de búsqueda y botones
    frm_botones_buscar = Frame(contenido, bg="#FFFFFF")
    frm_botones_buscar.pack(pady=10, fill="x", padx=80)

    btn_agregar = Button(
        frm_botones_buscar,
        text="Agregar",
        bg="#5D85AC",
        fg="#5D85AC",
        activebackground="#5D85AC",
        activeforeground="white",
        highlightbackground="white",
        highlightcolor="white",
        highlightthickness=2,
        bd=0,
        relief="flat",
    )
    btn_agregar.pack(side="left", padx=5)  # Espacio entre botones

    btn_modificar = Button(
        frm_botones_buscar,
        text="Modificar",
        bg="#5D85AC",
        fg="#5D85AC",
        activebackground="#5D85AC",
        activeforeground="white",
        highlightbackground="white",
        highlightcolor="white",
        highlightthickness=2,
        bd=0,
        relief="flat",
    )
    btn_modificar.pack(side="left", padx=5)

    btn_eliminar = Button(
        frm_botones_buscar,
        text="Eliminar",
        bg="#5D85AC",
        fg="#5D85AC",
        activebackground="#5D85AC",
        activeforeground="white",
        highlightbackground="white",
        highlightcolor="white",
        highlightthickness=2,
        bd=0,
        relief="flat",
    )
    btn_eliminar.pack(side="left", padx=5)

    entry_busq = Entry(
        frm_botones_buscar, 
        width=30, 
        bg="white", 
        fg="#4A90E2",
        highlightbackground="#4A90E2",
        highlightcolor="#4A90E2",
        highlightthickness=2,
        bd=0,
        relief="flat",
    )
    entry_busq.pack(side="right", padx=5)
    agregar_placeholder(entry_busq, "Buscar")
    entry_busq.bind("<KeyRelease>", buscar)

    # Frame de la tabla
    frm_tabla = Frame(contenido)
    frm_tabla.pack(fill=BOTH, expand=True, padx=80, pady=(0,40))

    style = Style()
    style.theme_use("default")  # Usar tema "default" para poder personalizar mejor

    # Configurar colores para Treeview (tabla)
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    fieldbackground="white",
                    rowheight=25,
                    font=("Arial", 11))

    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    background="#f0f0f0",
                    foreground="black")
    
    style.map('Treeview',
            background=[('selected', '#3874f2')],
            foreground=[('selected', 'white')])

    tbl = Treeview(frm_tabla, columns=("codigo", "nombre", "precio", "costo", "existencias", "fecha_caducidad", "idcategoria", "idproveedor", "idunidad"), show="headings")
    tbl.heading("codigo", text="Código")
    tbl.heading("nombre", text="Nombre")
    tbl.heading("precio", text="Precio")
    tbl.heading("costo", text="Costo")
    tbl.heading("existencias", text="Existencias")
    tbl.heading("fecha_caducidad", text="Fecha Caducidad")
    tbl.heading("idcategoria", text="ID Categoría")
    tbl.heading("idproveedor", text="ID Proveedor")
    tbl.heading("idunidad", text="ID Unidad")
    tbl.column("codigo", width=100, anchor="center")
    tbl.column("nombre", width=200, anchor="center")
    tbl.column("precio", width=100, anchor="center")
    tbl.column("costo", width=100, anchor="center")
    tbl.column("existencias", width=100, anchor="center")
    tbl.column("fecha_caducidad", width=150, anchor="center")
    tbl.column("idcategoria", width=100, anchor="center")
    tbl.column("idproveedor", width=100, anchor="center")
    tbl.column("idunidad", width=100, anchor="center")
    tbl.pack(fill=BOTH, expand=True)
    
    def refrescar():
        nonlocal items
        for row in tbl.get_children():
            tbl.delete(row)
        cursor.execute("SELECT codigo, nombre, precio, costo, existencias, fecha_caducidad, id_categoria, id_proveedor, id_unidad FROM medicamentos")
        for r in cursor.fetchall():
            tbl.insert("", "end", values=r)
        items = tbl.get_children()
        
    refrescar()
    
    def validar_campos(cod, nom, pre, cos, exi, fec):
        if not validaciones.validar_codigo(cod):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("codigo"))
            return False
        if not validaciones.validar_nombre(nom):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("nombre"))
            return False
        if not validaciones.validar_precio(pre):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("precio"))
            return False
        if not validaciones.validar_costo(cos):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("costo"))
            return False
        if not validaciones.validar_existencias(exi):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("existencias"))
            return False
        if not validaciones.validar_fecha(fec):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("fecha"))
            return False
        return True

    def agregar():
        # Obtener listas para los combobox
        def obtener_datos(tabla, id_col, nombre_col):
            cursor.execute(f"SELECT {id_col}, {nombre_col} FROM {tabla}")
            return cursor.fetchall()  # Lista de tuplas: [(1, "Nombre1"), (2, "Nombre2"), ...]
        
        # Obtener los datos para combobox
        categorias = obtener_datos("categorias", "id_categoria", "nombre")
        proveedores = obtener_datos("proveedores", "id_proveedor", "nombre")
        unidades = obtener_datos("unidades", "id_unidad", "nombre")
        
        # Crear un frame modal (capa encima)
        modal_frame = Frame(contenido, bg="#FFFFFF", bd=2, relief="ridge")
        modal_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=500)

        Label(modal_frame, text="Agregar Medicamento", font=("Arial", 20), fg="#000000", bg="#FFFFFF").pack(pady=10)

        # Contenedor con grid para organizar los entrys
        form_frame = Frame(modal_frame, bg="#FFFFFF")
        form_frame.pack(pady=10)

        # Lado izquierdo
        Label(form_frame, text="Código", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_cod = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_cod.grid(row=1, column=0, padx=10, pady=5)
        entry_cod.focus()

        Label(form_frame, text="Nombre", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_nombre = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_nombre.grid(row=3, column=0, padx=10, pady=5)

        Label(form_frame, text="Precio", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        entry_precio = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_precio.grid(row=5, column=0, padx=10, pady=5)
        
        Label(form_frame, text="Costo", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        entry_costo = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_costo.grid(row=7, column=0, padx=10, pady=5)
        
        Label(form_frame, text="Existencias", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        entry_existencias = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_existencias.grid(row=9, column=0, padx=10, pady=5)

        # Lado derecho
        Label(form_frame, text="Fecha de Caducidad", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        entry_fecha = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_fecha.grid(row=1, column=1, padx=10, pady=5)
        
        Label(form_frame, text="Categoría", font=("Arial", 12), bg="#FFFFFF", fg="#000000").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        combo_categoria = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_categoria['values'] = [f"{id} - {nombre}" for id, nombre in categorias]
        combo_categoria.grid(row=3, column=1, padx=10, pady=5)
        
        Label(form_frame, text="Proveedor", font=("Arial", 12), bg="#FFFFFF", fg="#000000").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        combo_proveedor = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_proveedor['values'] = [f"{id} - {nombre}" for id, nombre in proveedores]
        combo_proveedor.grid(row=5, column=1, padx=10, pady=5)

        Label(form_frame, text="Unidad", font=("Arial", 12), bg="#FFFFFF", fg="#000000").grid(row=6, column=1, padx=10, pady=5, sticky="w")
        combo_unidad = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_unidad['values'] = [f"{id} - {nombre}" for id, nombre in unidades]
        combo_unidad.grid(row=7, column=1, padx=10, pady=5)

        lbl_error = Label(modal_frame, text="", fg="red", font=("Arial", 10), bg="#FFFFFF")
        lbl_error.pack(pady=5)
        
        # Función para guardar
        def guardar():
            cod = entry_cod.get().strip()
            nom = entry_nombre.get().strip()
            pre = entry_precio.get().strip()
            cos = entry_costo.get().strip()
            exi = entry_existencias.get().strip()
            fec = entry_fecha.get().strip()
            idc = combo_categoria.get().split(" - ")[0]
            idp = combo_proveedor.get().split(" - ")[0]
            idu = combo_unidad.get().split(" - ")[0]
            
            if not validar_campos(cod, nom, pre, cos, exi, fec): 
                lbl_error.config(text="Error en los datos ingresados.")
                return
            
            # Convertir fecha a ISO
            fecha_sql = datetime.strptime(fec, "%d/%m/%Y").strftime("%Y-%m-%d")
            
            try:
                cursor.execute("INSERT INTO medicamentos (codigo, nombre, precio, costo, existencias, fecha_caducidad, id_categoria, id_proveedor, id_unidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (cod, nom, pre, cos, exi, fecha_sql, idc, idp, idu))
                conn.commit()
                refrescar()
                messagebox.showinfo("Éxito", "Medicamento agregado correctamente")
                modal_frame.destroy()
            except Exception as e:
                lbl_error.config(text=f"Error: {str(e)}")
            
        # Función para cancelar
        def cancelar():
            modal_frame.destroy()

        # Botones del modal
        btn_frame = Frame(modal_frame, bg="white")
        btn_frame.pack(pady=10)

        btn_guardar = Button(
            btn_frame, 
            text="Guardar", 
            command=guardar, 
            bg="#5D85AC", 
            fg="#5D85AC", 
            width=12, 
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="#5D85AC",
            highlightthickness=2,
            bd=0,
            relief="flat"
        )
        btn_guardar.pack(side="left", padx=5)

        btn_cancelar = Button(
            btn_frame, 
            text="Cancelar", 
            command=cancelar, 
            bg="red", 
            fg="red", 
            width=12, 
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="#5D85AC",
            highlightthickness=2,
            bd=0,
            relief="flat"
        )
        btn_cancelar.pack(side="left", padx=5)

    btn_agregar.config(command=agregar)
    
    def modificar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona primero una fila.")
            return

        # Obtener valores de la fila seleccionada
        codigo, nombre, precio, costo, existencias, fecha_caducidad, id_categoria, id_proveedor, id_unidad = tbl.item(sel[0], "values")
        
        # Obtener listas para los combobox
        def obtener_datos(tabla, id_col, nombre_col):
            cursor.execute(f"SELECT {id_col}, {nombre_col} FROM {tabla}")
            return cursor.fetchall()  # Lista de tuplas: [(1, "Nombre1"), (2, "Nombre2"), ...]
        
        # Obtener los datos para combobox
        categorias = obtener_datos("categorias", "id_categoria", "nombre")
        proveedores = obtener_datos("proveedores", "id_proveedor", "nombre")
        unidades = obtener_datos("unidades", "id_unidad", "nombre")
        
        # Crear un frame modal (capa encima)
        modal_frame = Frame(contenido, bg="#FFFFFF", bd=2, relief="ridge")
        modal_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=500)

        Label(modal_frame, text="Modificar Medicamento", font=("Arial", 20), fg="#000000", bg="#FFFFFF").pack(pady=10)

        # Contenedor con grid para organizar los entrys
        form_frame = Frame(modal_frame, bg="#FFFFFF")
        form_frame.pack(pady=10)

        # Lado izquierdo
        Label(form_frame, text="Código", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_cod = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#FFFFFF")
        entry_cod.grid(row=1, column=0, padx=10, pady=5)
        entry_cod.focus()
        entry_cod.insert(0, codigo)
        entry_cod.config(state='readonly')

        Label(form_frame, text="Nombre", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_nombre = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_nombre.grid(row=3, column=0, padx=10, pady=5)
        entry_nombre.insert(0, nombre)

        Label(form_frame, text="Precio", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        entry_precio = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_precio.grid(row=5, column=0, padx=10, pady=5)
        entry_precio.insert(0, precio)
        
        Label(form_frame, text="Costo", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        entry_costo = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_costo.grid(row=7, column=0, padx=10, pady=5)
        entry_costo.insert(0, costo)
        
        Label(form_frame, text="Existencias", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        entry_existencias = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_existencias.grid(row=9, column=0, padx=10, pady=5)
        entry_existencias.insert(0, existencias)

        # Lado derecho
        Label(form_frame, text="Fecha de Caducidad", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        entry_fecha = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_fecha.grid(row=1, column=1, padx=10, pady=5)
        entry_fecha.insert(0, fecha_caducidad)
        
        Label(form_frame, text="Categoría", font=("Arial", 12), bg="#FFFFFF", fg="#000000").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        combo_categoria = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_categoria['values'] = [f"{id} - {nombre}" for id, nombre in categorias]
        combo_categoria.grid(row=3, column=1, padx=10, pady=5)
        
        Label(form_frame, text="Proveedor", font=("Arial", 12), bg="#FFFFFF", fg="#000000").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        combo_proveedor = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_proveedor['values'] = [f"{id} - {nombre}" for id, nombre in proveedores]
        combo_proveedor.grid(row=5, column=1, padx=10, pady=5)

        Label(form_frame, text="Unidad", font=("Arial", 12), bg="#FFFFFF", fg="#000000").grid(row=6, column=1, padx=10, pady=5, sticky="w")
        combo_unidad = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_unidad['values'] = [f"{id} - {nombre}" for id, nombre in unidades]
        combo_unidad.grid(row=7, column=1, padx=10, pady=5)

        lbl_error = Label(modal_frame, text="", fg="red", font=("Arial", 10), bg="#FFFFFF")
        lbl_error.pack(pady=5)

        # Función para guardar los cambios
        def guardar_cambios():
            nuevo_codigo = entry_cod.get().strip()
            nuevo_nombre = entry_nombre.get().strip()
            nuevo_precio = entry_precio.get().strip()
            nuevo_costo = entry_costo.get().strip()
            nueva_fecha = entry_fecha.get().strip()
            nuevo_existencias = entry_existencias.get().strip()
            nuevo_categoria = combo_categoria.get().split(" - ")[0]
            nuevo_proveedor = combo_proveedor.get().split(" - ")[0]
            nuevo_unidad = combo_unidad.get().split(" - ")[0]
            
            if nuevo_nombre == "":
                lbl_error.config(text="El nombre no puede estar vacío")
                return
            
            try:
                cursor.execute(
                    "UPDATE medicamentos SET nombre=%s, precio=%s, costo=%s, existencias=%s, fecha_caducidad=%s, id_categoria=%s, id_proveedor=%s, id_unidad=%s WHERE codigo=%s",
                    (nuevo_nombre, nuevo_precio, nuevo_costo, nuevo_existencias, nueva_fecha, nuevo_categoria, nuevo_proveedor, nuevo_unidad, nuevo_codigo)
                )
                conn.commit()
                refrescar()
                modal_frame.destroy()
                messagebox.showinfo("Éxito", "Medicamento modificado correctamente")
            except Exception as e:
                lbl_error.config(text=f"Error: {str(e)}")

        # Función para cancelar la modificación
        def cancelar():
            modal_frame.destroy()

        # Botones del modal
        btn_frame = Frame(modal_frame, bg="white")
        btn_frame.pack(pady=10)

        btn_guardar = Button(
            btn_frame, 
            text="Guardar", 
            command=guardar_cambios, 
            bg="white", 
            fg="#5D85AC", 
            width=12, 
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="#5D85AC",
            highlightthickness=2,
            bd=0,
            relief="flat"
        )
        btn_guardar.pack(side="left", padx=5)

        btn_cancelar = Button(
            btn_frame, 
            text="Cancelar", 
            command=cancelar, 
            bg="white", 
            fg="red", 
            width=12, 
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="#5D85AC",
            highlightthickness=2,
            bd=0,
            relief="flat"
        )
        btn_cancelar.pack(side="left", padx=5)
    
    # Función para modificar
    btn_modificar.config(command=modificar)
    
    def eliminar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona primero una fila.")
            return
        cod = tbl.item(sel[0], "values")[0]

        # Crear un frame modal (capa encima)
        modal_frame = Frame(contenido, bg="#FFFFFF", bd=2, relief="ridge")
        modal_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=250)

        # Contenedor interno para centrar el contenido
        inner_frame = Frame(modal_frame, bg="#FFFFFF")
        inner_frame.pack(expand=True)

        Label(inner_frame, text="Eliminar Medicamento", font=("Arial", 25), fg="#000000", bg="#FFFFFF").pack(pady=10)
        Label(inner_frame, text=f"¿Deseas eliminar Medicamento {cod}?", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)

        # Función que realmente elimina el registro
        def confirmar_eliminacion():
            cursor.execute("DELETE FROM medicamentos WHERE codigo=%s", (cod,))
            conn.commit()
            refrescar()
            modal_frame.destroy()  # Cierra el modal después de eliminar

        # Contenedor para los botones centrados
        btn_frame = Frame(inner_frame, bg="#FFFFFF")
        btn_frame.pack(pady=15)

        # Botones para confirmar o cancelar
        btn_eliminar = Button(
            btn_frame, 
            text="Eliminar", 
            command=confirmar_eliminacion,  
            bg="white", 
            fg="red", 
            width=12, 
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="#5D85AC",
            highlightthickness=2,
            bd=0,
            relief="flat"
        )
        btn_eliminar.pack(side="left", padx=10)

        btn_cancelar = Button(
            btn_frame, 
            text="Cancelar", 
            command=modal_frame.destroy, 
            bg="white", 
            fg="black", 
            width=12, 
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="#5D85AC",
            highlightthickness=2,
            bd=0,
            relief="flat"
        )
        btn_cancelar.pack(side="right", padx=10)
            
    btn_eliminar.config(command=eliminar)

    # Guardar IDs de items para control de búsqueda
    items = tbl.get_children()