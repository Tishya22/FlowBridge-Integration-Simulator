from flask import Flask, request, render_template
from engine.storage_helper import read_data, write_data
from engine.router import decide_route
from services.order_service import create_order
from services.integration_service import process_order

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return {
        "project": "FlowBridge Integration Simulator",
        "status": "running",
        "availableEndpoints": [
            "/health",
            "/summary",
            "/inventory",
            "/orders",
            "/invoices",
            "/shipments",
            "/logs",
            "/deadletters",
            "/dashboard",
            "/create-order",
            "/process-order",
            "/retry-deadletter/<index>"
        ]
    }


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health_check():
    return {
        "success": True,
        "service": "FlowBridge Integration Simulator",
        "status": "UP"
    }


@app.route("/summary", methods=["GET"])
def get_summary():
    orders = read_data("orders.json")
    invoices = read_data("invoices.json")
    shipments = read_data("shipments.json")
    logs = read_data("logs.json")
    deadletters = read_data("deadletter.json")

    return {
        "success": True,
        "summary": {
            "totalOrders": len(orders),
            "totalInvoices": len(invoices),
            "totalShipments": len(shipments),
            "totalLogs": len(logs),
            "totalDeadletters": len(deadletters)
        }
    }


@app.route("/inventory", methods=["GET"])
def get_inventory():
    products = read_data("products.json")
    return {
        "success": True,
        "products": products
    }


@app.route("/orders", methods=["GET"])
def get_orders():
    orders = read_data("orders.json")
    return {
        "success": True,
        "orders": orders
    }


@app.route("/invoices", methods=["GET"])
def get_invoices():
    invoices = read_data("invoices.json")
    return {
        "success": True,
        "invoices": invoices
    }


@app.route("/shipments", methods=["GET"])
def get_shipments():
    shipments = read_data("shipments.json")
    return {
        "success": True,
        "shipments": shipments
    }


@app.route("/logs", methods=["GET"])
def get_logs():
    logs = read_data("logs.json")
    return {
        "success": True,
        "logs": logs
    }


@app.route("/deadletters", methods=["GET"])
def get_deadletters():
    deadletters = read_data("deadletter.json")
    return {
        "success": True,
        "deadletters": deadletters
    }


@app.route("/create-order", methods=["POST"])
def create_order_route():
    order_payload = request.get_json()
    route_type = decide_route(order_payload)

    is_created, order_data = create_order(order_payload, route_type)

    return {
        "success": is_created,
        "order": order_data
    }


@app.route("/process-order", methods=["POST"])
def process_order_route():
    order_payload = request.get_json()

    success, result = process_order(order_payload)

    return {
        "success": success,
        "result": result
    }


@app.route("/retry-deadletter/<int:index>", methods=["POST"])
def retry_deadletter(index):
    deadletters = read_data("deadletter.json")

    if index < 0 or index >= len(deadletters):
        return {
            "success": False,
            "message": "Invalid deadletter index"
        }, 400

    failed_entry = deadletters[index]
    payload = failed_entry.get("payload", {})

    success, result = process_order(payload)

    if success:
        deadletters.pop(index)
        write_data("deadletter.json", deadletters)

        return {
            "success": True,
            "message": "Deadletter reprocessed successfully",
            "result": result
        }

    return {
        "success": False,
        "message": "Retry failed again",
        "result": result
    }


if __name__ == "__main__":
    app.run(debug=True)