import subprocess, os
from datetime import datetime

commit_time = datetime(2025,10,8,8,0,0)
iso = commit_time.strftime("%Y-%m-%dT%H:%M:%S+07:00")

env = os.environ.copy()
env["GIT_AUTHOR_DATE"] = iso
env["GIT_COMMITTER_DATE"] = iso

subprocess.run(["git", "commit", "--allow-empty", "-m", f"Empty commit at {iso}"], cwd=".", check=True, env=env)
