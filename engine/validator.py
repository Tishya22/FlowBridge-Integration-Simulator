def validate_order(order_payload):
    allowed_channels = ["website", "reseller", "exhibition"]
    allowed_payment_modes = ["prepaid", "cod"]
    allowed_delivery_types = ["standard", "express"]

    if not isinstance(order_payload, dict):
        return False, "Order payload must be a JSON object"

    channel = order_payload.get("channel")
    if channel not in allowed_channels:
        return False, "Invalid or missing channel"

    customer = order_payload.get("customer")
    if not isinstance(customer, dict):
        return False, "Customer details are missing"

    customer_name = customer.get("name")
    if not customer_name or not customer_name.strip():
        return False, "Customer name is required"

    customer_city = customer.get("city")
    if not customer_city or not customer_city.strip():
        return False, "Customer city is required"

    items = order_payload.get("items")
    if not isinstance(items, list) or len(items) == 0:
        return False, "Order must contain at least one item"

    for item in items:
        if not isinstance(item, dict):
            return False, "Each item must be an object"

        sku = item.get("sku")
        quantity = item.get("quantity")

        if not sku or not str(sku).strip():
            return False, "Each item must have a valid SKU"

        if not isinstance(quantity, int) or quantity <= 0:
            return False, "Each item quantity must be a positive integer"

    payment_mode = order_payload.get("paymentMode")
    if payment_mode not in allowed_payment_modes:
        return False, "Invalid or missing payment mode"

    delivery_type = order_payload.get("deliveryType")
    if delivery_type not in allowed_delivery_types:
        return False, "Invalid or missing delivery type"

    return True, "Validation successful"