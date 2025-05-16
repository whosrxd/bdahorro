import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from main import interfaz

# Configuración de estilos
entry_cfg = {
    "bg": "#ffffff",
    "fg": "black",
    "relief": "flat",
    "bd": 0,
    "font": ("Arial", 14),
    "width": 20,
    "highlightbackground": "black",
    "highlightcolor": "black",
    "highlightthickness": 1
}

label_cfg = {
    "bg": "#ffffff",
    "fg": "black",
    "font": ("Arial", 14)
}

label_tit = {
    "bg": "#ffffff",
    "fg": "black",
    "font": ("Arial", 18, "bold")
}

# Login para usuario
def login(root, entry_user, entry_pass):
    usuario = entry_user.get()
    contraseña = entry_pass.get()

    if usuario == "admin" and contraseña == "Rodri1705":
        root.destroy()  # Cierra la ventana de login
        interfaz()      # Llama a la interfaz principal
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Cargando imagen
def imagen_derecha(frame):
    frame.update()
    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()

    if frame_width <= 1:
        frame_width = (frame.winfo_screenwidth() * 8) // 10
    if frame_height <= 1:
        frame_height = frame.winfo_screenheight()

    image_right = Image.open("assets/sider_ahorro.png")

    if image_right.mode == "RGBA":
        background = Image.new("RGB", image_right.size, (255, 255, 255))
        background.paste(image_right, mask=image_right.split()[3])
        image_right = background

    img_ratio = image_right.width / image_right.height
    frame_ratio = frame_width / frame_height

    if img_ratio > frame_ratio:
        new_width = frame_width
        new_height = int(frame_width / img_ratio)
    else:
        new_height = frame_height
        new_width = int(frame_height * img_ratio)

    image_right = image_right.resize((new_width, new_height), Image.Resampling.LANCZOS)
    photo_right = ImageTk.PhotoImage(image_right)

    label_img_right = tk.Label(frame, image=photo_right, bg="#ffffff")
    label_img_right.image = photo_right
    label_img_right.pack(fill="both", expand=True)

def abrir_login():
    root = tk.Tk()
    root.title("Login - BD Farmacias del Ahorro")
    root.attributes("-fullscreen", True)
    root.configure(bg="#ffffff")

    screen_width = root.winfo_screenwidth()

    root.grid_columnconfigure(0, weight=2, minsize=int(screen_width * 0.2))
    root.grid_columnconfigure(1, weight=8)
    root.grid_rowconfigure(0, weight=1)

    # Frame izquierdo
    left_frame = tk.Frame(root, bg="#ffffff")
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid_propagate(False)

    left_frame.grid_rowconfigure(0, weight=3)
    left_frame.grid_rowconfigure(1, weight=5)
    left_frame.grid_columnconfigure(0, weight=1)

    # Imagen logo
    image = Image.open("assets/logo.png")
    img_width = (screen_width * 3) // 20
    aspect_ratio = image.height / image.width
    img_height = int(img_width * aspect_ratio)

    image = image.resize((img_width, img_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    label_img = tk.Label(left_frame, image=photo, bg="#ffffff")
    label_img.image = photo
    label_img.grid(row=0, column=0, pady=20)

    # Frame del login
    login_frame = tk.Frame(left_frame, bg="#ffffff")
    login_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=20)
    login_frame.grid_columnconfigure(0, weight=1)

    label_user = tk.Label(login_frame, text="Usuario", **label_cfg, anchor="w")
    label_user.grid(row=0, column=0, sticky="ew", pady=(0, 5))

    entry_user = tk.Entry(login_frame, **entry_cfg)
    entry_user.grid(row=1, column=0, sticky="ew", pady=(0, 15))

    label_pass = tk.Label(login_frame, text="Contraseña", **label_cfg, anchor="w")
    label_pass.grid(row=2, column=0, sticky="ew", pady=(0, 5))

    entry_pass = tk.Entry(login_frame, show="*", **entry_cfg)
    entry_pass.grid(row=3, column=0, sticky="ew", pady=(0, 20))

    btn_login = tk.Button(login_frame, text="Ingresar", font=("Arial", 14),
                          bg="#ffffff", fg="black", relief="flat",
                          borderwidth=0, highlightthickness=0,
                          activebackground="#ffffff", activeforeground="black",
                          command=lambda: login(root, entry_user, entry_pass))

    btn_login.grid(row=4, column=0, sticky="ew", ipady=6)

    # Frame derecho
    right_frame = tk.Frame(root, bg="#ffffff")
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_propagate(False)

    root.after(100, lambda: imagen_derecha(right_frame))
    root.mainloop()
    
if __name__ == "__main__":
    abrir_login()