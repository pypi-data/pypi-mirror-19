from NucleusUtils.events import Event

from NucleusApp.chest.exceptions import LockError

ROOT_MARK = '$'
TEMP_MARK = '#'


class Container:
    def __init__(self, name, chest=None):
        self.name = name
        self.chest = chest

        self.__locked = False
        self.__data = {}

        self.on_put = Event(name=str(self) + ':on_put', threaded=not name.startswith(ROOT_MARK))
        self.on_get = Event(name=str(self) + ':on_get', threaded=not name.startswith(ROOT_MARK))
        self.on_drop = Event(name=str(self) + ':on_drop', threaded=not name.startswith(ROOT_MARK))

        if self.name.startswith(TEMP_MARK):
            self.lock()

    def put(self, name, value):
        if self.__locked:
            raise LockError(self.name)
        self.__data[name] = value
        self.on_put(name, value)

    def get(self, name, default=None):
        self.on_get(name, self.__data.get(name, default))
        return self.__data.get(name, default)

    def drop(self, name):
        """
        Drop element by name
        :param name:
        :return:
        """
        if self.is_locked():
            raise LockError(self.name)
        del self.__data[name]
        self.on_drop(name)

    def clear(self):
        """
        Clear container
        :return:
        """
        if self.is_locked():
            raise LockError(self.name)
        self.__data.clear()

    def lock_forever(self):
        """
        Unsafe method! Not recommended to use this method!
        :return:
        """
        self.lock()
        self.__dict__['__orig_unlock'] = self.unlock
        self.unlock = None

    def lock(self):
        self.__locked = True

    def unlock(self):
        self.__locked = False

    def is_locked(self):
        return self.__locked

    def items(self):
        return self.__data.items()

    def __enter__(self):
        if self.name.startswith(TEMP_MARK):
            self.unlock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.name.startswith(TEMP_MARK):
            self.lock()
            self.clear()
            if self.chest:
                self.chest.destroy(self.name)

    def __call__(self, name, default=None):
        return self.get(name, default)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __delitem__(self, key):
        self.drop(key)

    def __iter__(self):
        return self.__data.items()

    def __str__(self):
        if self.is_locked():
            lock_status = ':locked'
        else:
            lock_status = ''

        if self.chest:
            chest = str(self.chest) + '.'
        else:
            chest = ''
        return f"Container: {chest}{self.name}({len(self)}){lock_status}"

    def __len__(self):
        return len(self.__data)
