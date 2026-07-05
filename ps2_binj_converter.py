#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path

INPUT_DIR = Path("/storage/emulated/0/Download/PS2-BINJ")
OUTPUT_DIR = Path("/storage/emulated/0/Download/PS2-ISO")


def clear_screen():
    print("\033c", end="")


def progress_bar(current, total):
    percent = int((current / total) * 100)

    filled = percent // 5
    empty = 20 - filled

    bar = "█" * filled + "░" * empty

    print(f"\n[{bar}] {percent}%\n")


def parse_cue(cue_path):
    files = []

    with cue_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if line.upper().startswith("FILE "):
                parts = line.split('"')

                if len(parts) >= 2:
                    files.append(parts[1])

    return files


def convert_game(cue_file, keep_originals, lang):

    game_name = cue_file.stem

    print("=" * 40)
    print(f"{lang['processing']}: {game_name}")
    print("=" * 40)

    referenced_files = parse_cue(cue_file)

    if not referenced_files:
        print(f"✗ {lang['missing']}")
        return False

    missing = []

    for filename in referenced_files:
        file_path = INPUT_DIR / filename

        if not file_path.exists():
            missing.append(filename)

    if missing:
        print(f"✗ {lang['missing']}")

        for item in missing:
            print(f"  - {item}")

        return False

    bin_file = INPUT_DIR / referenced_files[0]

    prefix = INPUT_DIR / game_name

    try:
        subprocess.run(
            [
                "bchunk",
                str(bin_file),
                str(cue_file),
                str(prefix),
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        print(f"✗ {lang['failed']}")
        return False

    iso_file = INPUT_DIR / f"{game_name}01.iso"

    if not iso_file.exists():
        print(f"✗ {lang['failed']}")
        return False

    final_iso = OUTPUT_DIR / f"{game_name}.iso"

    shutil.move(str(iso_file), str(final_iso))

    print(f"✓ {lang['success']}")

    if not keep_originals:

        cue_file.unlink(missing_ok=True)

        for filename in referenced_files:
            path = INPUT_DIR / filename

            if path.exists():
                path.unlink()

    return True


def main():

    clear_screen()

    if shutil.which("bchunk") is None:
        print("bchunk not found.")
        print("Install with:")
        print("pkg install bchunk")
        return

    print("========================================")
    print("         PS2 BIN/CUE Converter")
    print("========================================")
    print()
    print("1) Português (Brasil)")
    print("2) English")
    print()

    lang_choice = input(
        "Selecione o idioma / Select language: "
    ).strip()

    if lang_choice == "2":
        lang = {
            "processing": "Processing",
            "success": "Successfully converted",
            "failed": "Conversion failed",
            "missing": "Referenced files not found",
            "found": "Games found",
            "none": "No games found",
            "keep": "Keep original files after conversion?",
            "yes": "Yes",
            "no": "No",
            "done": "Process completed",
            "total": "Total converted",
            "exit": "Press Enter to exit..."
        }
    else:
        lang = {
            "processing": "Processando",
            "success": "Convertido com sucesso",
            "failed": "Falha na conversão",
            "missing": "Arquivos referenciados não encontrados",
            "found": "Jogos encontrados",
            "none": "Nenhum jogo encontrado",
            "keep": "Deseja manter os arquivos originais após a conversão?",
            "yes": "Sim",
            "no": "Não",
            "done": "Processo concluído",
            "total": "Total convertidos",
            "exit": "Pressione Enter para sair..."
        }

    print()
    print(lang["keep"])
    print()
    print(f"1) {lang['yes']}")
    print(f"2) {lang['no']}")
    print()

    keep_originals = input("> ").strip() == "1"

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cue_files = sorted(INPUT_DIR.glob("*.cue"))

    if not cue_files:
        print()
        print(lang["none"])
        return

    total = len(cue_files)

    print()
    print(f"{lang['found']}: {total}")

    converted = 0

    for index, cue_file in enumerate(cue_files, start=1):

        if convert_game(
            cue_file,
            keep_originals,
            lang
        ):
            converted += 1

        progress_bar(index, total)

    print("=" * 40)
    print(f"{lang['total']}: {converted}/{total}")
    print(lang["done"])
    print("=" * 40)

    input(f"\n{lang['exit']}")


if __name__ == "__main__":
    main()
