import os

import dotenv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit
from .elements import TitleLabel, SubtitleLabel, InputElement, SubmitButton, LogPanel
from .runner import ScriptRunner

dotenv.load_dotenv(override=True)

class ReviewCommitsGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('בודקומיטר - Git Outta here')
        self.setMinimumWidth(600)
        self.init_ui()
        self.runner = None

    def init_ui(self):
        title = TitleLabel('בודקומיטר')
        subtitle = SubtitleLabel('Git Outta here')

        gitlab_token = os.getenv('GITLAB_TOKEN')
        groq_token = os.getenv('GROQ_API_KEY')
        form_layout = QFormLayout()

        self.gitlab_token_input = InputElement('GITLAB TOKEN')
        self.gitlab_token_input.setEchoMode(QLineEdit.EchoMode.Password)

        if gitlab_token:
            self.gitlab_token_input.setText(gitlab_token)

        form_layout.addRow('GitLab Token:', self.gitlab_token_input)

        self.groq_token_input = InputElement('GROQ API TOKEN')
        self.groq_token_input.setEchoMode(QLineEdit.EchoMode.Password)

        if groq_token:
            self.groq_token_input.setText(groq_token)

        form_layout.addRow('Groq API Token:', self.groq_token_input)

        self.project_url_input = InputElement('Project URL')
        form_layout.addRow('Project URL:', self.project_url_input)

        self.min_commits_input = InputElement('Min commits')
        form_layout.addRow('Min commits: ', self.min_commits_input)

        self.max_commits_input = InputElement('Max commits')
        form_layout.addRow('Max commitsL: ', self.max_commits_input)

        self.submit_btn = SubmitButton('בדוק קומיטים')
        self.submit_btn.clicked.connect(self.run_script)

        self.log_panel = LogPanel()

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(form_layout)
        layout.addWidget(self.submit_btn)
        layout.addWidget(QLabel('לוג:'))
        layout.addWidget(self.log_panel)
        self.setLayout(layout)

    def run_script(self):
        gitlab_token = self.gitlab_token_input.text().strip()
        groq_token = self.groq_token_input.text().strip()
        project_url = self.project_url_input.text().strip()
        min_commits = int(self.min_commits_input.text().strip())
        max_commits = int(self.max_commits_input.text().strip())

        if not (gitlab_token and groq_token and project_url):
            self.log_panel.append('נא למלא את כל השדות.\n')
            return

        self.log_panel.clear()
        self.submit_btn.setEnabled(False)
        self.runner = ScriptRunner(gitlab_token, groq_token, project_url, min_commits, max_commits)
        self.runner.log_signal.connect(self.log_panel.append)
        self.runner.finished_signal.connect(lambda: self.submit_btn.setEnabled(True))
        self.runner.start()
