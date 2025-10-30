import subprocess, os, random
from datetime import datetime, timedelta

# ====== KONFIGURASI ======
REPO_DIR = "."  # ganti ke path repo kamu kalau perlu
tz = "+07:00"   # timezone Jakarta

start_date = datetime(2023, 2, 1)  # mulai commit dari tanggal ini
end_date   = datetime(2023, 2, 7)  # sampai tanggal ini (ikut / inclusive)

# per hari mau berapa commit? bisa angka, bisa random di range
MIN_COMMITS_PER_DAY = 1
MAX_COMMITS_PER_DAY = 3
# =========================

current = start_date
env_base = os.environ.copy()

while current <= end_date:
    # tentukan berapa commit hari ini
    n_commits = random.randint(MIN_COMMITS_PER_DAY, MAX_COMMITS_PER_DAY)

    for i in range(n_commits):
        # bikin jam random dalam hari itu (0–23), dan menit/detik random
        hour = random.randint(8, 18)      # biar kelihatan jam kerja
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        commit_time = datetime(
            current.year,
            current.month,
            current.day,
            hour,
            minute,
            second
        )

        iso = commit_time.strftime(f"%Y-%m-%dT%H:%M:%S{tz}")

        env = env_base.copy()
        env["GIT_AUTHOR_DATE"] = iso
        env["GIT_COMMITTER_DATE"] = iso

        msg = f"chore: auto commit at {iso}"
        print(f"→ commit {msg}")

        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", msg],
            cwd=REPO_DIR,
            check=True,
            env=env
        )

    # lanjut ke hari berikutnya
    current += timedelta(days=1)
