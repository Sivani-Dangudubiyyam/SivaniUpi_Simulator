import qrcode
from PIL import Image
import sqlite3
import uuid
import time
from datetime import datetime
import getpass

#GLOBALS
current_user = ""
user_upi_id = ""
wallet_balance = 0.0

#DATABASE SETUP
conn = sqlite3.connect("upi_simulator.db")
cursor = conn.cursor()

# Users table with UPI and password
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    upi_id TEXT UNIQUE NOT NULL,
    balance REAL
)
""")

# Transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    username TEXT,
    to_upi TEXT,
    amount REAL,
    status TEXT,
    timestamp TEXT,
    FOREIGN KEY (username) REFERENCES users(username)
)
""")
conn.commit()

#FAKE PRE_USERS
def pre_users():
    users = [
        ("sivani", "pass123", "sivani@bob", 49000.00),
        ("roopa", "rop456", "roopa@paytm", 25000.00),
        ("parvathi", "par789", "parvathi@okaxis", 63000.00),
        ("babji", "babji999", "babji@okhdfcbank", 190000.00)
    ]
    for username, password, upi, balance in users:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, upi_id, balance) VALUES (?, ?, ?, ?)",
                           (username, password, upi, balance))
    conn.commit()

pre_users()  

#QR CODE GENERATOR
def generate_real_qr(upi_id, amount, name="Test User"):
    upi_url = (
        f"upi://pay?pa={upi_id}&pn={name.replace(' ', '%20')}"
        f"&am={amount}&cu=INR"
    )

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(upi_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    file_name = f"upi_qr_{upi_id.replace('@','')}{int(time.time())}.png"
    img.save(file_name)

    print(f"\n📷 QR Code saved as: {file_name}")
    try:
        img.show()
        print("📲 QR Code opened in your default image viewer.")
    except:
        print("⚠ Unable to auto-open QR. Please open manually.")

#AUTHENTICATION
def user_login():
    global wallet_balance, current_user, user_upi_id
    print("\n🔐 Login or Register")
    choice = input("Do you have an account? (y/n): ").lower()

    username = input("👤 Username: ").strip().lower()
    password = getpass.getpass("🔒 Password: ")

    if choice == 'n':
        upi_id = input("🔗 Create your UPI ID (e.g., name@bank): ").strip().lower()
        cursor.execute("SELECT * FROM users WHERE username = ? OR upi_id = ?", (username, upi_id))
        if cursor.fetchone():
            print("⚠ Username or UPI ID already exists. Try again.")
            return user_login()
        wallet_balance = 5000.00
        cursor.execute("INSERT INTO users (username, password, upi_id, balance) VALUES (?, ?, ?, ?)", (username, password, upi_id, wallet_balance))
        conn.commit()
        print(f"🆕 New user '{username}' registered. Balance: ₹{wallet_balance}")
        user_upi_id = upi_id
    else:
        cursor.execute("SELECT password, balance, upi_id FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if not result or result[0] != password:
            print("❌ Invalid credentials.")
            return user_login()
        wallet_balance = result[1]
        user_upi_id = result[2]
        print(f"✅ Welcome back, {username}. Balance: ₹{wallet_balance:.2f}")

    current_user = username

#PAYMENT FLOW
def make_upi_payment():
    global wallet_balance
    cursor.execute("SELECT upi_id FROM users")
    upi_users = [row[0] for row in cursor.fetchall() if row[0] != user_upi_id]

    print("\n🔠 Available Payees:", ", ".join(upi_users))
    to_upi = input("👤 Enter UPI ID to pay: ").lower()

    if to_upi not in upi_users or '@' not in to_upi:
        print("❌ Invalid or unknown UPI ID.")
        return

    try:
        amount = float(input("💰 Enter amount: ₹"))
    except:
        print("⚠ Invalid amount.")
        return

    if amount > wallet_balance:
        print("❌ Insufficient balance.")
        return

    generate_real_qr(to_upi, amount, name=current_user)
    confirm = input("\n✅ Confirm payment after scanning? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Payment cancelled.")
        return

    txn_id = str(uuid.uuid4())[:10]
    wallet_balance -= amount

    cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (wallet_balance, current_user))
    cursor.execute("""
        INSERT INTO transactions (id, username, to_upi, amount, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        txn_id, current_user, to_upi, amount, "Success",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()

    print(f"\n🟢 Payment of ₹{amount} to {to_upi} successful!")
    print(f"🔖 Transaction ID: {txn_id}")

#HISTORY
def show_transactions():
    print(f"\n📜 Transactions for {current_user}:")
    cursor.execute("SELECT * FROM transactions WHERE username = ? ORDER BY timestamp DESC", (current_user,))
    rows = cursor.fetchall()
    if not rows:
        print("🕒 No transactions yet.")
    for txn in rows:
        print(f"🕒 {txn[5]} | 💸 ₹{txn[3]} ➡ {txn[2]} | ID: {txn[0]}")

# === MAIN APP ===
def main():
    user_login()
    while True:
        print("\nSivani's UPI Simulator")
        print(f"👤 User: {current_user} | 🆔 UPI: {user_upi_id} | 💼 Wallet: ₹{wallet_balance:.2f}")
        print("1️. Make UPI Payment")
        print("2️. View Transactions")
        print("3️. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            make_upi_payment()
        elif choice == '2':
            show_transactions()
        elif choice == '3':
            print("👋 Thank you for using Sivani's UPI. Goodbye!")
            break
        else:
            print("⚠ Invalid input.")
main()
conn.close()