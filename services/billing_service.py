from engine.storage_helper import read_data, write_data


def generate_invoice(order_payload, order_id):
    products = read_data("products.json")
    invoices = read_data("invoices.json")
    items = order_payload.get("items", [])

    total_amount = 0
    invoice_items = []

    for ordered_item in items:
        ordered_sku = ordered_item.get("sku")
        ordered_quantity = ordered_item.get("quantity")

        for product in products:
            if product.get("sku") == ordered_sku:
                price = product.get("price", 0)
                line_total = price * ordered_quantity

                invoice_items.append({
                    "sku": ordered_sku,
                    "quantity": ordered_quantity,
                    "unitPrice": price,
                    "lineTotal": line_total
                })

                total_amount += line_total
                break

    invoice_data = {
        "invoiceId": f"INV-{order_id}",
        "orderId": order_id,
        "itemCount": len(invoice_items),
        "totalAmount": total_amount,
        "paymentMode": order_payload.get("paymentMode"),
        "invoiceItems": invoice_items,
        "billingStatus": "INVOICE_GENERATED"
    }

    invoices.append(invoice_data)
    write_data("invoices.json", invoices)

    return True, invoice_data