from due_deligence.util.progress_presenter import ProgressPresenter


class NullProgressPresenter(ProgressPresenter):
    def print(self, *value) -> None:
        pass

    def wrap_tqdm(self, range_value: range) -> range:
        return range_value
