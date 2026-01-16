import json
from deep_translator import GoogleTranslator
from pathlib import Path
import os
from datetime import datetime
from XLH_utilities.select_tasks_directory import select_tasks_directory

# Imposta directory principali
root_dir = Path(__file__).resolve().parent
project_root = root_dir.parent

tasks_root, translated_tasks_root, dataset_name = select_tasks_directory(project_root)


# Lingue target
langs = ['it', 'es', 'de', 'fr', 'pt', 'ru', 'ar', 'zh-CN', 'ja', 'ko']


# Tracking risultati
stats = {
    'attempts': 0,
    'success': 0,
    'failed': 0,
    'skipped_existing': 0,
}


# File dove salvare il report di traduzione

run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
report_file = root_dir / 'results' / f'translation_report_{run_id}.json'


# Funzione di traduzione e salvataggio

def translate_and_save(task, lang, task_file):
    translated_task = dict(task)

    # path tipo 1-1/0.json
    relative_path = task_file.relative_to(tasks_root)

    dest_dir = translated_tasks_root / lang / relative_path.parent
    os.makedirs(dest_dir, exist_ok=True)

    dest_file = dest_dir / task_file.name

    # Evita lavoro inutile
    if dest_file.exists():
        print(f"[{lang}] Già esistente → salto: {dest_file}")
        stats["skipped_existing"] += 1
        return

    try:
        stats["attempts"] += 1

        translated_text = GoogleTranslator(
            source="auto",
            target=lang
        ).translate(task["task"])

    except Exception as e:
        print(f" Errore traducendo {relative_path} in {lang}: {e}")
        stats["failed"] += 1
        return

    # Successo
    translated_task["task"] = translated_text
    stats["success"] += 1

    with dest_file.open("w", encoding="utf-8") as f:
        json.dump(translated_task, f, ensure_ascii=False, indent=2)

    print(f"[{lang}] ✔️ Salvato: {dest_file}")


# TIMESTAMP INIZIO
start_time = datetime.now()
print("\n INIZIO TRADUZIONE:", start_time.strftime("%Y-%m-%d %H:%M:%S"))
print("--------------------------------------------------")


# Ciclo principale su tutte le task
for task_file in sorted(tasks_root.rglob("*.json")):
    print(f"\n Caricamento task: {task_file}")

    if "testbed" in task_file.parts:
        continue

    with task_file.open('r', encoding='utf-8') as f:
        task = json.load(f)

    for lang in langs:
        translate_and_save(task, lang, task_file)


# TIMESTAMP FINE
end_time = datetime.now()
duration = end_time - start_time

print("\n FINE TRADUZIONE:", end_time.strftime("%Y-%m-%d %H:%M:%S"))
print(" Durata totale:", str(duration))


# REPORT FINALE
report = {
    "dataset": dataset_name,
    "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
    "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
    "duration_seconds": duration.total_seconds(),
    "duration_h_m_s": str(duration),
    "stats": stats,
}

with report_file.open('w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)


# Output riepilogativo
print("\n RISULTATI GLOBALI")
print("------------------------------")
print(f"Tentativi totali: {stats['attempts']}")
print(f"Successi:         {stats['success']}")
print(f"Falliti:          {stats['failed']}")
print(f"Già esistenti:    {stats['skipped_existing']}")

