# Purwadhika-capstone-project-2
Purwadhika-capstone project 2

# Patient & Visit Management System

A command-line application for managing patient records and clinic visit schedules, built in Python as **Capstone Project 2** of the *Job Connector Bootcamp Business & Data Analyst* at [Purwadhika Digital Technology School](https://purwadhika.com) (class JCBDAAH-003).

The application lets clinic staff register patients, schedule visits by clinic and doctor, search and update records, and keep all data saved between sessions. The user interface (menus and prompts) is in Indonesian.

## Features

**Patient management**
- Add, view, update, and delete patient records
- Automatic patient IDs in the format `PSN0001`, `PSN0002`, ...
- National ID (No. KTP) validation: exactly 16 digits, numbers only
- Duplicate protection: a National ID cannot be registered twice, both when adding and when editing a patient
- Update a single field (name, National ID, age, address, or gender) with a confirmation step before saving
- Age is limited to 0-120 and gender must be entered as L or P
- Search a patient by ID

**Visit scheduling**
- Create visit schedules by choosing a patient, date, clinic, and doctor
- The patient ID must exist, and dates are validated and normalized to `YYYY-MM-DD` when scheduling, editing, and searching visits (for example, `2025-8-27` becomes `2025-08-27`)
- Visit IDs are based on the highest existing ID, so they never repeat after a visit is deleted
- Clinic and doctor choices are range-checked, and numeric inputs are validated so the program does not crash on invalid entries
- 5 clinics (General, Dental, Pediatrics, Cardiology, Neurology), each with 2 doctors
- View all visits, or search by visit ID, clinic, or date
- Update the date, clinic, or doctor of an existing visit, with confirmation
- Delete a visit with confirmation

**Data integrity and storage**
- Deleting a patient also removes all of that patient's visits
- All data is saved automatically to a JSON file (`data_pasien.json`) after every change
- On first run, the program creates the file with sample data (5 patients and 1 visit), so it can be tried immediately

## Tech Stack

- Python 3
- Standard library only (`json`, `os`), no external packages required

## Getting Started

1. Make sure Python 3 is installed:
   ```bash
   python --version
   ```
2. Clone this repository:
   ```bash
   git clone https://github.com/raharjaganjar1103/Purwadhika-capstone-project-2.git
   cd Purwadhika-capstone-project-2
   ```
3. Run the program:
   ```bash
   python "Capstone Project 2 JCBDAAH-003 Ganjar Raharja.py"
   ```

## Usage

The program opens with a main menu:

```
=== Sistem Data Pasien ===

1. Lihat Data
2. Tambah Pasien / Kunjungan
3. Ubah Pasien / Kunjungan
4. Hapus Pasien / Kunjungan
0. Keluar
```

| Menu | What it does |
|---|---|
| 1. Lihat Data | View all patients or one patient by ID; view all visits or filter by ID, clinic, or date |
| 2. Tambah | Register a new patient or schedule a new visit |
| 3. Ubah | Edit patient details or visit details |
| 4. Hapus | Delete a patient (and their visits) or a single visit |
| 0. Keluar | Exit the program |

## Data Structure

Data is stored in `data_pasien.json` with two lists.

**Patients:** `[patient ID, name, National ID, age, address, gender]`

```json
["PSN0001", "Andi", "1234567890123456", 30, "Jakarta", "Laki-laki"]
```

**Visits:** `[visit ID, patient ID, date, clinic ID, doctor]`

```json
[1, "PSN0005", "2025-08-27", 1, "Dr. Agung"]
```

To reset the application to its sample data, delete `data_pasien.json` and run the program again.

## Future Improvements

- Replace JSON file storage with a SQL database
- Add a time slot to each visit

## Author

**Ganjar Raharja**
Purwadhika Job Connector Bootcamp Business & Data Analyst, class JCBDAAH-003
