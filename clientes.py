# clientes.py
from tkinter import Tk, Label, Entry, Frame, BOTH, messagebox
from tkinter.ttk import Button, Notebook, Style, Treeview
import conexion
import validaciones

def clientes_app():
    # — Conexión a BD —
    conn   = conexion.conectar()
    cursor = conn.cursor()

    # — Ventana principal fullscreen —
    ventana = Tk()
    ventana.title("Gestión de Clientes")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg="#E3F2FD")

    # — Notebook por si añades más módulos después —
    notebook = Notebook(ventana)
    notebook.pack(fill=BOTH, expand=True)

    # — Pestaña Clientes —
    pestaña = Frame(notebook, bg="#E3F2FD")
    notebook.add(pestaña, text="Clientes")

    # — Estilos globales —
    style = Style()
    style.theme_use("default")
    style.configure("BotonAzul.TButton",
                    background="#64B5F6", foreground="black",
                    font=("Arial",12,"bold"), padding=(10,8))
    style.map("BotonAzul.TButton", background=[("active", "#42A5F5")])
    style.configure("Treeview",
                    background="white", fieldbackground="white",
                    foreground="black", rowheight=30,
                    font=("Arial",12))
    style.configure("Treeview.Heading",
                    background="#90CAF9", foreground="black",
                    font=("Arial",12,"bold"))

    # — Configuración de Labels y Entries —
    label_cfg  = {"bg": "#E3F2FD", "fg": "black", "font": ("Arial",14)}
    title_cfg  = {"bg": "#E3F2FD", "fg": "black", "font": ("Arial",18,"bold")}
    entry_cfg  = {"bg": "#BBDEFB", "fg": "black", "relief": "flat", "bd": 0,
                  "font": ("Arial",14), "width": 20}

    # — Frame del formulario —
    frm = Frame(pestaña, bg="#E3F2FD")
    frm.pack(pady=30)

    # Título
    Label(frm, text="Cliente", **title_cfg).grid(row=0, column=0, columnspan=4, pady=(0,20))

    # Entrys
    entry_tel    = Entry(frm, **entry_cfg)
    entry_nom    = Entry(frm, **entry_cfg)
    entry_id     = Entry(frm, **entry_cfg)
    entry_dir    = Entry(frm, **entry_cfg)
    entry_correo = Entry(frm, **entry_cfg)

    # Etiquetas + grid
    Label(frm, text="Teléfono", **label_cfg).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_tel.grid(row=1, column=1, padx=10, pady=5)
    Label(frm, text="Nombre", **label_cfg).grid(row=1, column=2, sticky="e", padx=10, pady=5)
    entry_nom.grid(row=1, column=3, padx=10, pady=5)

    Label(frm, text="ID Cliente", **label_cfg).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_id.grid(row=2, column=1, padx=10, pady=5)
    Label(frm, text="Dirección", **label_cfg).grid(row=2, column=2, sticky="e", padx=10, pady=5)
    entry_dir.grid(row=2, column=3, padx=10, pady=5)

    Label(frm, text="Correo", **label_cfg).grid(row=3, column=0, sticky="e", padx=10, pady=5)
    entry_correo.grid(row=3, column=1, padx=10, pady=5)

    # — Frame Botones CRUD —
    frm_btn = Frame(pestaña, bg="#E3F2FD")
    frm_btn.pack(pady=15)

    # — Validación de campos —
    def validar(i,n,t,d,c):
        if not validaciones.validar_telefono(t):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("telefono")); return False
        if not validaciones.validar_nombre(n):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("nombre")); return False
        if not validaciones.validar_id(i):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("id")); return False
        if not validaciones.validar_correo(c):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("correo")); return False
        return True

    # — Operaciones CRUD —
    def refrescar():
        nonlocal items
        for r in tbl.get_children(): tbl.delete(r)
        cursor.execute("SELECT id_cliente,nombre,telefono,direccion,correo FROM clientes")
        for rec in cursor.fetchall():
            tbl.insert("", "end", values=rec)
        items = tbl.get_children()

    def agregar():
        t = entry_tel.get().strip(); n = entry_nom.get().strip()
        i = entry_id.get().strip(); d = entry_dir.get().strip()
        c = entry_correo.get().strip()
        if not validar(i,n,t,d,c): return
        cursor.execute(
            "INSERT INTO clientes(telefono,nombre,id_cliente,direccion,correo) VALUES(%s,%s,%s,%s,%s)",
            (t,n,i,d,c)
        )
        conn.commit(); refrescar()

    def modificar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una fila primero."); return
        t = entry_tel.get().strip(); n = entry_nom.get().strip()
        i = entry_id.get().strip(); d = entry_dir.get().strip()
        c = entry_correo.get().strip()
        if not validar(i,n,t,d,c): return
        cursor.execute(
            "UPDATE clientes SET nombre=%s,id_cliente=%s,direccion=%s,correo=%s WHERE telefono=%s",
            (n,i,d,c,t)
        )
        conn.commit(); refrescar()

    def eliminar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una fila primero."); return
        t = tbl.item(sel[0],"values")[2]
        if messagebox.askyesno("Confirmar", f"Eliminar cliente {t}?"):
            cursor.execute("DELETE FROM clientes WHERE telefono=%s",(t,))
            conn.commit(); refrescar()

    # — Botones CRUD —
    Button(frm_btn, text="Agregar",  style="BotonAzul.TButton", command=agregar).pack(side="left", padx=10)
    Button(frm_btn, text="Modificar",style="BotonAzul.TButton", command=modificar).pack(side="left", padx=10)
    Button(frm_btn, text="Eliminar", style="BotonAzul.TButton", command=eliminar).pack(side="left", padx=10)

    # — Frame de Búsqueda (auto) —
    frm_search = Frame(pestaña, bg="#E3F2FD")
    frm_search.pack(pady=10)
    Label(frm_search, text="Buscar:", **label_cfg).pack(side="left", padx=5)
    entry_busq = Entry(frm_search, **entry_cfg)
    entry_busq.pack(side="left", padx=5)

    def mostrar_todos(event=None):
        for it in items: tbl.reattach(it, '', 'end')
        entry_busq.delete(0, "end")

    def buscar(event=None):
        término = entry_busq.get().lower().strip()
        if not término:
            mostrar_todos()
            return
        for it in items:
            vals = tbl.item(it, "values")
            if (término not in vals[2].lower()  # teléfono
                and término not in vals[1].lower()):  # nombre
                tbl.detach(it)
            else:
                tbl.reattach(it, '', 'end')

    entry_busq.bind("<KeyRelease>", buscar)

    # — Tabla de Clientes —
    tbl = Treeview(pestaña,
                   columns=("id","nombre","telefono","direccion","correo"), show="headings")
    tbl.pack(fill=BOTH, expand=True, padx=80, pady=(0,40))
    for col,w,txt in [
        ("id",100,"ID Cliente"),
        ("nombre",200,"Nombre"),
        ("telefono",150,"Teléfono"),
        ("direccion",200,"Dirección"),
        ("correo",200,"Correo")
    ]:
        tbl.heading(col, text=txt)
        tbl.column(col, width=w, anchor="center")

    # — Carga de selección en el formulario —
    def on_select(e):
        sel = tbl.selection()
        if sel:
            v = tbl.item(sel[0], "values")
            entry_id.delete(0,"end");  entry_id.insert(0,v[0])
            entry_nom.delete(0,"end"); entry_nom.insert(0,v[1])
            entry_tel.delete(0,"end"); entry_tel.insert(0,v[2])
            entry_dir.delete(0,"end"); entry_dir.insert(0,v[3])
            entry_correo.delete(0,"end"); entry_correo.insert(0,v[4])

    tbl.bind("<<TreeviewSelect>>", on_select)

    # — Carga inicial —
    items = []
    refrescar()

    ventana.mainloop()

if __name__ == "__main__":
    clientes_app()
