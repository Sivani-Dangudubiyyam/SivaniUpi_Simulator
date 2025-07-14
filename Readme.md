# 💸 Sivani's UPI Simulator

A **command-line Python application** that simulates UPI-based digital payments using QR codes. Users can register, login, view wallet balance, generate QR codes for transactions, and maintain transaction history — all stored securely using SQLite.

---

## 🚀 Features

* 🔐 **User Registration & Login** with password input via `getpass`
* 🏦 **Simulated Wallet** with preloaded balances
* 📷 **QR Code Generation** for UPI payments
* 📊 **Transaction History** with timestamps and unique IDs
* 🗃️ **SQLite Database Integration** (users & transactions stored)
* 🖼️ **Automatic QR Preview** using the system image viewer

---

## 🛠️ Tech Stack

* **Python 3.x**
* `sqlite3` – for data persistence
* `qrcode` – to generate UPI QR codes
* `Pillow (PIL)` – to render and preview QR codes
* `uuid` – to generate unique transaction IDs
* `getpass` – for secure password entry

---

## 📦 Installation

1. **Clone the repo** or download the script.

2. **Install dependencies:**

```bash
pip install qrcode[pil]
```

> `getpass`, `uuid`, and `sqlite3` are built into Python’s standard library – no installation needed.

---

## ▶️ Running the Application

```bash
python upi_simulator.py
```

On launch:

* Choose to **register** or **login**
* Make UPI payments to existing users
* Scan the generated QR code (simulated)
* Confirm and log your payment
* View full transaction history

---

## 👤 Default Pre-Users

| Username | Password | UPI ID            | Balance (₹) |
| -------- | -------- | ----------------- | ----------- |
| sivani   | pass123  | sivani\@bob       | 49,000.00   |
| roopa    | rop456   | roopa\@paytm      | 25,000.00   |
| parvathi | par789   | parvathi\@okaxis  | 63,000.00   |
| babji    | babji999 | babji\@okhdfcbank | 190,000.00  |

---

## 📝 Database Schema

### `users` table

| Column   | Type | Description     |
| -------- | ---- | --------------- |
| username | TEXT | Primary key     |
| password | TEXT | User's password |
| upi\_id  | TEXT | Unique UPI ID   |
| balance  | REAL | Wallet balance  |

### `transactions` table

| Column    | Type | Description                    |
| --------- | ---- | ------------------------------ |
| id        | TEXT | Unique transaction ID (UUID)   |
| username  | TEXT | Payer's username               |
| to\_upi   | TEXT | Payee's UPI ID                 |
| amount    | REAL | Transaction amount             |
| status    | TEXT | Transaction status ("Success") |
| timestamp | TEXT | Date and time of transaction   |

---

## 📷 Sample UPI QR Output

Each payment generates a file like:

```
upi_qr_roopaokpaytm1720967842.png
```

It can be scanned by a real UPI app (for visual testing only; it won’t process real money).

---

## 🔐 Security Notes

* Passwords are securely entered using `getpass`
* No encryption used for storage — not suitable for production
* This project is intended for **educational/demo purposes only**

---


## 📄 License

This project is open for learning and personal experimentation. No official license applied.
