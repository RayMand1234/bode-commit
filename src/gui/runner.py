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

    def run(self):
        env = os.environ.copy()
        env['GITLAB_TOKEN'] = self.gitlab_token
        env['GROQ_API_KEY'] = self.groq_token
        process = subprocess.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__), '../main.py')],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            text=True
        )
        try:
            process.stdin.write(self.project_url + '\n')
            process.stdin.flush()
            for line in process.stdout:
                self.log_signal.emit(line)
        except Exception as e:
            self.log_signal.emit(f'Error: {e}\n')
        finally:
            process.stdin.close()
            process.stdout.close()
            process.wait()
            self.finished_signal.emit() 