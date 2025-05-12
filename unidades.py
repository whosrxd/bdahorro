# unidades.py
from tkinter import Tk, Label, Entry, Frame, BOTH, messagebox
from tkinter.ttk import Button, Notebook, Style, Treeview
import conexion
import validaciones

def unidades_app():
    # — Conexión a BD —
    conn   = conexion.conectar()
    cursor = conn.cursor()

    # — Ventana principal fullscreen —
    ventana = Tk()
    ventana.title("Gestión de Unidades de Medida")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg="#E3F2FD")

    # — Notebook por si quieres añadir más pestañas luego —
    notebook = Notebook(ventana)
    notebook.pack(fill=BOTH, expand=True)

    # — Pestaña Unidades —
    pestaña = Frame(notebook, bg="#E3F2FD")
    notebook.add(pestaña, text="Unidades")

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
    Label(frm, text="Unidad de Medida", **title_cfg).grid(row=0, column=0, columnspan=2, pady=(0,20))

    # Entrys
    entry_id   = Entry(frm, **entry_cfg)
    entry_nom  = Entry(frm, **entry_cfg)

    # Etiquetas + grid
    Label(frm, text="ID Unidad", **label_cfg).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_id.grid(row=1, column=1, padx=10, pady=5)
    Label(frm, text="Nombre", **label_cfg).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_nom.grid(row=2, column=1, padx=10, pady=5)

    # — Frame Botones CRUD —
    frm_btn = Frame(pestaña, bg="#E3F2FD")
    frm_btn.pack(pady=15)

    # — Validación de campos —
    def validar_campos(i, n):
        if not validaciones.validar_id(i):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("id")); return False
        if not validaciones.validar_nombre(n):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("nombre")); return False
        return True

    # — Operaciones CRUD —
    def refrescar():
        nonlocal items
        for r in tbl.get_children():
            tbl.delete(r)
        cursor.execute("SELECT id_unidad, nombre FROM unidades")
        for rec in cursor.fetchall():
            tbl.insert("", "end", values=rec)
        items = tbl.get_children()

    def agregar():
        i = entry_id.get().strip(); n = entry_nom.get().strip()
        if not validar_campos(i, n): return
        cursor.execute("INSERT INTO unidades(id_unidad, nombre) VALUES(%s,%s)", (i, n))
        conn.commit(); refrescar()

    def modificar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una fila primero."); return
        i = entry_id.get().strip(); n = entry_nom.get().strip()
        if not validar_campos(i, n): return
        cursor.execute("UPDATE unidades SET nombre=%s WHERE id_unidad=%s", (n, i))
        conn.commit(); refrescar()

    def eliminar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una fila primero."); return
        i = tbl.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirmar", f"Eliminar unidad {i}?"):
            cursor.execute("DELETE FROM unidades WHERE id_unidad=%s", (i,))
            conn.commit(); refrescar()

    # — Botones CRUD —
    Button(frm_btn, text="Agregar",  style="BotonAzul.TButton", command=agregar).pack(side="left", padx=10)
    Button(frm_btn, text="Modificar",style="BotonAzul.TButton", command=modificar).pack(side="left", padx=10)
    Button(frm_btn, text="Eliminar", style="BotonAzul.TButton", command=eliminar).pack(side="left", padx=10)

    # — Frame de Búsqueda —
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
        if not término: return mostrar_todos()
        for it in items:
            vals = tbl.item(it, "values")
            if término not in vals[0].lower() and término not in vals[1].lower():
                tbl.detach(it)
            else:
                tbl.reattach(it, '', 'end')

    entry_busq.bind("<KeyRelease>", buscar)

    # — Tabla de Unidades —
    tbl = Treeview(pestaña,
                   columns=("id","nombre"), show="headings")
    tbl.pack(fill=BOTH, expand=True, padx=80, pady=(0,40))
    for col, w, txt in [
        ("id",120,"ID Unidad"),
        ("nombre",400,"Nombre")
    ]:
        tbl.heading(col, text=txt)
        tbl.column(col, width=w, anchor="center")

    # — Carga de selección en formulario —
    def on_select(e):
        sel = tbl.selection()
        if sel:
            v = tbl.item(sel[0], "values")
            entry_id.delete(0, "end");  entry_id.insert(0, v[0])
            entry_nom.delete(0, "end"); entry_nom.insert(0, v[1])

    tbl.bind("<<TreeviewSelect>>", on_select)

    # — Carga inicial —
    items = []
    refrescar()

    ventana.mainloop()

if __name__ == "__main__":
    unidades_app()
