from engine.storage_helper import read_data, write_data
import uuid
from datetime import datetime


def create_order(order_payload, route_type):
    orders = read_data("orders.json")

    order_id = "ORD-" + str(uuid.uuid4())[:8]

    new_order = {
        "orderId": order_id,
        "channel": order_payload.get("channel"),
        "routeType": route_type,
        "customer": order_payload.get("customer"),
        "items": order_payload.get("items"),
        "paymentMode": order_payload.get("paymentMode"),
        "deliveryType": order_payload.get("deliveryType"),
        "status": "CREATED",
        "createdAt": datetime.now().isoformat()
    }

    orders.append(new_order)
    write_data("orders.json", orders)

    return True, new_order