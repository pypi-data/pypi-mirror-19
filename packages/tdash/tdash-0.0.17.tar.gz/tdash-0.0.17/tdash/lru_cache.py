import operator
import functools
import warnings

class LRUCache(object):
    def __init__(self, size, provider_func, on_evicted_func=None, on_entry_func=None):
        """
        :param size: size of cache
        :type size: int
        :param provider_func: gets the value if missing from cache of will be called with the regular key
                              ie func(key) and should return value.
        :type provider_func: func if None then do nothing
        :param on_evicted_func: gets called on the key, value when being removed from the cache.
                               ie func(key, value). whatever it returns is not used.
        :type on_evicted_func: func
        :param on_entry_func: gets called when function is entered into the cache via func(key, value).
                              if None does nothing
        :type on_entry_func: func
        """
        self._size = size
        self._counter = 0
        self._provider_func = provider_func
        self._on_evicted_func = functools.partial(call_func_if_not_none, on_evicted_func)
        self._on_entry_func = functools.partial(call_func_if_not_none, on_entry_func)

        self._values = {}
        self._access_history = {}

    def __getitem__(self, key):
        self._note_access(key)
        try:
            return self._values[key]
        except KeyError:
            return self._populate_missing(key)

    def __setitem__(self, key, value):
        self._on_entry_func(key, value)
        self._note_access(key)
        self._values[key] = value
        self._evict_lru_if_applicable()

    def __len__(self):
        return len(self._values)

    def _populate_missing(self, key):
        self._values[key] = self._provider_func(key)
        self._evict_lru_if_applicable()
        return self._values[key]

    def _evict_lru_if_applicable(self):
        if len(self) > self._size:
            lru_key, _ = min(self._access_history.items(), key=operator.itemgetter(1))
            failed = False
            # TODO: check if two equal sized item what happens.
            # TODO synchronise this function to stop multiple threads.
            #TODO (cont): see https://github.com/GrahamDumpleton/wrapt/blob/develop/blog/07-the-missing-synchronized-decorator.md

            try:
                lru_val = self._values.pop(lru_key)
            except KeyError:
                failed = True
                warnings.warn('Cannot find key %s in values. Values keys are \n %s. \n Access History items are \n %s' % (
                    str(lru_key), str(self._values.keys()), str(self._access_history.items())))

            try:
                del self._access_history[lru_key]
            except KeyError:
                warnings.warn(
                    'Cannot find key %s in access history. Values keys are \n %s. \n Access History items are \n %s' % (
                        str(lru_key), str(self._values.keys()), str(self._access_history.items())))

            # Do this last if possible as may take some time.
            if not failed:
                self._on_evicted_func(lru_key, lru_val)

    def _note_access(self, key):
        self._access_history[key] = self._get_counter_and_increase_by_one()

    def _get_counter_and_increase_by_one(self):
        old_counter = self._counter
        self._counter += 1
        return old_counter


def call_func_if_not_none(func, *args, **kwargs):
    if func is not None:
        return func(*args, **kwargs)


