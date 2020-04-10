from abc import ABCMeta, abstractmethod


class ProgressPresenter(object):
    @abstractmethod
    def print(self, *value) -> None:
        raise NotImplementedError

    def wrap_tqdm(self, range_value: range) -> range:
        raise NotImplementedError
