import re


class TasksManager(object):
    def __init__(self):
        self._total_pool = set()
        self._downloaded = set()

    def fetch_one_task(self):
        # print(self.print_progress())
        diff = self._total_pool - self._downloaded
        if len(diff) > 0:
            return diff.pop()
        else:
            return

    def add_task(self, task):
        if task not in self._total_pool:
            self._total_pool.add(task)
            return 1
        return 0

    def add_tasks(self, tasks):
        old_cnt = len(self._total_pool)
        self._total_pool.update(tasks)
        new_cnt = len(self._total_pool)
        return new_cnt - old_cnt

    def mark_task_done(self, task):
        self._downloaded.add(task)

    def mark_tasks_done(self, tasks):
        self._downloaded.update(tasks)

    def progress(self):
        total = len(self._total_pool)
        done = len(self._downloaded)
        return {
            'total': total,
            'done': done,
            'todo': total - done,
        }

    def print_progress(self):
        print('=== total: %(total)s, done: %(done)s, todo: %(todo)s' % self.progress())


class AlbumTasksManager(TasksManager):

    task_ptn = re.compile(r'https://www.lanvshen.com/a/(\d+)/?')

    def find_tasks(self, text):
        return set(self.task_ptn.findall(text))

    def feed_tasks(self, text):
        tasks = self.find_tasks(text)
        # print(tasks)
        added = self.add_tasks(tasks)
        print('%s tasks found, %s new' % (len(tasks), added))
