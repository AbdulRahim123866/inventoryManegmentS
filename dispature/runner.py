from api.messaging import construct_mailer
from constant.const import APP_NAME
from controllers.core import AppController
from models.db import get_db_hook
from models.models import BASE
from views.login import LoginForm
from utilities.log_svc_client import get_logger
from controllers.utils import load_json

class CoreDispatcher:
    def __init__(self,args,app=None):
        self._args=args
        self._app=app
        # connection,factory=get_db_hook(
        #     config=load_json(args.config),
        #     create=True,
        #     base=BASE,
        # )
        cfg = load_json(args.config)

        connection, factory = get_db_hook(
            config=cfg["database"],
            create=True,
            base=BASE,
        )

        self._logger=get_logger(
            service_name=APP_NAME,
            path=args.config

        )
        AppController.set_mailer(
            construct_mailer(path=args.config,
                             logger=self._logger))

        AppController.set_logger(self._logger)
        AppController.set_connection(connection,factory)



    def start(self):
        AppController.LOGGER.info('form started ')

        self.form=LoginForm()
        self.form.show()