from due_deligence.util.progress_presenter import ProgressPresenter
from tqdm import tqdm


class CliProgressPresenter(ProgressPresenter):
    def print(self, *value) -> None:
        for val in value:
            print(val, sep=' ')

    def wrap_tqdm(self, range_value: range) -> range:
        return tqdm(range_value)
