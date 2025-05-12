# proveedores.py
from tkinter import Tk, Label, Entry, Frame, BOTH, messagebox
from tkinter.ttk import Button, Notebook, Style, Treeview
import conexion
import validaciones

def proveedores_app():
    # — Conexión a BD —
    conn   = conexion.conectar()
    cursor = conn.cursor()

    # — Ventana principal pantalla completa —
    ventana = Tk()
    ventana.title("Gestión de Proveedores")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg="#E3F2FD")

    # — Notebook (por si añades más pestañas) —
    notebook = Notebook(ventana)
    notebook.pack(fill=BOTH, expand=True)

    # — Pestaña Proveedores —
    pestaña = Frame(notebook, bg="#E3F2FD")
    notebook.add(pestaña, text="Proveedores")

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
    label_cfg = {"bg": "#E3F2FD", "fg": "black", "font": ("Arial",14)}
    title_cfg = {"bg": "#E3F2FD", "fg": "black", "font": ("Arial",18,"bold")}
    entry_cfg = {"bg": "#BBDEFB", "fg": "black",
                 "relief": "flat", "bd": 0,
                 "font": ("Arial",14), "width": 20}

    # — Frame del formulario —
    frm = Frame(pestaña, bg="#E3F2FD")
    frm.pack(pady=30)

    # Título
    Label(frm, text="Proveedor", **title_cfg).grid(row=0, column=0, columnspan=4, pady=(0,20))

    # Campos de formulario
    entry_id      = Entry(frm, **entry_cfg)
    entry_nombre  = Entry(frm, **entry_cfg)
    entry_tel     = Entry(frm, **entry_cfg)
    entry_contact = Entry(frm, **entry_cfg)

    Label(frm, text="ID Proveedor", **label_cfg).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_id.grid(row=1, column=1, padx=10, pady=5)
    Label(frm, text="Nombre", **label_cfg).grid(row=1, column=2, sticky="e", padx=10, pady=5)
    entry_nombre.grid(row=1, column=3, padx=10, pady=5)

    Label(frm, text="Teléfono", **label_cfg).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_tel.grid(row=2, column=1, padx=10, pady=5)
    Label(frm, text="Contacto", **label_cfg).grid(row=2, column=2, sticky="e", padx=10, pady=5)
    entry_contact.grid(row=2, column=3, padx=10, pady=5)

    # — Frame Botones CRUD —
    frm_btn = Frame(pestaña, bg="#E3F2FD")
    frm_btn.pack(pady=15)

    # Funciones auxiliares
    def validar_campos(idp, nom, tel):
        if not validaciones.validar_id(idp):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("id"))
            return False
        if not validaciones.validar_nombre(nom):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("nombre"))
            return False
        if not validaciones.validar_telefono(tel):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("telefono"))
            return False
        return True

    # CRUD real
    def refrescar():
        nonlocal items
        for row in tbl.get_children():
            tbl.delete(row)
        cursor.execute("SELECT id_proveedor,nombre,telefono,contacto FROM proveedores")
        for r in cursor.fetchall():
            tbl.insert("", "end", values=r)
        items = tbl.get_children()

    def agregar():
        i = entry_id.get().strip()
        n = entry_nombre.get().strip()
        t = entry_tel.get().strip()
        c = entry_contact.get().strip()
        if not validar_campos(i,n,t): return
        cursor.execute(
            "INSERT INTO proveedores(id_proveedor,nombre,telefono,contacto) VALUES(%s,%s,%s,%s)",
            (i,n,t,c)
        )
        conn.commit(); refrescar()

    def modificar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una fila primero.")
            return
        i = entry_id.get().strip()
        n = entry_nombre.get().strip()
        t = entry_tel.get().strip()
        c = entry_contact.get().strip()
        if not validar_campos(i,n,t): return
        cursor.execute(
            "UPDATE proveedores SET nombre=%s,telefono=%s,contacto=%s WHERE id_proveedor=%s",
            (n,t,c,i)
        )
        conn.commit(); refrescar()

    def eliminar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una fila primero.")
            return
        i = tbl.item(sel[0],"values")[0]
        if messagebox.askyesno("Confirmar", f"Eliminar proveedor {i}?"):
            cursor.execute("DELETE FROM proveedores WHERE id_proveedor=%s",(i,))
            conn.commit(); refrescar()

    # Botones
    Button(frm_btn, text="Agregar",  style="BotonAzul.TButton", command=agregar).pack(side="left", padx=10)
    Button(frm_btn, text="Modificar",style="BotonAzul.TButton", command=modificar).pack(side="left", padx=10)
    Button(frm_btn, text="Eliminar", style="BotonAzul.TButton", command=eliminar).pack(side="left", padx=10)

    # — Frame Búsqueda —
    frm_search = Frame(pestaña, bg="#E3F2FD")
    frm_search.pack(pady=10)
    Label(frm_search, text="Buscar:", **label_cfg).pack(side="left", padx=5)
    entry_busq = Entry(frm_search, **entry_cfg)
    entry_busq.pack(side="left", padx=5)

    def mostrar_todos(event=None):
        for it in items: tbl.reattach(it,'','end')
        entry_busq.delete(0,"end")

    def buscar(event=None):
        término = entry_busq.get().lower().strip()
        if not término: return mostrar_todos()
        for it in items:
            vals = tbl.item(it,"values")
            # Busca en ID, nombre o teléfono
            if (término not in vals[0].lower()
                and término not in vals[1].lower()
                and término not in vals[2].lower()):
                tbl.detach(it)
            else:
                tbl.reattach(it,'','end')

    entry_busq.bind("<KeyRelease>", buscar)

    # — Tabla de Proveedores —
    tbl = Treeview(pestaña,
                   columns=("id","nombre","telefono","contacto"),
                   show="headings")
    tbl.pack(fill=BOTH, expand=True, padx=80, pady=(0,40))
    for col,w,txt in [
        ("id",       120, "ID Proveedor"),
        ("nombre",   200, "Nombre"),
        ("telefono", 150, "Teléfono"),
        ("contacto", 250, "Contacto")
    ]:
        tbl.heading(col, text=txt)
        tbl.column(col, width=w, anchor="center")

    # Selección para cargar en form
    def on_select(e):
        sel = tbl.selection()
        if sel:
            v = tbl.item(sel[0],"values")
            entry_id.delete(0,"end"); entry_id.insert(0,v[0])
            entry_nombre.delete(0,"end"); entry_nombre.insert(0,v[1])
            entry_tel.delete(0,"end"); entry_tel.insert(0,v[2])
            entry_contact.delete(0,"end"); entry_contact.insert(0,v[3])

    tbl.bind("<<TreeviewSelect>>", on_select)

    # Carga inicial
    items = []
    refrescar()

    ventana.mainloop()

if __name__ == "__main__":
    proveedores_app()
