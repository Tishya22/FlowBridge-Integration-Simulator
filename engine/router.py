def decide_route(order_payload):
    channel = order_payload.get("channel", "").lower()

    if channel == "website":
        return "STANDARD_WEB_FLOW"

    if channel == "reseller":
        return "BULK_PARTNER_FLOW"

    if channel == "exhibition":
        return "QUICK_COUNTER_FLOW"

    return "UNKNOWN_FLOW"