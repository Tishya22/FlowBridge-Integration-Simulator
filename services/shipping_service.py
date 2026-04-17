import uuid
from datetime import datetime
from engine.storage_helper import read_data, write_data


def generate_shipment(order_data):
    shipments = read_data("shipments.json")

    tracking_id = "TRK-" + str(uuid.uuid4())[:8]

    shipment_data = {
        "shipmentId": f"SHP-{order_data['orderId']}",
        "orderId": order_data["orderId"],
        "trackingId": tracking_id,
        "carrier": "BlueDart",
        "dispatchTime": datetime.now().isoformat(),
        "shippingStatus": "DISPATCHED"
    }

    shipments.append(shipment_data)
    write_data("shipments.json", shipments)

    return True, shipment_data