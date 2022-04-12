from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import json
import subprocess


with open("options.json","r")as option:
    options= json.load(option)



root = Tk()
root.title("DarEdit")
root.geometry("600x500")
root.iconbitmap(bitmap="icone.ico")

scrolly = Scrollbar(root)
scrolly.pack(side= RIGHT,fill =Y)
text  = Text(root,yscrollcommand=scrolly.set,bg=options["bg"],fg=options["textcolor"],insertbackground=options["insertbg"],undo=True)
text.pack(fill=BOTH, expand=YES)




if options["recentfile"] != "":
    try:
        with open(options["recentfile"], "r")as file:
            text.insert(1.0,file.read())
            name = options["recentfile"]

            root.title(name + " - DarEdit")
    except:
        options["recentfile"]=""

def save():
    print("save")


    contenu_text=text.get(1.0,END)
    if options["recentfile"]!="":
        with open(options["recentfile"],"w")as f:
            f.write(contenu_text)
    else:
        sauv = asksaveasfilename(title="Sauvegardez votre fichier")
        with open(sauv,"w") as file:
            file.write(contenu_text)
        options["recentfile"]=sauv
    print(contenu_text)
def open_new_file():
    print("open")
    open_new = askopenfilename(title="ouvrir un nouveau fichier")
    if open_new != "":
        with open(open_new,"r") as file:
            text.insert(1.0,file.read())
            options["recentfile"]=open_new
            root.title(open_new+" - DarEdit")

def new_file():
    demande = askyesno("Voulez-vous sauvegarder le fichier actuel?",message="Voulez-vous sauvegarder le fichier actuel?",icon="warning")
    if demande:
        save()
    new = asksaveasfilename(title="Nouveau fichier")
    print(new)
    if new != "":
        with open(new,"w") as f:
            text.delete(1.0,END)
            options["recentfile"]=new

def quit():
    demande = askyesno("Voulez-vous sauvegarder le fichier actuel?",message="Voulez-vous sauvegarder le fichier actuel?", icon="warning")
    if demande:
        save()
    root.destroy()

def save_in():
    open_new = askopenfilename(title="ouvrir un nouveau fichier")
    if open_new != "":
        with open(open_new, "r") as file:
            text.insert(1.0, file.read())
            options["recentfile"] = open_new
            root.title(open_new + " - DarEdit")

def run():
    subprocess.run([options["recentfile"]])

def touch_save_in(event):
    save_in()

def touch_quit(event):
    quit()

def touch_open_new_file(event):
    print("opennew")
    open_new_file()
def touch_save(event):
    save()
def touch_new_file(event):
    new_file()
def redo(event):
    text.edit_redo()
    print("redo")
def undo(event):
    text.edit_undo()
    print("undo")
def separator(event):
    text.edit_separator()




menu_haut = Menu(root,tearoff=0)
root.config(menu=menu_haut)
menufichier = Menu(menu_haut,tearoff=0)
menu_haut.add_cascade(label="Fichier",menu=menufichier)
menufichier.add_command(label="Ouvrir nouveau",command=open_new_file)
menufichier.add_command(label="Nouveau",command=new_file)
menufichier.add_command(label="Enregistrer",command=save)
menufichier.add_command(label="Enregistrer sous...",command=save_in)
menufichier.add_command(label="lancer",command=run)
menufichier.add_separator()
menufichier.add_command(label="Quitter",command=quit)






root.bind("<Control-s>",touch_save)
root.bind("<Control-o>",touch_open_new_file)
root.bind("<Control-n>",touch_new_file)
root.bind("<Control-q>",touch_quit)
root.bind("<Alt-s>",touch_save_in)
#root.bind("<Control-z>",undo)
#root.bind("<Control-y>",redo)
#root.bind(text,"KeyPress",separator)



root.mainloop()

with open("options.json","w")as f:
    json.dump(options, f)

