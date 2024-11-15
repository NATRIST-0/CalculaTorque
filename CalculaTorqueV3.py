#!/usr/bin/python3 
# author: Tristan Gayrard

"""
CalculaTorqueV3
"""

import tkinter as tk
from tkinter import ttk
import sys
import os


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class CalculaTorqueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CalculaTorque V3")
        self.attributes("-topmost", True)
        try:
            self.iconbitmap(resource_path("wrench.ico"))
        except:
            pass 

        # Grille
        self.grid_columnconfigure(1, weight=1)

        # Entrées
        ttk.Label(self, text="Valeur Nominale :").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.valeur_nominale = tk.DoubleVar()
        self.entry_nominale = ttk.Entry(self, textvariable=self.valeur_nominale)
        self.entry_nominale.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.configure_entry(self.entry_nominale)

        ttk.Label(self, text="Valeur Étalon :").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.valeur_etalon = tk.DoubleVar()
        self.valeur_etalon = ttk.Entry(self, textvariable=self.valeur_etalon)
        self.valeur_etalon.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.configure_entry(self.valeur_etalon)

        ttk.Label(self, text="Valeur Instrument :").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.valeur_instru = tk.DoubleVar()
        self.valeur_instru = ttk.Entry(self, textvariable=self.valeur_instru)
        self.valeur_instru.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.configure_entry(self.valeur_instru, trigger_calculate=True)

        # Résultat
        ttk.Label(self, text="Valeur Optimu :").grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.result_label = ttk.Label(self, text="0.000")
        self.result_label.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        # Boutons
        self.copy_button = ttk.Button(self, text="Copier", command=self.copy_result)
        self.copy_button.grid(row=2, column=5, padx=5, pady=5, sticky="w")

        self.add_row_button = ttk.Button(self, text="+ Ajouter une ligne", command=self.add_row)
        self.add_row_button.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        # Menu déroulant
        self.variable = tk.StringVar(self)
        reference = ["Référence Étalon", "Référence Instrument"]
        self.variable.set(reference[0])
        self.option_menu = ttk.OptionMenu(self, self.variable, reference[0], *reference, command=self.update_fields)
        self.option_menu.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        # Label de confirmation
        self.confirm_label = ttk.Label(self, text="", foreground="green")
        self.confirm_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
    def update_fields(self, event):
        """Switches the columns 'Valeur Étalon' and 'Valeur Instrument' 
           when triggered. Adjusts the calculation based on the selected reference."""
        reference = self.variable.get()
        if reference == "Référence Étalon":
            # Met à jour les libellés pour correspondre à l'état Référence Étalon
            self.children["!label2"].config(text="Valeur Étalon :")
            self.children["!label3"].config(text="Valeur Instrument :")
        else:
            # Met à jour les libellés pour correspondre à l'état Référence Instrument
            self.children["!label2"].config(text="Valeur Instrument :")
            self.children["!label3"].config(text="Valeur Étalon :")
        
        # Met à jour l'étiquette de confirmation pour informer l'utilisateur
        self.confirm_label.config(text=f"Mode changé à : {reference}", foreground="green")
        self.after(2000, lambda: self.confirm_label.config(text="", foreground="green"))

       
    
    def configure_entry(self, entry, trigger_calculate=False):
        """Configure entry to select all text on focus and optionally trigger calculation on Enter key."""
        entry.bind("<FocusIn>", lambda event: entry.select_range(0, tk.END))
        if trigger_calculate:
            entry.bind("<Return>", lambda event: self.calculate())
        else:
            entry.bind("<Return>", self.focus_next_widget)

    def focus_next_widget(self, event):
        """Move focus to the next widget when Enter is pressed."""
        event.widget.tk_focusNext().focus()
        return "break"

    def calculate(self):
        try:
            # Conversion des entrées en float
            valeur_nominale = float(self.valeur_nominale.get())
            valeur_etalon = float(self.valeur_etalon.get())
            valeur_instru = float(self.valeur_instru.get())
            reference = self.variable.get()
            
            if reference == "Référence Étalon":
                valeur_optimu = valeur_instru - (valeur_etalon - valeur_nominale)
            else:
                valeur_optimu = valeur_nominale - (valeur_etalon - valeur_instru)
    
            self.result_label.config(text=f"{valeur_optimu:.3f}")
            self.copy_result()
        except ValueError:
            self.confirm_label.config(text="Entrée invalide", foreground="red")
            self.after(2000, lambda: self.confirm_label.config(text="", foreground="green"))


    def copy_result(self):
        valeur_optimu = self.result_label.cget("text")
        self.clipboard_clear()
        self.clipboard_append(valeur_optimu)
        self.confirm_label.config(text="Valeur copiée dans le presse-papiers")
        self.after(2000, lambda: self.confirm_label.config(text=""))

    def add_row(self):
        self.confirm_label.config(text="Fonctionnalité à implémenter", foreground="blue")
        self.after(2000, lambda: self.confirm_label.config(text="", foreground="green"))


if __name__ == "__main__":
    app = CalculaTorqueApp()
    app.mainloop()
    
    

