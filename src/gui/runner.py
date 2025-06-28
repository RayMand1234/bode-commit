import dotenv
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
import sys
import os

class ScriptRunner(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, gitlab_token, groq_token, project_url, min_commits, max_commits):
        super().__init__()
        self.gitlab_token = gitlab_token
        self.groq_token = groq_token
        self.project_url = project_url
        self.min_commits = min_commits
        self.max_commits = max_commits

    def run(self):
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')

        print(env_path)

        dotenv.set_key(env_path, key_to_set='GITLAB_TOKEN', value_to_set=self.gitlab_token)
        dotenv.set_key(env_path, key_to_set='GROQ_API_KEY', value_to_set=self.groq_token)

        process = subprocess.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__), '../main.py'), self.project_url, self.min_commits, self.max_commits],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        try:
            for line in process.stdout:
                self.log_signal.emit(line)
        except Exception as e:
            self.log_signal.emit(f'Error: {e}\n')
        finally:
            process.stdout.close()
            process.wait()
            self.finished_signal.emit() 