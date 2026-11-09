"""Task Manager: small command-line task manager."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "tasks.json"


def load_tasks():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("Avertissement : fichier de données illisible. Démarrage avec une liste vide.")
        return []


def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def add_task(tasks):
    title = input("Titre de la tâche : ").strip()
    if not title:
        print("Le titre ne peut pas être vide.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print("Tâche ajoutée.")


def list_tasks(tasks):
    if not tasks:
        print("Aucune tâche enregistrée.")
        return
    print("\n--- Liste des tâches ---")
    for index, task in enumerate(tasks, start=1):
        status = "Terminée" if task["done"] else "À faire"
        print(f"{index}. [{status}] {task['title']}")


def complete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return
    try:
        index = int(input("Numéro de la tâche à terminer : "))
        if not 1 <= index <= len(tasks):
            raise ValueError
    except ValueError:
        print("Numéro invalide.")
        return
    tasks[index - 1]["done"] = True
    save_tasks(tasks)
    print("Tâche marquée comme terminée.")


def delete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return
    try:
        index = int(input("Numéro de la tâche à supprimer : "))
        if not 1 <= index <= len(tasks):
            raise ValueError
    except ValueError:
        print("Numéro invalide.")
        return
    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f"Tâche supprimée : {removed['title']}")


def main():
    tasks = load_tasks()
    while True:
        print("\n===== TASK MANAGER =====")
        print("1. Ajouter une tâche")
        print("2. Afficher les tâches")
        print("3. Terminer une tâche")
        print("4. Supprimer une tâche")
        print("0. Quitter")
        choice = input("Votre choix : ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "0":
            print("Au revoir.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()
