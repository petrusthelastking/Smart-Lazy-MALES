import subprocess, os, random
from datetime import datetime, timedelta

# =========================================
# KONFIGURASI
# =========================================
REPO_DIR = "."          # ganti kalau repo-nya bukan di folder ini
TZ = "+07:00"           # timezone buat GIT_AUTHOR_DATE
YEAR = 2023             # kita gambar di tahun 2023

# jumlah commit untuk sel yg MENYALA (#)
MIN_COMMITS_HOT = 15
MAX_COMMITS_HOT = 30

# jumlah commit untuk sel yg MATI (.)
MIN_COMMITS_COLD = 0
MAX_COMMITS_COLD = 1

# =========================================
# POLA LABU (53 kolom = 53 minggu, 7 baris = Minggu..Sabtu)
# tiap string = 53 karakter
# karakter:
#   '#' = bikin banyak commit
#   '.' = kosong / sedikit commit
# kamu boleh ngedit pola ini nanti biar lebih cakep
# =========================================
PATTERN = [
    ".......................#######.......................",  # row 0 (Minggu)
    ".....................###########.....................",  # row 1 (Senin)
    "....................#############....................",  # row 2 (Selasa)
    "....................#############....................",  # row 3 (Rabu)
    ".....................###########.....................",  # row 4 (Kamis)
    "......................#########......................",  # row 5 (Jumat)
    "........................#####........................",  # row 6 (Sabtu)
]
# cek panjang pola
assert all(len(row) == 53 for row in PATTERN), "Semua baris harus 53 kolom!"

# =========================================
# FUNGSI BIKIN COMMIT DI TANGGAL TERTENTU
# =========================================
def make_commits_at(date_obj, num_commits, repo_dir, tz):
    env_base = os.environ.copy()
    for i in range(num_commits):
        # biar natural: jam random 08:00–18:00
        hour = random.randint(8, 18)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        commit_time = datetime(
            date_obj.year,
            date_obj.month,
            date_obj.day,
            hour,
            minute,
            second
        )
        iso = commit_time.strftime(f"%Y-%m-%dT%H:%M:%S{tz}")

        env = env_base.copy()
        env["GIT_AUTHOR_DATE"] = iso
        env["GIT_COMMITTER_DATE"] = iso

        msg = f"chore(pumpkin): {iso}"
        print(f"→ commit {msg}")
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", msg],
            cwd=repo_dir,
            check=True,
            env=env
        )


# =========================================
# MULAI DARI MINGGU PERTAMA TAHUN 2023
# 1 Jan 2023 = Minggu → pas dengan row 0
# =========================================
start_date = datetime(YEAR, 1, 1)

# loop 53 minggu (53 kolom)
for week in range(53):
    for day_of_week in range(7):  # 0 = Minggu, 6 = Sabtu
        char = PATTERN[day_of_week][week]
        current_date = start_date + timedelta(weeks=week, days=day_of_week)

        # kalau sudah lewat tahun ini (misal 2023 nggak sampai full 53 kolom),
        # boleh di-skip supaya ga nabrak 2024
        if current_date.year != YEAR:
            continue

        if char == "#":
            n_commits = random.randint(MIN_COMMITS_HOT, MAX_COMMITS_HOT)
        else:
            n_commits = random.randint(MIN_COMMITS_COLD, MAX_COMMITS_COLD)

        if n_commits > 0:
            make_commits_at(current_date, n_commits, REPO_DIR, TZ)
