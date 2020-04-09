from abc import ABCMeta, abstractmethod

class AnalyzeRequestor(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def analyze_company(self, company_list):
    raise NotImplementedError

  @abstractmethod
  def analyze_company_list(self, company_list):
    raise NotImplementedError
