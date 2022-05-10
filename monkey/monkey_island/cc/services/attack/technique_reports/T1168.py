from common.common_consts.post_breach_consts import POST_BREACH_JOB_SCHEDULING
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1168(PostBreachTechnique):
    tech_id = "T1168"
    relevant_systems = ["Linux"]
    unscanned_msg = "Monkey didn't try scheduling a job on Linux."
    scanned_msg = "Monkey tried scheduling a job on the Linux system but failed."
    used_msg = "Monkey scheduled a job on the Linux system."
    pba_names = [POST_BREACH_JOB_SCHEDULING]
