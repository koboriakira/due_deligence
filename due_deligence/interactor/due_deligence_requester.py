from abc import ABCMeta, abstractmethod

class DueDeligenceRequester(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def search(self, start_date, end_date):
    raise NotImplementedError
