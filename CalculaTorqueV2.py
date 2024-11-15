#!/usr/bin/python3 
# author: Tristan Gayrard

"""
CalculaTorqueV2
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class CalculaTorqueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CalculaTorque V2")
        self.attributes("-topmost", True)
        self.iconbitmap(resource_path("wrench.ico"))
        
        # Configuration de la grille
        self.grid_columnconfigure(1, weight=1)
        
        # Entrées de données
        ttk.Label(self, text="Valeur Nominale :").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.valeur_nominale = tk.DoubleVar()
        self.entry_nominale = ttk.Entry(self, textvariable=self.valeur_nominale)
        self.entry_nominale.grid(row=1, column=0, padx=5, pady=5)
        self.configure_entry(self.entry_nominale)
        
        ttk.Label(self, text="Valeur Étalon :").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.valeur_capteur = tk.DoubleVar()
        self.entry_capteur = ttk.Entry(self, textvariable=self.valeur_capteur)
        self.entry_capteur.grid(row=1, column=1, padx=5, pady=5)
        self.configure_entry(self.entry_capteur)
        
        ttk.Label(self, text="Valeur Instrument :").grid(row=0, column=2, padx=1, pady=5, sticky="w")
        self.valeur_cle = tk.DoubleVar()
        self.entry_cle = ttk.Entry(self, textvariable=self.valeur_cle)
        self.entry_cle.grid(row=1, column=2, padx=5, pady=5)
        self.configure_entry(self.entry_cle, trigger_calculate=True)  # Activation du calcul au niveau de "Valeur Clé"
        
        # Affichage du résultat
        ttk.Label(self, text="Valeur Optimu :").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.result_label = ttk.Label(self, text="0.000")
        self.result_label.grid(row=4, column=1, padx=5, pady=5)
        
        # Label de confirmation
        self.confirm_label = ttk.Label(self, text="", foreground="green")
        self.confirm_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        self.signature = ttk.Label(self, text="By : Tristan Gayrard 👍😎")
        self.signature.grid(row=5, column=2, columnspan=2, padx=5, pady=5)

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
        # Récupération des valeurs
        valeur_nominale = self.valeur_nominale.get()
        valeur_capteur = self.valeur_capteur.get()
        valeur_cle = self.valeur_cle.get()
        
        # Calcul de valeur_optimu
        valeur_optimu = valeur_cle - (valeur_capteur - valeur_nominale)
        
        # Affichage du résultat
        self.result_label.config(text=f"{valeur_optimu:.3f}")
        
        # Copie de la valeur dans le presse-papiers
        self.clipboard_clear()
        self.clipboard_append(f"{valeur_optimu:.3f}")
        
        # Affichage du message de confirmation
        self.confirm_label.config(text="Valeur copiée dans le presse-papiers")
        self.after(2000, lambda: self.confirm_label.config(text=""))  # Disparition du message après 2 secondes

if __name__ == "__main__":
    app = CalculaTorqueApp()
    app.mainloop()
