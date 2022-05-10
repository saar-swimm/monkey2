import http.client

import flask_restful
from flask import jsonify

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.zero_trust.zero_trust_report.finding_service import FindingService
from monkey_island.cc.services.zero_trust.zero_trust_report.pillar_service import PillarService
from monkey_island.cc.services.zero_trust.zero_trust_report.principle_service import (
    PrincipleService,
)

REPORT_DATA_PILLARS = "pillars"
REPORT_DATA_FINDINGS = "findings"
REPORT_DATA_PRINCIPLES_STATUS = "principles"


class ZeroTrustReport(flask_restful.Resource):
    @jwt_required
    def get(self, report_data=None):
        if report_data == REPORT_DATA_PILLARS:
            return jsonify(PillarService.get_pillar_report_data())
        elif report_data == REPORT_DATA_PRINCIPLES_STATUS:
            return jsonify(PrincipleService.get_principles_status())
        elif report_data == REPORT_DATA_FINDINGS:
            return jsonify(FindingService.get_all_findings_for_ui())

        flask_restful.abort(http.client.NOT_FOUND)
