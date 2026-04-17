# FlowBridge Integration Simulator

## Overview

FlowBridge Integration Simulator is a Python Flask-based system designed to simulate SAP-style enterprise integration workflows.

The system processes customer orders from multiple channels such as website, reseller, and exhibition. It performs routing, validation, inventory reservation, invoice generation, shipment creation, logging, and failure handling using a deadletter queue.

A dashboard interface provides real-time monitoring of system health, inventory, orders, invoices, shipments, logs, and failed transactions.

---

## Key Features

- Multi-channel order routing
- Order validation system
- Inventory reservation
- Invoice generation
- Shipment creation
- Logging system
- Deadletter queue handling
- Dashboard monitoring

---

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- REST APIs
- JSON

---

## How to Run

Install dependencies:

pip install -r requirements.txt

Run server:

python app.py

Open dashboard:

http://127.0.0.1:5000/dashboard

---

## Author

Tishya Misra