import subprocess, os, random
from datetime import datetime, timedelta

# ===============================
# KONFIG
# ===============================
REPO_DIR = "."       # ganti kalau repo bukan di sini
TZ = "+07:00"
YEAR = 2023

# warna tebal (bagian labu)
MIN_COMMITS_HOT = 18
MAX_COMMITS_HOT = 35

# warna tipis / background
MIN_COMMITS_COLD = 0
MAX_COMMITS_COLD = 1

# ===============================
# POLA LABU 🎃
# 7 baris (Minggu -> Sabtu)
# 53 kolom (1 tahun di GitHub)
# '#' = bikin banyak commit
# '.' = kosong / tipis
# ===============================
PATTERN = [
    "...................###############...................",  # 0 Minggu (atas)
    "..............#########################..............",  # 1 Senin
    "..........#####....###############....#####..........",  # 2 mata kiri/kanan
    ".........################...################.........",  # 3 hidung
    "..........####..#.....#.....#.....#....####..........",  # 4 mulut (gigi)
    "............####.....................####............",  # 5 garis mulut bawah
    "................#####################................",  # 6 paling bawah
]

# semua baris harus 53
assert all(len(r) == 53 for r in PATTERN)

def make_commits_at(date_obj, num_commits, repo_dir, tz):
    env_base = os.environ.copy()
    for i in range(num_commits):
        # bikin jam random biar natural
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


# 1 Jan 2023 = Minggu → pas ke row 0
start_date = datetime(YEAR, 1, 1)

for week in range(53):          # kolom
    for dow in range(7):        # baris: 0=Min..6=Sab
        ch = PATTERN[dow][week]
        current_date = start_date + timedelta(weeks=week, days=dow)

        # kalau nyebrang ke 2024, skip
        if current_date.year != YEAR:
            continue

        if ch == "#":
            n = random.randint(MIN_COMMITS_HOT, MAX_COMMITS_HOT)
        else:
            n = random.randint(MIN_COMMITS_COLD, MAX_COMMITS_COLD)

        if n > 0:
            make_commits_at(current_date, n, REPO_DIR, TZ)
