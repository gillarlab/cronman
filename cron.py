#!/usr/bin/python3

from crontab import CronTab, CronItem


class Cron(CronTab):
    def __init__(self, user='root'):
        super().__init__(user=user)

    def tasks(self):
        return [self.__item_str(item) for item in self]

    def enable(self, no: int, enabled: bool = True) -> bool:
        if 0 <= no < len(self):
            self[no].enable(enabled)
            self.write()
            return True
        else:
            return False

    def disable(self, no: int) -> bool:
        return self.enable(no, False)

    @staticmethod
    def __item_str(item: CronItem):
        return {
            'valid':        item.is_valid(),
            'enabled':      item.is_enabled(),
            'comment':      item.comment,
            'command':      item.command,
            'schedule':     str(item.slices),
        }


if __name__ == '__main__':
    pass
