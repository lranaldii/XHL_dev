# future task configuration
def select_tasks_directory(project_root):
    options = {
        "1": "OfficeBench_tasks",
        "2": "XLH_tasks"
    }

    print("\nSeleziona la directory sorgente delle task:")
    for k, v in options.items():
        print(f"[{k}] {v}")

    choice = None
    while choice not in options:
        choice = input("Inserisci il numero della directory corrispondente (1 o 2): ").strip()
        if choice == "1":
            tasks_root = project_root / "OB_tasks" / "en"
            translated_tasks_root = project_root / "OB_translated"
            dataset_name = "OfficeBench"
        elif choice == "2":
            tasks_root = project_root / "XLH_tasks" / "en"
            translated_tasks_root = project_root / "XLH_translated"
            dataset_name = "XLH"
        else:
            print("Scelta non valida. Inserisci 1 o 2.")
    
    print(f"\n✔️ Dataset selezionato: {dataset_name}")
    print(f"📂 Input : {tasks_root}")
    print(f"📂 Output: {translated_tasks_root}\n")

    return tasks_root, translated_tasks_root, dataset_name

