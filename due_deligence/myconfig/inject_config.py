from copy import copy
import inject

from due_deligence.domain_model.document import DocumentService
from due_deligence.adapter.document import SimpleDocumentService
from due_deligence.domain_model.deligence import DeligenceService
from due_deligence.adapter.deligence import SimpleDeligenceService, XbrlDownloader
from due_deligence.domain_model.stock import StockService
from due_deligence.adapter.stock import SimpleStockService
from due_deligence.adapter.http.xbrl_obj_downloader import XbrlObjDownloader
from due_deligence.controller.dd_controller import ResultPresenter, ResultFilter
from due_deligence.adapter.presenter.result_screen_presenter import ResultScreenPresenter
from due_deligence.adapter.presenter.result_json_presenter import ResultJsonPresenter
from due_deligence.adapter.presenter.result_today_recommend_presenter import ResultTodayRecommendPresenter
from due_deligence.util.progress_presenter import ProgressPresenter
from due_deligence.adapter.presenter.cli_progress_presenter import CliProgressPresenter
from due_deligence.adapter.presenter.null_progress_presenter import NullProgressPresenter
from due_deligence.adapter.http.requests import Requests
from due_deligence.adapter.http.cache_requests import CacheRequests

__DEFAULT_OUTPUT_FILEPATH = './due_deligence'

__output_path = ''
__format = ''
__is_cli = False
__is_cache = False


def init_injection(output_path='', format_type='', is_cli=False, is_cache=False):
    global __output_path, __format, __is_cli, __is_cache
    __output_path = output_path
    __format = format_type
    __is_cli = is_cli
    __is_cache = is_cache
    inject.configure(config)


def config(binder):
    binder.bind_to_constructor(DocumentService, SimpleDocumentService)
    binder.bind_to_constructor(DeligenceService, SimpleDeligenceService)
    binder.bind_to_constructor(StockService, SimpleStockService)
    binder.bind_to_constructor(XbrlDownloader, XbrlObjDownloader)
    if __format == 'screen':
        binder.bind_to_constructor(ResultPresenter, ResultScreenPresenter)
    elif __format == 'json':
        path = __output_path if len(
            __output_path) > 0 else __DEFAULT_OUTPUT_FILEPATH + '.json'
        binder.bind(ResultPresenter, ResultJsonPresenter(path))
    # 指定されたパスへのcsvやjson出力にも対応させる。
    if __is_cli:
        binder.bind_to_constructor(ProgressPresenter, CliProgressPresenter)
    else:
        binder.bind_to_constructor(ProgressPresenter, NullProgressPresenter)
    if __is_cache:
        binder.bind(Requests, CacheRequests(wait_time=2))
