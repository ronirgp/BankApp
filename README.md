# 🏦 BankApp - Banking System

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive Python-based banking application with user authentication, transaction management, and admin controls.

## ✨ Features

- 👤 **User Authentication** - Secure login with password hashing
- 💰 **Account Management** - Create, delete, and manage accounts
- 💸 **Transactions** - Deposit, withdraw, and transfer money
- 📊 **Transaction History** - View detailed transaction logs
- 🔐 **Admin Panel** - Manage users and view system statistics
- 📝 **Receipts** - Generate transaction receipts
- 🗝️ **Password Management** - Change passwords securely

## 📁 Project Structure

```
BankApp/
├── src/
│   ├── main.py                 # Main application
│   ├── database/
│   │   └── setup.py            # Database initialization
│   └── utils/
│       └── auth.py             # Authentication functions
├── data/
│   ├── db/
│   │   └── bank.db             # SQLite database
│   ├── transactions/           # User transaction logs
│   ├── users/                  # User data files
│   └── backups/                # Database backups
├── logs/
│   ├── receipts/               # Transaction receipts
│   └── audit/                  # Audit logs
├─�� config/
│   └── settings.py             # Configuration settings
├── tests/                      # Test files
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/ronirgp/BankApp.git
cd BankApp
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Initialize the database**
```bash
python -m src.database.setup
```

4. **Run the application**
```bash
python src/main.py
```

## 💻 Usage

### First Time Setup

1. Run the application
2. Login with admin credentials:
   - **Username:** admin
   - **Password:** admin123

### Available Operations

#### User Operations
- **Show Balance** - View current account balance
- **Deposit Money** - Add funds to account
- **Withdraw Money** - Remove funds (if sufficient balance)
- **Transfer Money** - Send funds to another user
- **View Transactions** - See transaction history
- **Change Password** - Update account password

#### Admin Operations (admin account only)
- **Admin Panel** - View all users and system statistics
- **Search User** - Find specific user information
- **Create Account** - Add new user account
- **Delete Account** - Remove user account
- **User Transaction Report** - Generate detailed reports

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    balance REAL DEFAULT 0,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    receiver TEXT
)
```

### Login History Table
```sql
CREATE TABLE login_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    login_time TEXT NOT NULL
)
```

## 🔒 Security Features

- ✅ Password hashing with SHA256
- ✅ Secure login authentication
- ✅ Admin-only operations
- ✅ Login history tracking
- ✅ Transaction logging
- ✅ Balance validation

## 📋 Sample Users

| Username | Password | Balance | Role |
|----------|----------|---------|------|
| admin | admin123 | 1000 | Administrator |
| Ronald | 1234 | 1600 | User |
| Maria | abcd | 3000 | User |
| Carlos | 9999 | 0 | User |

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black src/
```

### Linting
```bash
flake8 src/
```

## 📝 File Descriptions

- **src/main.py** - Main application logic and menu system
- **src/database/setup.py** - Database initialization and schema
- **src/utils/auth.py** - Authentication and password hashing functions
- **config/settings.py** - Configuration constants and paths
- **data/db/bank.db** - SQLite database file
- **data/transactions/** - Individual user transaction logs
- **logs/receipts/** - Transaction receipts

## 🐛 Troubleshooting

### "Database file not found"
- Run `python -m src.database.setup` to initialize

### "User not found"
- Check username spelling
- Create new account if needed

### "Insufficient funds"
- Deposit more money or request transfer
- Check balance with option 1

## 🚀 Future Enhancements

- [ ] GUI with Tkinter/PyQt
- [ ] Multiple currency support
- [ ] Interest calculations
- [ ] Loan management
- [ ] API REST interface
- [ ] Email notifications
- [ ] Mobile app

## 📚 Technologies Used

- **Language:** Python 3.8+
- **Database:** SQLite3
- **Security:** SHA256 hashing
- **Architecture:** Object-oriented with modular design

## 👨‍💼 Author

**Ronald Gustavo Pineda**  
📧 [ronald.pneda8@gmail.com](mailto:ronald.pneda8@gmail.com)  
🇸🇻 From El Salvador  
💼 Open to: Freelance work, collaborations, job opportunities

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Last Updated:** June 2026  
**Status:** ✅ Production Ready
