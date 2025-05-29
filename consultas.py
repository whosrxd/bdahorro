from tkinter import Frame, Label, Button, NW, BOTH, messagebox, Entry
from tkinter.ttk import Treeview, Style
from tkinter import ttk
import conexion
import validaciones
from datetime import datetime

def consultas_app(contenido):
    # — Conexión a BD —
    conn = conexion.conectar()
    cursor = conn.cursor()
    
    # Limpiar el frame
    for widget in contenido.winfo_children():
        widget.destroy()
    
    # CRUD
    titulo = Label(contenido, text="Consultas", font=("Arial", 70, "bold"), bg="#FFFFFF", fg="#000000")
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
                entry.config(fg='#4A90E2')  # azul clarito al escribir

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

    tbl = Treeview(frm_tabla, columns=("id_consulta", "id_cliente", "id_empleado", "id_receta", "fecha", "motivo"), show="headings")
    tbl.heading("id_consulta", text="ID Consulta")
    tbl.heading("id_cliente", text="ID Cliente")
    tbl.heading("id_empleado", text="ID Empleado")
    tbl.heading("id_receta", text="ID Receta")
    tbl.heading("fecha", text="Fecha")
    tbl.heading("motivo", text="Motivo")
    tbl.column("id_consulta", width=90, anchor="center")
    tbl.column("id_cliente", width=90, anchor="center")
    tbl.column("id_empleado", width=90, anchor="center")
    tbl.column("id_receta", width=90, anchor="center")
    tbl.column("fecha", width=100, anchor="center")
    tbl.column("motivo", width=160, anchor="center")
    tbl.pack(fill=BOTH, expand=True)
    
    def refrescar():
        nonlocal items
        for row in tbl.get_children():
            tbl.delete(row)
        cursor.execute("SELECT id_consulta, id_cliente, id_empleado, id_receta, fecha, motivo FROM consultas")
        for r in cursor.fetchall():
            tbl.insert("", "end", values=r)
        items = tbl.get_children()
        
    refrescar()
    
    def validar_campos(idc, fec, mot):
        if not validaciones.validar_id(idc):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("id"))
            return False
        if not validaciones.validar_fecha(fec):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("fecha"))
            return False
        if not validaciones.validar_motivo(mot):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("motivo"))
            return False
        return True

    def agregar():
        # Obtener listas para los combobox
        def obtener_datos(tabla, id_col, nombre_col):
            cursor.execute(f"SELECT {id_col}, {nombre_col} FROM {tabla}")
            return cursor.fetchall()  # Lista de tuplas: [(1, "Nombre1"), (2, "Nombre2"), ...]
        
        # Obtener los datos para combobox
        clientes = obtener_datos("clientes", "id_cliente", "nombre")
        empleados = obtener_datos("empleados", "id_empleado", "nombre")
        recetas = obtener_datos("recetas", "id_receta", "fecha")
        
        # Crear un frame modal (capa encima)
        modal_frame = Frame(contenido, bg="#FFFFFF", bd=2, relief="ridge")
        modal_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=350)

        Label(modal_frame, text="Agregar Consulta", font=("Arial", 20), fg="#000000", bg="#FFFFFF").pack(pady=10)

        # Contenedor con grid para organizar los entrys
        form_frame = Frame(modal_frame, bg="#FFFFFF")
        form_frame.pack(pady=10)

        # Lado izquierdo
        Label(form_frame, text="ID Consulta", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_id = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_id.grid(row=1, column=0, padx=10, pady=5)
        entry_id.focus()

        Label(form_frame, text="ID Cliente", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        combo_cliente = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_cliente['values'] = [f"{id} - {nombre}" for id, nombre in clientes]
        combo_cliente.grid(row=3, column=0, padx=10, pady=5)
        
        Label(form_frame, text="ID Empleado", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        combo_empleado = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_empleado['values'] = [f"{id} - {nombre}" for id, nombre in empleados]
        combo_empleado.grid(row=5, column=0, padx=10, pady=5)
        
        # Lado derecho
        Label(form_frame, text="ID Receta", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        combo_receta = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_receta['values'] = [f"{id} - {nombre}" for id, nombre in recetas]
        combo_receta.grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Fecha", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        entry_fecha = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_fecha.grid(row=3, column=1, padx=10, pady=5)

        Label(form_frame, text="Motivo", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        entry_motivo = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_motivo.grid(row=5, column=1, padx=10, pady=5)

        lbl_error = Label(modal_frame, text="", fg="red", font=("Arial", 10), bg="#FFFFFF")
        lbl_error.pack(pady=5)

        # Función para guardar
        def guardar():
            idc = entry_id.get().strip()
            idcl = combo_cliente.get().split(" - ")[0]
            ide = combo_empleado.get().split(" - ")[0]
            idr = combo_receta.get().split(" - ")[0]
            fec = entry_fecha.get().strip()
            mot = entry_motivo.get().strip()
            
            if not validar_campos(idc, fec, mot): 
                lbl_error.config(text="Error en los datos ingresados.")
                return
            
            # Convertir fecha a ISO
            fecha_sql = datetime.strptime(fec, "%d/%m/%Y").strftime("%Y-%m-%d")
            
            try:
                cursor.execute("INSERT INTO consultas (id_consulta, id_cliente, id_empleado, id_receta, fecha, motivo) VALUES (%s, %s, %s, %s, %s, %s)", (idc, idcl, ide, idr, fecha_sql, mot))
                conn.commit()
                refrescar()
                messagebox.showinfo("Éxito", "Consulta agregada correctamente")
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
        id_consulta, id_cliente, id_empleado, id_receta, fecha, motivo = tbl.item(sel[0], "values")
        
        # Obtener listas para los combobox
        def obtener_datos(tabla, id_col, nombre_col):
            cursor.execute(f"SELECT {id_col}, {nombre_col} FROM {tabla}")
            return cursor.fetchall()  # Lista de tuplas: [(1, "Nombre1"), (2, "Nombre2"), ...]
        
        # Obtener los datos para combobox
        clientes = obtener_datos("clientes", "id_cliente", "nombre")
        empleados = obtener_datos("empleados", "id_empleado", "nombre")
        recetas = obtener_datos("empleados", "id_empleado", "nombre")

        # Crear un frame modal (capa encima)
        modal_frame = Frame(contenido, bg="#FFFFFF", bd=2, relief="ridge")
        modal_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=350)

        Label(modal_frame, text="Modificar Consulta", font=("Arial", 25), fg="#000000", bg="#FFFFFF").pack(pady=5)

        # Frame interno con grid
        form_frame = Frame(modal_frame, bg="#FFFFFF")
        form_frame.pack(pady=5)

        # Lado izquierdo
        Label(form_frame, text="ID Consulta", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_id = Entry(form_frame, font=("Arial", 12), width=20, bg="#000000", fg = "#FFFFFF")
        entry_id.grid(row=1, column=0, padx=10, pady=5)
        entry_id.insert(0, id_consulta)
        entry_id.config(state="readonly")

        Label(form_frame, text="ID Cliente", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        combo_cliente = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_cliente['values'] = [f"{id} - {nombre}" for id, nombre in clientes]
        combo_cliente.grid(row=3, column=0, padx=10, pady=5)
        
        Label(form_frame, text="ID Empleado", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        combo_empleado = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_empleado['values'] = [f"{id} - {nombre}" for id, nombre in empleados]
        combo_empleado.grid(row=5, column=0, padx=10, pady=5)
        
        # Lado derecho
        Label(form_frame, text="ID Receta", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        combo_receta = ttk.Combobox(form_frame, font=("Arial", 12), width=20, state="readonly")
        combo_receta['values'] = [f"{id} - {nombre}" for id, nombre in recetas]
        combo_receta.grid(row=1, column=1, padx=10, pady=5)

        Label(form_frame, text="Fecha", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        entry_fecha = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_fecha.grid(row=3, column=1, padx=10, pady=5)
        entry_fecha.insert(0, fecha)

        Label(form_frame, text="Motivo", font=("Arial", 12), bg="#FFFFFF", fg = "#000000").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        entry_motivo = Entry(form_frame, font=("Arial", 12), width=20, bg="#FFFFFF", fg = "#000000")
        entry_motivo.grid(row=5, column=1, padx=10, pady=5)
        entry_motivo.insert(0, motivo)

        lbl_error = Label(modal_frame, text="", fg="red", font=("Arial", 10), bg="#FFFFFF")
        lbl_error.pack(pady=5)

        # Función para guardar los cambios
        def guardar_cambios():
            nuevo_id = entry_id.get().strip()
            nuevo_cliente = combo_cliente.get().split(" - ")[0]
            nuevo_empleado = combo_empleado.get().split(" - ")[0]
            nueva_receta = combo_receta.get().split(" - ")[0]
            nuevo_motivo = entry_motivo.get().strip()
            nueva_fecha = entry_fecha.get().strip()
            
            try:
                cursor.execute(
                    "UPDATE consultas SET id_cliente=%s, id_empleado=%s, id_receta=%s, motivo=%s, fecha=%s WHERE id_consulta=%s",
                    (nuevo_cliente, nuevo_empleado, nueva_receta, nuevo_motivo, nueva_fecha, nuevo_id)
                )
                conn.commit()
                refrescar()
                modal_frame.destroy()
                messagebox.showinfo("Éxito", "Consulta modificada correctamente")
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
        idc = tbl.item(sel[0], "values")[0]

        # Crear un frame modal (capa encima)
        modal_frame = Frame(contenido, bg="#FFFFFF", bd=2, relief="ridge")
        modal_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=250)

        # Contenedor interno para centrar el contenido
        inner_frame = Frame(modal_frame, bg="#FFFFFF")
        inner_frame.pack(expand=True)

        Label(inner_frame, text="Eliminar Consulta", font=("Arial", 25), fg="#000000", bg="#FFFFFF").pack(pady=10)
        Label(inner_frame, text=f"¿Deseas eliminar Consulta {idc}?", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)

        # Función que realmente elimina el registro
        def confirmar_eliminacion():
            cursor.execute("DELETE FROM consultas WHERE id_consulta=%s", (idc,))
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