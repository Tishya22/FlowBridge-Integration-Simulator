from datetime import datetime
from engine.validator import validate_order
from engine.router import decide_route
from engine.log_helper import add_log
from engine.storage_helper import read_data, write_data
from services.inventory_service import reserve_stock
from services.order_service import create_order
from services.billing_service import generate_invoice
from services.shipping_service import generate_shipment


def process_order(order_payload):
    add_log(
        stage="ORDER_RECEIVED",
        status="INFO",
        message="New order received for processing",
        payload=order_payload
    )

    route_type = decide_route(order_payload)

    add_log(
        stage="ROUTING",
        status="SUCCESS",
        message=f"Order routed through {route_type}",
        payload=order_payload
    )

    is_valid, validation_message = validate_order(order_payload)

    if not is_valid:
        add_log(
            stage="VALIDATION",
            status="FAILED",
            message=validation_message,
            payload=order_payload
        )

        deadletter_entry = {
            "time": datetime.now().isoformat(),
            "error": validation_message,
            "payload": order_payload
        }

        deadletters = read_data("deadletter.json")
        deadletters.append(deadletter_entry)
        write_data("deadletter.json", deadletters)

        return False, validation_message

    add_log(
        stage="VALIDATION",
        status="SUCCESS",
        message="Order validation successful",
        payload=order_payload
    )

    items = order_payload.get("items", [])

    stock_ok, stock_message = reserve_stock(items)

    if not stock_ok:
        add_log(
            stage="INVENTORY",
            status="FAILED",
            message=stock_message,
            payload=order_payload
        )
        return False, stock_message

    add_log(
        stage="INVENTORY",
        status="SUCCESS",
        message="Stock reserved successfully",
        payload=order_payload
    )

    order_created, order_data = create_order(order_payload, route_type)

    if not order_created:
        add_log(
            stage="ORDER_CREATION",
            status="FAILED",
            message="Order creation failed",
            payload=order_payload
        )
        return False, "Order creation failed"

    add_log(
        stage="ORDER_CREATION",
        status="SUCCESS",
        message="Order created successfully",
        payload=order_data
    )

    billing_ok, billing_data = generate_invoice(order_payload, order_data["orderId"])

    if not billing_ok:
        add_log(
            stage="BILLING",
            status="FAILED",
            message="Billing failed",
            payload=order_data
        )
        return False, "Billing failed"

    add_log(
        stage="BILLING",
        status="SUCCESS",
        message="Invoice generated successfully",
        payload=billing_data
    )

    shipping_ok, shipping_data = generate_shipment(order_data)

    if not shipping_ok:
        add_log(
            stage="SHIPPING",
            status="FAILED",
            message="Shipping failed",
            payload=order_data
        )
        return False, "Shipping failed"

    add_log(
        stage="SHIPPING",
        status="SUCCESS",
        message="Shipment created successfully",
        payload=shipping_data
    )

    final_result = {
        "order": order_data,
        "invoice": billing_data,
        "shipment": shipping_data
    }

    return True, final_result