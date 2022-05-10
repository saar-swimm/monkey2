from common.common_consts.post_breach_consts import POST_BREACH_TIMESTOMPING
from monkey_island.cc.services.attack.technique_reports.pba_technique import PostBreachTechnique


class T1099(PostBreachTechnique):
    tech_id = "T1099"
    relevant_systems = ["Linux", "Windows"]
    unscanned_msg = "Monkey didn't try changing any file's time attributes."
    scanned_msg = "Monkey tried changing a file's time attributes but failed."
    used_msg = "Monkey successfully changed a file's time attributes."
    pba_names = [POST_BREACH_TIMESTOMPING]
