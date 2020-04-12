from datetime import date
import inject
import logging

from due_deligence.controller import dd_controller
from due_deligence.myconfig import inject_config

logging.basicConfig(level=logging.DEBUG)

inject_config.init_injection(
    format_type='screen', is_cli=True, is_cache=True, output_path='test.json')

from_date = date.fromisoformat('2020-04-10')
end_date = date.fromisoformat('2020-04-10')
controller = dd_controller.DDController(from_date=from_date, end_date=end_date)
result = controller.execute()

presenter = inject.instance(dd_controller.ResultPresenter)
presenter.print(result)
