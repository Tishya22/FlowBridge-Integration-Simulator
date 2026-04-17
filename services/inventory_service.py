from engine.storage_helper import read_data, write_data


def reserve_stock(items):
    products = read_data("products.json")

    for ordered_item in items:
        ordered_sku = ordered_item.get("sku")
        ordered_quantity = ordered_item.get("quantity")

        matching_product = None
        for product in products:
            if product.get("sku") == ordered_sku:
                matching_product = product
                break

        if matching_product is None:
            return False, f"SKU {ordered_sku} not found"

        available_stock = matching_product.get("stock", 0)
        if available_stock < ordered_quantity:
            return False, f"Insufficient stock for SKU {ordered_sku}"

    for ordered_item in items:
        ordered_sku = ordered_item.get("sku")
        ordered_quantity = ordered_item.get("quantity")

        for product in products:
            if product.get("sku") == ordered_sku:
                product["stock"] = product.get("stock", 0) - ordered_quantity
                break

    write_data("products.json", products)

    return True, "Stock reserved successfully"