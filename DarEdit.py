from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import *
from tkinter.messagebox import *
import json
import subprocess
import webbrowser

def license_web():
    print("web")
    webbrowser.open_new(r"https://www.gnu.org/licenses/gpl-3.0.html")

splash_screen = Tk()
img_file = "logo.png"
img = PhotoImage(file=img_file)
splash_screen.geometry("300x400+625+200")
splash_screen.overrideredirect(1)
canvas = Canvas(splash_screen,bd=0,highlightthickness=0,width=300,height=300,bg="white")
canvas.create_image(150,140,image=img)
textvar="par Fytecas"
label = Label(splash_screen,text=textvar,bg="white",font="helvetica")
licence = Label(splash_screen,text="GNU General Public License (GPL)",bg="white")
canvas.grid()
label.grid()
licence.grid()
splash_screen.configure(bg="white")




def destroy_splash():
    splash_screen.destroy()
splash_screen.after(3000,destroy_splash)
splash_screen.mainloop()


#on load les option du fichier options.json
with open("options.json","r")as file:
    options= json.load(file)

#on creer la fenetre et ses widgets
root = Tk()
root.title("DarEdit")
root.geometry("600x500")
root.iconbitmap(bitmap="icone.ico")
style = ttk.Style()
style.theme_use('classic')
pw = ttk.PanedWindow(orient=HORIZONTAL)

#on creer la zone de texte principale
text=[0,1]
scrolly = tk.Scrollbar(root)
scrolly.pack(side= LEFT,fill =Y)
text[0]  = tk.Text(root,yscrollcommand=scrolly.set,bg=options["bg"],fg=options["textcolor"],insertbackground=options["insertbg"],undo=True)
#le zone de texte secondaire
scrolly1 = tk.Scrollbar(root)
scrolly1.pack(side= RIGHT,fill =Y)
text[1]  = tk.Text(root,yscrollcommand=scrolly1.set,bg=options["bg"],fg=options["textcolor"],insertbackground=options["insertbg"],undo=True)
#la variable textzone permet de savoir sur quelle widget text se trouve le curseur
textzone=0
#création des fonction de l'éditeur
    #refresh permet de mettre a jour tout les widget text, lorsque l'on ouvre deux fois le même fichier par exemple
def refresh():
    el = 0
    for i in text:
        print(i)
        if i != "":
            with open(options["recentfile"][el], "r") as file:
                text[el].insert(1.0, file.read())

                root.title(options["recentfile"][el] + " - DarEdit")
        el=+1

#la variable save permet de sauver un widget text
def save(textnum):

    message = tk.Message(root,text="text "+str(textzone)+" saved")
    message.pack()


    contenu_text=text[textnum].get(1.0,tk.END)

    recentfile=options["recentfile"]
    if recentfile[textnum]!="":
        with open(recentfile[textnum],"w")as f:
            f.write(contenu_text)
    else:
        sauv = asksaveasfilename(title="Sauvegardez votre fichier")
        with open(sauv,"w") as file:
            file.write(contenu_text)
        recentfile[textnum]=sauv

    def destroy_message():
        message.destroy()
    root.after(1500,destroy_message)
#la fonction open_new_file permet d'ouvrir un fichier dans un widget text
def open_new_file(textnum):
    open_new = askopenfilename(title="ouvrir un nouveau fichier")
    if open_new != "":
        with open(open_new,"r") as file:
            text[textnum].insert(1.0,file.read())
            root.title(options["recentfile"][textnum]+" - DarEdit")

#la fonction new_file permet de creer un nouveau fichier et de demander a l'utilisateur si il veut sauvegarder le fichier actuel
def new_file(textnum):
    demande = askyesno("Voulez-vous sauvegarder le fichier actuel?",message="Voulez-vous sauvegarder le fichier actuel?",icon="warning")
    if demande:
        save(textnum)
    new = asksaveasfilename(title="Nouveau fichier")
    if new != "":
        with open(new,"w") as f:
            text[textnum].delete(1.0,tk.END)
            options["recentfile"]=new

#la fonction quit permet de quitter le logiciel en demandant si l'utilisateur veut sauvegarder le fichier actuel
def quit(textnum):
    demande = askyesno("Voulez-vous sauvegarder le fichier actuel?",message="Voulez-vous sauvegarder le fichier actuel?", icon="warning")
    if demande:
        save(textnum)
    root.destroy()

#la fonction save_in permet de sauvegarder un fichier dans un dosier spécifié par l'utilisateur
def save_in(textnum):
    filesave_in = asksaveasfilename(title="Enregistrer sous...")
    if filesave_in != "":
        with open(filesave_in, "w") as file:
            file.write(text[textnum].get(1.0,tk.END))
            options["recentfile"][textnum] = filesave_in
            root.title(filesave_in + " - DarEdit")

#la fonction textzone_refresh permet de mettre a jour la variable textzone
def textzone_refresh(event):
    global textzone
    save(textzone)
    if "text"in str(event.widget):
        textzone=str(event.widget).replace(".!text","")
    if textzone == "":
        textzone=0
    elif textzone != 0:
        textzone=int(textzone)-1

#la fonction run permet de lancer le script
def run(event=0):
    subprocess.call(options["recentfile"][textzone], shell=True)

def touch_save_in(event):
    save_in(textzone)

def touch_quit(event):
    quit(textzone)

def touch_open_new_file(event):
    open_new_file(textzone)
def touch_save(event=0):
    save(textzone)
def touch_new_file(event):
    new_file(textzone)
def redo(event):
    text[textzone].edit_redo()
    print("redo")
def undo(event):
    text[textzone].edit_undo()
    print("undo")
def open_source():
    webbrowser.open_new(r"https://github.com/Fytecas/DarEdit.git")




#création du menu
menu_haut = tk.Menu(root,tearoff=0)
root.config(menu=menu_haut)
menufichier = tk.Menu(menu_haut,tearoff=0)
menu_haut.add_cascade(label="Fichier",menu=menufichier)
menufichier.add_command(label="Ouvrir nouveau",command=open_new_file)
menufichier.add_command(label="Nouveau",command=new_file)
menufichier.add_command(label="Enregistrer",command=touch_save)
menufichier.add_command(label="Enregistrer sous...",command=save_in)
menufichier.add_command(label="lancer",command=run)
menufichier.add_command(label="Mettre a jour",command=refresh)
menufichier.add_separator()
menufichier.add_command(label="Quitter",command=quit)

menu_licence = tk.Menu(menu_haut,tearoff=0)
menu_haut.add_cascade(label="licence | open source",menu=menu_licence)
menu_licence.add_command(label="GNU General Public License (GPL)",command=license_web)
menu_licence.add_command(label="Un logiciel par Fytecas | Fichiers source",command=open_source)

#création des raccoucis
root.bind("<Control-s>",touch_save)
root.bind("<Control-o>",touch_open_new_file)
root.bind("<Control-n>",touch_new_file)
root.bind("<Control-q>",touch_quit)
root.bind("<Alt-s>",touch_save_in)
root.bind("<Button-1>",textzone_refresh)
root.bind("<Control-l>",run)
root.bind("<Control-z>",undo)
root.bind("<Control-y>",redo)


text[1].pack(fill=BOTH, expand=tk.YES,side=RIGHT)
text[0].pack(fill=BOTH, expand=tk.YES,side=LEFT)
pw.add(text[0])
pw.add(text[1])
pw.pack(fill=BOTH,expand=YES)
refresh()
root.mainloop()

with open("options.json","w")as f:
    json.dump(options, f)

