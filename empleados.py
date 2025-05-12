# empleados.py
from tkinter import Tk, Label, Entry, Frame, BOTH, messagebox
from tkinter.ttk import Button, Notebook, Style, Treeview, Combobox
from datetime import datetime
import conexion
import validaciones

def empleados_app():
    # — Conexión a BD —
    conn   = conexion.conectar()
    cursor = conn.cursor()

    # — Ventana principal fullscreen —
    ventana = Tk()
    ventana.title("Gestión de Empleados")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg="#E3F2FD")

    # — Notebook por si agregas más módulos —
    notebook = Notebook(ventana)
    notebook.pack(fill=BOTH, expand=True)

    # — Pestaña Empleados —
    pestaña = Frame(notebook, bg="#E3F2FD")
    notebook.add(pestaña, text="Empleados")

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
    Label(frm, text="Empleado", **title_cfg).grid(row=0, column=0, columnspan=4, pady=(0,20))

    # Entrys y Combobox
    entry_id    = Entry(frm, **entry_cfg)
    entry_nom   = Entry(frm, **entry_cfg)
    entry_tel   = Entry(frm, **entry_cfg)
    entry_dir   = Entry(frm, **entry_cfg)
    combo_puesto = Combobox(frm, values=[
        "Cajero", "Farmacéutico", "Auxiliar", "Supervisor", "Administrativo"
    ], state="readonly", font=("Arial",14), width=18)
    entry_fecha = Entry(frm, **entry_cfg)

    # Etiquetas + grid
    Label(frm, text="ID Empleado", **label_cfg).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_id.grid(row=1, column=1, padx=10, pady=5)
    Label(frm, text="Nombre", **label_cfg).grid(row=1, column=2, sticky="e", padx=10, pady=5)
    entry_nom.grid(row=1, column=3, padx=10, pady=5)

    Label(frm, text="Teléfono", **label_cfg).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_tel.grid(row=2, column=1, padx=10, pady=5)
    Label(frm, text="Dirección", **label_cfg).grid(row=2, column=2, sticky="e", padx=10, pady=5)
    entry_dir.grid(row=2, column=3, padx=10, pady=5)

    Label(frm, text="Puesto", **label_cfg).grid(row=3, column=0, sticky="e", padx=10, pady=5)
    combo_puesto.grid(row=3, column=1, padx=10, pady=5)
    Label(frm, text="Fecha Contratación", **label_cfg).grid(row=3, column=2, sticky="e", padx=10, pady=5)
    entry_fecha.grid(row=3, column=3, padx=10, pady=5)

    # — Frame Botones CRUD —
    frm_btn = Frame(pestaña, bg="#E3F2FD")
    frm_btn.pack(pady=15)

    # — Validación de campos —
    def validar_campos(i,n,t,d,p,f):
        if not validaciones.validar_id(i):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("id")); return False
        if not validaciones.validar_nombre(n):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("nombre")); return False
        if not validaciones.validar_telefono(t):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("telefono")); return False
        if not validaciones.validar_puesto(p):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("puesto")); return False
        if not validaciones.validar_fecha(f):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("fecha")); return False
        return True

    # — Operaciones CRUD —
    def refrescar():
        nonlocal items
        for r in tbl.get_children(): tbl.delete(r)
        cursor.execute(
            "SELECT id_empleado, nombre, telefono, direccion, puesto, fecha_contratacion "
            "FROM empleados"
        )
        for rec in cursor.fetchall():
            tbl.insert("", "end", values=rec)
        items = tbl.get_children()

    def agregar():
        i = entry_id.get().strip(); n = entry_nom.get().strip()
        t = entry_tel.get().strip(); d = entry_dir.get().strip()
        p = combo_puesto.get().strip(); f = entry_fecha.get().strip()
        if not validar_campos(i,n,t,d,p,f): return
        # Convertir fecha a ISO
        fecha_sql = datetime.strptime(f, "%d/%m/%Y").strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO empleados(id_empleado, nombre, telefono, direccion, puesto, fecha_contratacion) "
            "VALUES(%s,%s,%s,%s,%s,%s)",
            (i, n, t, d, p, fecha_sql)
        )
        conn.commit(); refrescar()

    def modificar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una fila primero."); return
        i = entry_id.get().strip(); n = entry_nom.get().strip()
        t = entry_tel.get().strip(); d = entry_dir.get().strip()
        p = combo_puesto.get().strip(); f = entry_fecha.get().strip()
        if not validar_campos(i,n,t,d,p,f): return
        fecha_sql = datetime.strptime(f, "%d/%m/%Y").strftime("%Y-%m-%d")
        cursor.execute(
            "UPDATE empleados SET nombre=%s, telefono=%s, direccion=%s, puesto=%s, fecha_contratacion=%s "
            "WHERE id_empleado=%s",
            (n, t, d, p, fecha_sql, i)
        )
        conn.commit(); refrescar()

    def eliminar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una fila primero."); return
        i = tbl.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirmar", f"Eliminar empleado {i}?"):
            cursor.execute("DELETE FROM empleados WHERE id_empleado=%s", (i,))
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
        entry_busq.delete(0,"end")

    def buscar(event=None):
        término = entry_busq.get().lower().strip()
        if not término: return mostrar_todos()
        for it in items:
            vals = tbl.item(it, "values")
            if (término not in vals[0].lower()
                and término not in vals[1].lower()
                and término not in vals[2].lower()
                and término not in vals[4].lower()):
                tbl.detach(it)
            else:
                tbl.reattach(it, '', 'end')

    entry_busq.bind("<KeyRelease>", buscar)

    # — Tabla de Empleados —
    tbl = Treeview(pestaña,
                   columns=("id","nombre","telefono","direccion","puesto","fecha"), show="headings")
    tbl.pack(fill=BOTH, expand=True, padx=80, pady=(0,40))
    for col,w,txt in [
        ("id",100,"ID Empleado"),
        ("nombre",200,"Nombre"),
        ("telefono",150,"Teléfono"),
        ("direccion",200,"Dirección"),
        ("puesto",150,"Puesto"),
        ("fecha",150,"Fecha")
    ]:
        tbl.heading(col, text=txt)
        tbl.column(col, width=w, anchor="center")

    # — Carga de selección en formulario —
    def on_select(e):
        sel = tbl.selection()
        if sel:
            v = tbl.item(sel[0], "values")
            entry_id.delete(0,"end"); entry_id.insert(0,v[0])
            entry_nom.delete(0,"end"); entry_nom.insert(0,v[1])
            entry_tel.delete(0,"end"); entry_tel.insert(0,v[2])
            entry_dir.delete(0,"end"); entry_dir.insert(0,v[3])
            combo_puesto.set(v[4])
            # convertir yyyy-mm-dd a dd/mm/YYYY
            fecha_fmt = datetime.strptime(v[5], "%Y-%m-%d").strftime("%d/%m/%Y")
            entry_fecha.delete(0,"end"); entry_fecha.insert(0, fecha_fmt)

    tbl.bind("<<TreeviewSelect>>", on_select)

    # — Carga inicial —
    items = []
    refrescar()

    ventana.mainloop()

if __name__ == "__main__":
    empleados_app()
