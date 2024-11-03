import subprocess
from subprocess import PIPE
import shlex
from logs.logging_config import app_logger

class PageLoader:
    def load_page(self, url):
        app_logger.info(f"Загрузка страницы {url}")
        try:
            cmd = f"curl -s {shlex.quote(url)}"
            valid_command = shlex.split(cmd)

            process = subprocess.Popen(
                valid_command,
                stdout=PIPE,
                stderr=PIPE
            )

            stdout, stderr = process.communicate()
            app_logger.info(f"Страница успешно загружена!")
            return stdout.decode('utf-8'), stderr.decode('utf-8')


        except Exception as exc:
            app_logger.error(f"Ошибка при загрузке страницы {url}: {exc}")