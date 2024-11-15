#!/usr/bin/python3
# author: Tristan Gayrard

"""
CalculaTorque V1
"""

valeur_nominale = float(input("Valeur Nominale = "))
valeur_capteur = float(input("Valeur Capteur = "))
valeur_cle = float(input("Valeur Clé = "))
valeur_optimu = valeur_cle - (valeur_capteur - valeur_nominale)

print(f"Valeur Optimu = {valeur_optimu:.3f}")
