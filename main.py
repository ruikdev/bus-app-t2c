import requests
import json
import tkinter as tk
from tkinter import messagebox


def test_api(stop_id):
    url = f"http://172.252.236.136:2064/horaire/{stop_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Erreur lors de la requête : {e}"}
    except json.JSONDecodeError:
        return {"error": "Erreur lors du décodage de la réponse JSON"}
    except Exception as e:
        return {"error": f"Une erreur inattendue s'est produite : {e}"}


def afficher_horaires(data):
    fenetre_resultats = tk.Toplevel()
    fenetre_resultats.title("Résultats")
    fenetre_resultats.geometry("500x300")

    text_widget = tk.Text(fenetre_resultats, wrap=tk.WORD)
    text_widget.pack(expand=True, fill=tk.BOTH)

    if "error" in data:
        text_widget.insert(tk.END, f"Erreur : {data['error']}\n")
    else:
        text_widget.insert(tk.END, f"Horaires pour l'arrêt :\n")
        text_widget.insert(tk.END, "-" * 50 + "\n")

        if "departures" in data:
            for departure in data["departures"]:
                text_widget.insert(tk.END,
                                   f"Ligne {departure['ligne']:3} | {departure['destination']:20} | Départ : {departure['depart']:10} | {departure['info']}\n")

        if "perturbation" in data and data["perturbation"]:
            text_widget.insert(tk.END, "\n⚠️ ATTENTION :\n")
            text_widget.insert(tk.END, data["perturbation"] + "\n")

    text_widget.config(state=tk.DISABLED)


def horaire_bus():
    fenetre_horaire = tk.Toplevel()
    fenetre_horaire.title("Horaire arrêt")
    fenetre_horaire.geometry("200x100")

    id_arret = tk.Entry(fenetre_horaire, width=30)
    id_arret.pack(pady=10)

    def send_request():
        stop_id = id_arret.get()
        if stop_id:
            data = test_api(stop_id)
            afficher_horaires(data)
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un ID d'arrêt")

    button_send = tk.Button(fenetre_horaire, text="OK", command=send_request)
    button_send.pack(pady=10)


def afficher_id_arrets():
    # Cette fonction pourrait être implémentée pour afficher une liste des ID d'arrêts
    # Pour l'instant, elle affiche juste un message
    messagebox.showinfo("ID des arrêts", "Fonctionnalité non implémentée")


def main():
    fenetre_menu = tk.Tk()
    fenetre_menu.title("T2C Bus")
    fenetre_menu.geometry("200x150")

    button_horaire = tk.Button(fenetre_menu, text="Prochain bus à l'arrêt", command=horaire_bus)
    button_horaire.pack(pady=5)

    button_arret = tk.Button(fenetre_menu, text="ID des arrêts", command=afficher_id_arrets)
    button_arret.pack(pady=5)

    fenetre_menu.mainloop()


if __name__ == "__main__":
    main()
