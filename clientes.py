from tkinter import Frame, Label, Button, NW, BOTH, messagebox, Entry
from tkinter.ttk import Treeview, Style
import conexion
import validaciones

def clientes_app(contenido):
    # — Conexión a BD —
    conn = conexion.conectar()
    cursor = conn.cursor()
    
    # Limpiar el frame
    for widget in contenido.winfo_children():
        widget.destroy()

    # CRUD
    titulo = Label(contenido, text="Clientes", font=("Arial", 70, "bold"), bg="#FFFFFF", fg="#000000")
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
    style.theme_use("default")  # Tema "default" para poder personalizar mejor

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

    tbl = Treeview(frm_tabla, columns=("id", "nombre", "telefono", "direccion", "correo"), show="headings")
    tbl.heading("id", text="ID Categoría")
    tbl.heading("nombre", text="Nombre")
    tbl.heading("telefono", text="Teléfono")
    tbl.heading("direccion", text="Dirección")
    tbl.heading("correo", text="Correo")
    tbl.column("id", width=100, anchor="center")
    tbl.column("nombre", width=200, anchor="center")
    tbl.column("telefono", width=100, anchor="center")
    tbl.column("direccion", width=200, anchor="center")
    tbl.column("correo", width=100, anchor="center")
    tbl.pack(fill=BOTH, expand=True)
    
    def refrescar():
        nonlocal items
        for row in tbl.get_children():
            tbl.delete(row)
        cursor.execute("SELECT id_cliente, nombre, telefono, direccion, correo FROM clientes")
        for r in cursor.fetchall():
            tbl.insert("", "end", values=r)
        items = tbl.get_children()
        
    refrescar()
    
    def validar_campos(idc, nom, tel, dir, cor):
        if not validaciones.validar_id(idc):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("id"))
            return False
        if not validaciones.validar_nombre(nom):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("nombre"))
            return False
        if not validaciones.validar_telefono(tel):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("telefono"))
            return False
        if not validaciones.validar_direccion(dir):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("direccion"))
            return False
        if not validaciones.validar_correo(cor):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("correo"))
            return False
        return True

    def agregar():
        # Crear un frame modal (capa encima)
        modal_frame = Frame(contenido, bg="#FFFFFF", bd=2, relief="ridge")
        modal_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=450)

        Label(modal_frame, text="Agregar cliente", font=("Arial", 20), fg="#000000", bg="#FFFFFF").pack(pady=5)
        
        Label(modal_frame, text="ID Cliente", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_id = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_id.pack(pady=5)
        entry_id.focus()
        
        Label(modal_frame, text="Nombre de cliente", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_nombre = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_nombre.pack(pady=5)
        
        Label(modal_frame, text="Teléfono", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_telefono = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_telefono.pack(pady=5)
        
        Label(modal_frame, text="Dirección", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_direccion = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_direccion.pack(pady=5)
        
        Label(modal_frame, text="Correo", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_correo = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_correo.pack(pady=5)

        lbl_error = Label(modal_frame, text="", fg="red", font=("Arial", 10), bg="#FFFFFF")
        lbl_error.pack()

        # Función para guardar
        def guardar():
            idc = entry_id.get().strip()
            nom = entry_nombre.get().strip()
            tel = entry_telefono.get().strip()
            dir = entry_direccion.get().strip()
            cor = entry_correo.get().strip()
            
            if not validar_campos(idc, nom, tel, dir, cor): 
                lbl_error.config(text="Error en los datos ingresados.")
                return
            
            try:
                cursor.execute("INSERT INTO clientes(id_cliente, nombre, telefono, direccion, correo) VALUES(%s, %s, %s, %s, %s)", (idc, nom, tel, dir, cor))
                conn.commit()
                refrescar()
                messagebox.showinfo("Éxito", "Cliente agregado correctamente")
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
        id_cliente, nombre_cliente, telefono_cliente, direccion_cliente, correo_cliente = tbl.item(sel[0], "values")

        # Crear un frame modal (capa encima)
        modal_frame = Frame(contenido, bg="#FFFFFF", bd=2, relief="ridge")
        modal_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=450)

        Label(modal_frame, text="Modificar cliente", font=("Arial", 25), fg="#000000", bg="#FFFFFF").pack(pady=5)
        Label(modal_frame, text="ID Cliente", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)

        entry_id = Entry(modal_frame, font=("Arial", 12), width=20, fg="#FFFFFF", bg="#000000")
        entry_id.pack(pady=5)
        entry_id.insert(0, id_cliente)
        entry_id.config(state='readonly')  # ID es solo lectura

        Label(modal_frame, text="Nombre de cliente", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_nombre = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_nombre.pack(pady=5)
        entry_nombre.insert(0, nombre_cliente)
        entry_nombre.focus()
        
        Label(modal_frame, text="Teléfono", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_telefono = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_telefono.pack(pady=5)
        entry_telefono.insert(0, telefono_cliente)
        entry_telefono.focus()
        
        Label(modal_frame, text="Dirección", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_direccion = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_direccion.pack(pady=5)
        entry_direccion.insert(0, direccion_cliente)
        entry_direccion.focus()
        
        Label(modal_frame, text="Correo", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)
        entry_correo = Entry(modal_frame, font=("Arial", 12), width=20, fg="#000000", bg="#FFFFFF")
        entry_correo.pack(pady=5)
        entry_correo.insert(0, correo_cliente)
        entry_correo.focus()

        lbl_error = Label(modal_frame, text="", fg="red", font=("Arial", 10), bg="#FFFFFF")
        lbl_error.pack()

        # Función para guardar los cambios
        def guardar_cambios():
            nuevo_nombre = entry_nombre.get().strip()
            nuevo_telefono = entry_telefono.get().strip()
            nueva_direccion = entry_direccion.get().strip()
            nuevo_correo = entry_correo.get().strip()
            
            if nuevo_nombre == "":
                lbl_error.config(text="El nombre no puede estar vacío")
                return
            
            try:
                cursor.execute(
                    "UPDATE clientes SET nombre=%s, telefono=%s, direccion=%s, correo=%s WHERE id_cliente=%s",
                    (nuevo_nombre, nuevo_telefono, nueva_direccion, nuevo_correo, id_cliente)
                )
                conn.commit()
                refrescar()
                modal_frame.destroy()
                messagebox.showinfo("Éxito", "Cliente modificado correctamente")
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

        Label(inner_frame, text="Eliminar Cliente", font=("Arial", 25), fg="#000000", bg="#FFFFFF").pack(pady=10)
        Label(inner_frame, text=f"¿Deseas eliminar Cliente {idc}?", font=("Arial", 12), fg="#000000", bg="#FFFFFF").pack(pady=5)

        # Función que confirma la eliminación del registro
        def confirmar_eliminacion():
            cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (idc,))
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