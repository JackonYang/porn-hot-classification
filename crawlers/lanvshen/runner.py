from album_mng import AlbumTasksManager
from download_album import fetch_album


def main(inital_album_id):
    task_manager = AlbumTasksManager()

    task_manager.add_task(inital_album_id)

    while True:
        album_id = task_manager.fetch_one_task()
        if album_id is None:
            return

        print('start downloading album_id: %s' % album_id)
        fetch_album(album_id, task_manager)
        task_manager.mark_task_done(album_id)
        task_manager.print_progress()


if __name__ == '__main__':
    # main('31266')
    # main('32322')
    main('17694')
