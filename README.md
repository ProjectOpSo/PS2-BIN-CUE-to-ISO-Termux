# PS2-BIN-CUE-to-ISO-Termux

Convert PlayStation 2 BIN/CUE images to ISO format directly on Android using Termux and bchunk.

## Features

* Batch conversion of BIN/CUE images to ISO.
* Automatically creates input and output directories.
* Parses CUE files and validates referenced BIN files.
* Supports long filenames, spaces, and special characters.
* Moves generated ISO files to the destination folder.
* Choose whether to keep or delete original BIN/CUE files after successful conversion.
* Progress bar with percentage indicator.
* Portuguese (Brazil) and English language support.
* Lightweight and easy to use.

## Requirements

* Android device
* Termux
* Python 3
* bchunk

## Installation

### 1. Update Termux
```bash
pkg update -y && pkg upgrade -y
```

### 2. Initial Termux Configuration
Grant Termux access to internal storage:
```bash
termux-setup-storage
```
Note: Accept the permission prompt to allow access to your Download folder.

### 3. install Python | Git
```bash
pkg install python -y && pkg install git -y
```

### 4. Install bchunk
```bash
pkg install bchunk -y
```
### 5. Clone Repository
```bash
git clone https://github.com/ProjectOpSo/PS2-BIN-CUE-to-ISO-Termux.git
cd PS2-BIN-CUE-to-ISO-Termux
```

## Directory Structure

Place your BIN/CUE files in:
* `/storage/emulated/0/Download/PS2-BINJ`

Converted ISO files will be saved to:
* `/storage/emulated/0/Download/PS2-ISO`

### Example
```text
Download/
├── PS2-BINJ/
│   ├── Crash Bandicoot - The Wrath of Cortex (USA) (v1.01).cue
│   ├── Crash Bandicoot - The Wrath of Cortex (USA) (v1.01).bin
│   ├── Resident Evil - Dead Aim.cue
│   └── Resident Evil - Dead Aim.bin
│
└── PS2-ISO/
```

## Usage

Run the script:
```bash
python ps2_binj_converter.py
```

### What Happens
The script will ask two questions:

1. **Language Selection**
   * Português (Brasil)
   * English

2. **File Handling Preference**
   * Keep original BIN/CUE files
   * Delete original BIN/CUE files after successful conversion

### Process Flow
1. The script scans the PS2-BINJ folder.
2. Every CUE file found is analyzed.
3. Referenced BIN files are verified.
4. bchunk converts the image to ISO.
5. The generated ISO is moved to PS2-ISO.
6. Original files are kept or removed according to your selection.
7. Progress is displayed after every conversion.

## Example Output

```text
========================================
         PS2 BIN/CUE Converter
========================================

Games found: 2

========================================
Processing: Crash Bandicoot - The Wrath of Cortex
========================================

✓ Successfully converted

[██████████░░░░░░░░░░] 50%

========================================
Processing: Resident Evil - Dead Aim
========================================

✓ Successfully converted

[████████████████████] 100%

========================================
Total converted: 2/2
Process completed
========================================
```

## Notes

> [!IMPORTANT]
> The script uses bchunk for conversion. Make sure all BIN files referenced by the CUE file are present inside the PS2-BINJ directory before starting the conversion.

> [!NOTE]
> Multi-track disc images are validated through the CUE file before conversion.

## Compatibility

* PlayStation 2 CD images (.bin + .cue)
* Android (Termux)
* Python 3
* bchunk
