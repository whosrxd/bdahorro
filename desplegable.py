from tkinter import StringVar
from tkinter.ttk import Combobox

# Lista de especialidades válidas
especialidades_validas = [
    "Medicina General", "Pediatría", "Ginecología", "Odontología",
    "Dermatología", "Cardiología", "Oftalmología", "Psiquiatría",
    "Traumatología", "Cirugía General"
]

# Variable donde se guarda la selección
especialidad_var = StringVar()

# ComboBox
combo_especialidad = Combobox(frame_categoria, values=especialidades_validas, textvariable=especialidad_var, state="readonly", font=("Arial", 14), width=25)
combo_especialidad.grid(row=3, column=1, padx=10, pady=5)

# Label de la especialidad
Label(frame_categoria, text="Especialidad", **label_config).grid(row=3, column=0, sticky="e", padx=10, pady=5)