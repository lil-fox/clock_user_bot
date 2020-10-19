from crontab import CronTab
import config


class CommandHandler:

    def __init__(self):
        self._crontab = CronTab(user=True)
        self._handlers = {
            'activate': self._activate,
            'deactivate': self._deactivate
        }

    def handle(self, command):
        handler = self._handlers.get(command)
        if handler:
            handler()

    def _activate(self):
        self._deactivate()
        job = self._crontab.new(command=f"cd {config.DIR_PATH} && ./app.py",
                                comment=config.BOT_ID)

        job.minute.every(1)
        self._crontab.write()

    def _deactivate(self):
        job = self._crontab.find_comment(config.BOT_ID)
        self._crontab.remove(job)
        self._crontab.write()
