def get_classification(struct: dict) -> str:
    obs_alert, mod_alert = struct["obs_alert"], struct["mod_alert"]
    if obs_alert == 0 and mod_alert == 0:
        return "TN"
    elif obs_alert > 0 and mod_alert == 0:
        return "FN"
    elif mod_alert > 0 and mod_alert > 0:
        return "FP"
    elif obs_alert > 0 and mod_alert > 0:
        return "TP"

