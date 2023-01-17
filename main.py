from cProfile import label
from functools import partial
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import tkinter as tk


def genera_Hash(texto_bytes, texto_str, salida):
    messagebox.showinfo(message="Seleccione la llave privada")
    archivo = askopenfilename()

    with open(archivo, 'rb') as f:  # importa la llave privada
        llave = f.read()
        key = RSA.import_key(llave)
        hash_256 = SHA256.new(texto_bytes)
        firma = pss.new(key).sign(hash_256)

    with open(salida, 'w') as f:
        f.write(texto_str + firma.hex())


def verificar(texto, firma):
    messagebox.showinfo(message="Seleccione la llave publica")
    archivo = askopenfilename()

    with open(archivo, 'rb') as f:  # importa la llave publica
        llave = f.read()
        key = RSA.import_key(llave)
        hash_2 = SHA256.new(texto)
        verif = pss.new(key)

    try:
        verif.verify(hash_2, firma)
        messagebox.showinfo(message="El archivo es auténtico")
    except (ValueError, TypeError):
        messagebox.showinfo(message="El archivo NO es auténtico")


def principal():
    op = opciones.get()
    archivo = Arch_salida.get()
    if (op == "firmar" and archivo != ""):
        archivo += ".txt"
        messagebox.showinfo(message="Seleccione el archivo a firmar")
        lectura = askopenfilename()
        with open(lectura, 'r') as f:
            texto = f.read()
            genera_Hash(bytes(texto, encoding="utf-8"), texto, archivo)

    elif (op == "verificar"):
        messagebox.showinfo(message="Seleccione el archivo a verificar")
        archivo = askopenfilename()
        with open(archivo, 'r') as fil:
            cad = fil.read()
            firma = cad[-256:]
            cuerpo = cad[0:-256]
            verificar(bytes(cuerpo, encoding="utf-8"),
                      bytes.fromhex(firma))
    else:
        messagebox.showinfo(message="Llene todos los campos")


# ------------------Interfaz------------------#
ventana = tk.Tk()

ventana.title("Firma y verificacion")
ventana.geometry("600x300+500+200")
titulo = tk.Label(ventana, text="Bienvenido, desea firmar o verificar?",
                  font=('Arial 20 bold'))
label = tk.Label(ventana, font=('Arial 12 bold'),
                 text="Nombre del archivo de salida")
label_op = tk.Label(ventana, font=('Arial 12 bold'),
                    text="Seleccione una opcion")
opciones = ttk.Combobox(state="readonly", values=["firmar", "verificar"])
Arch_salida = tk.Entry(ventana)
titulo.grid(columnspan=2, padx=(30, 10))
boton = tk.Button(ventana, text="Ejecutar", font=(
    'Arial 12 bold'), command=partial(principal))
label_op.grid(row=1, column=0)
opciones.grid(row=1, column=1)
label.grid(row=2, column=0, pady=(20, 20))
Arch_salida.grid(row=2, column=1)
boton.grid(row=3, pady=(20, 0))

ventana.mainloop()
