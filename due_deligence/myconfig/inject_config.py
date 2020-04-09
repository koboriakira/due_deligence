from copy import copy
import inject

from due_deligence.adapter.document import DocumentRepository
from due_deligence.adapter.repo.document.document_mysql_repository import DocumentMysqlRepository
from due_deligence.domain_model.document import DocumentService
from due_deligence.adapter.document import SimpleDocumentService
from due_deligence.domain_model.deligence import DeligenceService
from due_deligence.adapter.deligence import SimpleDeligenceService
from due_deligence.adapter.deligence import XbrlDownloader, ReportRepository
from due_deligence.adapter.http.xbrl_obj_downloader import XbrlObjDownloader
from due_deligence.adapter.repo.deligence.report_mysql_repository import ReportMysqlRepository
from due_deligence.controller.dd_controller import ResultPresenter
from due_deligence.adapter.presenter.result_screen_presenter import ResultScreenPresenter


def init_injection():
    inject.configure(config)


def config(binder):
    binder.bind_to_constructor(DocumentService, SimpleDocumentService)
    binder.bind_to_constructor(DeligenceService, SimpleDeligenceService)
    binder.bind_to_constructor(XbrlDownloader, XbrlObjDownloader)
    binder.bind_to_constructor(ReportRepository, ReportMysqlRepository)
    binder.bind_to_constructor(ResultPresenter, ResultScreenPresenter)
    binder.bind_to_constructor(DocumentRepository, DocumentMysqlRepository)
