async function fetchJson(endpoint) {
    const response = await fetch(endpoint);
    if (!response.ok) {
        throw new Error("Failed to fetch data");
    }
    return await response.json();
}

function showError(outputId, message) {
    document.getElementById(outputId).innerHTML =
        `<p style="color:red;">${message}</p>`;
}

function renderHealthCard(data) {
    return `
        <p><strong>Service:</strong> ${data.service}</p>
        <p><strong>Status:</strong>
            <span class="${data.status === "UP" ? "status-good" : "status-bad"}">
                ${data.status}
            </span>
        </p>
        <p><strong>Success:</strong> ${data.success}</p>
    `;
}

async function loadHealth() {
    const output = document.getElementById("healthOutput");
    output.innerHTML = "Loading...";

    try {
        const data = await fetchJson("/health");
        output.innerHTML = renderHealthCard(data);
    } catch {
        showError("healthOutput", "Error loading health.");
    }
}

function renderSummaryCard(data) {
    const s = data.summary;
    return `
        <p><strong>Total Orders:</strong> ${s.totalOrders}</p>
        <p><strong>Total Invoices:</strong> ${s.totalInvoices}</p>
        <p><strong>Total Shipments:</strong> ${s.totalShipments}</p>
        <p><strong>Total Logs:</strong> ${s.totalLogs}</p>
        <p><strong>Total Deadletters:</strong> ${s.totalDeadletters}</p>
    `;
}

async function loadSummary() {
    const output = document.getElementById("summaryOutput");
    output.innerHTML = "Loading...";

    try {
        const data = await fetchJson("/summary");
        output.innerHTML = renderSummaryCard(data);
    } catch {
        showError("summaryOutput", "Error loading summary.");
    }
}

async function loadInventory() {
    const output = document.getElementById("inventoryOutput");
    output.innerHTML = "Loading...";

    try {
        const data = await fetchJson("/inventory");

        let html = `
        <table>
            <thead>
                <tr>
                    <th>SKU</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Stock</th>
                </tr>
            </thead>
            <tbody>
        `;

        data.products.forEach(p => {
            html += `
                <tr>
                    <td>${p.sku}</td>
                    <td>${p.name}</td>
                    <td>${p.price}</td>
                    <td>${p.stock}</td>
                </tr>
            `;
        });

        html += `
            </tbody>
        </table>
        `;

        output.innerHTML = html;
    } catch {
        showError("inventoryOutput", "Error loading inventory.");
    }
}

async function loadOrders() {
    const output = document.getElementById("ordersOutput");
    output.innerHTML = "Loading...";

    try {
        const data = await fetchJson("/orders");

        let html = `
        <table>
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>Customer</th>
                    <th>City</th>
                    <th>Channel</th>
                    <th>Route</th>
                </tr>
            </thead>
            <tbody>
        `;

        data.orders.forEach(o => {
            html += `
                <tr>
                    <td>${o.orderId || "-"}</td>
                    <td>${o.customer?.name || "-"}</td>
                    <td>${o.customer?.city || "-"}</td>
                    <td>${o.channel || "-"}</td>
                    <td>${o.routeType || "-"}</td>
                </tr>
            `;
        });

        html += `
            </tbody>
        </table>
        `;

        output.innerHTML = html;
    } catch {
        showError("ordersOutput", "Error loading orders.");
    }
}

async function loadInvoices() {
    const output = document.getElementById("invoicesOutput");
    output.innerHTML = "Loading...";

    try {
        const data = await fetchJson("/invoices");

        let html = `
        <table>
            <thead>
                <tr>
                    <th>Invoice ID</th>
                    <th>Order ID</th>
                    <th>Payment</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
        `;

        data.invoices.forEach(inv => {
            html += `
                <tr>
                    <td>${inv.invoiceId}</td>
                    <td>${inv.orderId}</td>
                    <td>${inv.paymentMode}</td>
                    <td>${inv.totalAmount}</td>
                </tr>
            `;
        });

        html += `
            </tbody>
        </table>
        `;

        output.innerHTML = html;
    } catch {
        showError("invoicesOutput", "Error loading invoices.");
    }
}

async function loadShipments() {
    const output = document.getElementById("shipmentsOutput");
    output.innerHTML = "Loading...";

    try {
        const data = await fetchJson("/shipments");

        let html = `
        <table>
            <thead>
                <tr>
                    <th>Shipment ID</th>
                    <th>Order ID</th>
                    <th>Tracking</th>
                    <th>Carrier</th>
                </tr>
            </thead>
            <tbody>
        `;

        data.shipments.forEach(s => {
            html += `
                <tr>
                    <td>${s.shipmentId}</td>
                    <td>${s.orderId}</td>
                    <td>${s.trackingId}</td>
                    <td>${s.carrier}</td>
                </tr>
            `;
        });

        html += `
            </tbody>
        </table>
        `;

        output.innerHTML = html;
    } catch {
        showError("shipmentsOutput", "Error loading shipments.");
    }
}

async function loadLogs() {
    const output = document.getElementById("logsOutput");
    output.innerHTML = "Loading...";

    try {
        const data = await fetchJson("/logs");

        let html = `
        <table>
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Stage</th>
                    <th>Status</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
        `;

        data.logs.forEach(log => {
            html += `
                <tr>
                    <td>${log.time}</td>
                    <td>${log.stage}</td>
                    <td>
                        <span class="${log.status === "SUCCESS" || log.status === "INFO" ? "status-good" : "status-bad"}">
                            ${log.status}
                        </span>
                    </td>
                    <td>${log.message}</td>
                </tr>
            `;
        });

        html += `
            </tbody>
        </table>
        `;

        output.innerHTML = html;
    } catch {
        showError("logsOutput", "Error loading logs.");
    }
}

async function loadDeadletters() {
    const output = document.getElementById("deadlettersOutput");
    output.innerHTML = "Loading...";

    try {
        const data = await fetchJson("/deadletters");

        let html = `
        <table>
            <thead>
                <tr>
                    <th>Index</th>
                    <th>Error</th>
                    <th>Customer</th>
                </tr>
            </thead>
            <tbody>
        `;

        data.deadletters.forEach((d, i) => {
            html += `
                <tr>
                    <td>${i}</td>
                    <td>${d.error}</td>
                    <td>${d.payload?.customer?.name || "-"}</td>
                </tr>
            `;
        });

        html += `
            </tbody>
        </table>
        `;

        output.innerHTML = html;
    } catch {
        showError("deadlettersOutput", "Error loading deadletters.");
    }
}