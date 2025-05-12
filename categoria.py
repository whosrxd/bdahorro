# categoria.py
from tkinter import Tk, Label, Entry, Frame, BOTH, messagebox
from tkinter.ttk import Button, Notebook, Style, Treeview
import conexion
import validaciones

def categoria_app():
    # — Conexión a BD —
    conn = conexion.conectar()
    cursor = conn.cursor()

    # — Ventana principal en pantalla completa —
    ventana = Tk()
    ventana.title("CRUD de Categorías")
    ventana.attributes('-fullscreen', True)
    ventana.configure(bg="#E3F2FD")

    # — Notebook de pestañas —
    notebook = Notebook(ventana)
    notebook.pack(fill=BOTH, expand=True)

    # — Pestaña Categoría —
    pestaña = Frame(notebook, bg="#E3F2FD")
    notebook.add(pestaña, text="Categoría")

    # — Estilos globales —
    style = Style()
    style.theme_use("default")
    style.configure("BotonAzul.TButton",
                    background="#64B5F6", foreground="black",
                    font=("Arial", 12, "bold"), padding=(10,8))
    style.map("BotonAzul.TButton",
              background=[("active", "#42A5F5")])
    style.configure("Treeview",
                    background="white", fieldbackground="white",
                    foreground="black", rowheight=30,
                    font=("Arial",12))
    style.configure("Treeview.Heading",
                    background="#90CAF9", foreground="black",
                    font=("Arial", 12, "bold"))

    # — Config de Entries y Labels —
    entry_cfg = {"bg": "#BBDEFB", "fg": "black",
                 "relief": "flat", "bd": 0,
                 "font": ("Arial", 14), "width": 20}
    label_cfg = {"bg": "#E3F2FD", "fg": "black", "font": ("Arial", 14)}
    label_tit  = {"bg": "#E3F2FD", "fg": "black", "font": ("Arial", 18, "bold")}

    # — Variables —
    id_var      = Entry
    nombre_var  = Entry
    search_var  = Entry
    items       = []

    # — Frame de Formulario (centrado) —
    frm_form = Frame(pestaña, bg="#E3F2FD")
    frm_form.pack(pady=30)

    # Título
    Label(frm_form, text="Categoría", **label_tit).grid(row=0, column=0, columnspan=2, pady=(0,20))

    # ID Categoría
    Label(frm_form, text="ID Categoría", **label_cfg).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entry_id = Entry(frm_form, **entry_cfg)
    entry_id.grid(row=1, column=1, padx=10, pady=5)

    # Nombre
    Label(frm_form, text="Nombre", **label_cfg).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entry_nombre = Entry(frm_form, **entry_cfg)
    entry_nombre.grid(row=2, column=1, padx=10, pady=5)

    # — Frame de Botones CRUD —
    frm_btns = Frame(pestaña, bg="#E3F2FD")
    frm_btns.pack(pady=10)

    # Funciones CRUD
    def refrescar():
        nonlocal items
        for row in tbl.get_children():
            tbl.delete(row)
        cursor.execute("SELECT id_categoria, nombre FROM categorias")
        for r in cursor.fetchall():
            tbl.insert("", "end", values=r)
        items = tbl.get_children()

    def validar_campos(idc, nom):
        if not validaciones.validar_id(idc):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("id"))
            return False
        if not validaciones.validar_nombre(nom):
            messagebox.showerror("Error", validaciones.mostrar_mensaje_error("nombre"))
            return False
        return True

    def agregar():
        idc  = entry_id.get().strip()
        nom  = entry_nombre.get().strip()
        if not validar_campos(idc, nom): return
        cursor.execute("INSERT INTO categorias(id_categoria,nombre) VALUES(%s,%s)", (idc, nom))
        conn.commit()
        refrescar()
        entry_id.delete(0, "end"); entry_nombre.delete(0, "end")

    def modificar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona primero una fila.")
            return
        idc = entry_id.get().strip()
        nom = entry_nombre.get().strip()
        if not validar_campos(idc, nom): return
        cursor.execute("UPDATE categorias SET nombre=%s WHERE id_categoria=%s", (nom, idc))
        conn.commit()
        refrescar()

    def eliminar():
        sel = tbl.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona primero una fila.")
            return
        idc = tbl.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirmar", f"Eliminar categoría {idc}?"):
            cursor.execute("DELETE FROM categorias WHERE id_categoria=%s", (idc,))
            conn.commit()
            refrescar()

    # Botones
    Button(frm_btns, text="Agregar",  style="BotonAzul.TButton", command=agregar).pack(side="left", padx=10)
    Button(frm_btns, text="Modificar",style="BotonAzul.TButton", command=modificar).pack(side="left", padx=10)
    Button(frm_btns, text="Eliminar", style="BotonAzul.TButton", command=eliminar).pack(side="left", padx=10)

    # — Frame de Búsqueda —
    frm_search = Frame(pestaña, bg="#E3F2FD")
    frm_search.pack(pady=20)

    Label(frm_search, text="Buscar:", **label_cfg).pack(side="left", padx=5)
    entry_busq = Entry(frm_search, **entry_cfg)
    entry_busq.pack(side="left", padx=5)

    def mostrar_todos(event=None):
        for it in items:
            tbl.reattach(it, '', 'end')
        entry_busq.delete(0, "end")

    def buscar(event=None):
        término = entry_busq.get().lower().strip()
        if not término:
            mostrar_todos()
            return
        for it in items:
            vals = tbl.item(it, "values")
            if término not in vals[0].lower() and término not in vals[1].lower():
                tbl.detach(it)
            else:
                tbl.reattach(it, '', 'end')

    entry_busq.bind("<KeyRelease>", buscar)

    # — Tabla de resultados —
    tbl = Treeview(pestaña, columns=("id","nombre"), show="headings")
    tbl.pack(fill=BOTH, expand=True, padx=80, pady=(0,40))
    tbl.heading("id",     text="ID Categoría")
    tbl.heading("nombre", text="Nombre")
    tbl.column("id",     width=200, anchor="center")
    tbl.column("nombre", width=600, anchor="w")

    # Selección de fila
    def on_select(event):
        sel = tbl.selection()
        if sel:
            vals = tbl.item(sel[0], "values")
            entry_id.delete(0, "end"); entry_id.insert(0, vals[0])
            entry_nombre.delete(0, "end"); entry_nombre.insert(0, vals[1])

    tbl.bind("<<TreeviewSelect>>", on_select)

    # Cargar datos inicialmente
    refrescar()

    ventana.mainloop()


# Si se ejecuta directamente
if __name__ == "__main__":
    categoria_app()
