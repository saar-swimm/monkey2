import logging

from monkey_island.cc.services import aws_service
from monkey_island.cc.services.reporting.aws_exporter import AWSExporter
from monkey_island.cc.services.reporting.report_exporter_manager import ReportExporterManager

logger = logging.getLogger(__name__)


def populate_exporter_list():
    manager = ReportExporterManager()
    try_add_aws_exporter_to_manager(manager)

    if len(manager.get_exporters_list()) != 0:
        logger.debug(
            "Populated exporters list with the following exporters: {0}".format(
                str(manager.get_exporters_list())
            )
        )


def try_add_aws_exporter_to_manager(manager):
    # noinspection PyBroadException
    try:
        if aws_service.is_on_aws():
            manager.add_exporter_to_list(AWSExporter)
    except Exception:
        logger.error("Failed adding aws exporter to manager. Exception info:", exc_info=True)
