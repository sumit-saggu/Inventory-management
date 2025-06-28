# Inventory Management System

A simple command-line Inventory Management System built with Python and MySQL. This project allows you to manage products, stock, purchases, and sales for a fashion store.

---

## Features

- **Add Product**: Add new products to the inventory.
- **Edit Product**: Update product details.
- **Delete Product**: Remove products and all related records.
- **View Product**: View all products or filter by name, brand, gender, season, or ID.
- **Purchase Product**: Record purchases and update stock.
- **View Purchases**: View purchase history for a product.
- **View Stock Details**: Check current stock and status.
- **Sale Product**: Record sales, apply discounts, and update stock.
- **View Sales Details**: View sales history for a product.

---

## Requirements

- Python 3.x
- MySQL Server
- Python packages:
  - `mysql-connector-python`
  - `tabulate`

---

## Setup

1. **Clone the repository or copy the project files.**

2. **Install required Python packages:**
   ```bash
   pip install mysql-connector-python
   pip install tabulate
   ```

3. **Set up the MySQL database:**
   - Create a database named `fashion`.
   - Create the following tables:

   ```sql
   CREATE TABLE product (
       product_id VARCHAR(20) PRIMARY KEY,
       PName VARCHAR(100),
       brand VARCHAR(100),
       gender VARCHAR(20),
       Season VARCHAR(20),
       rate INT
   );

   CREATE TABLE stock (
       item_id VARCHAR(20) PRIMARY KEY,
       Instock INT,
       status VARCHAR(10)
   );

   CREATE TABLE purchase (
       purchase_id VARCHAR(30) PRIMARY KEY,
       item_id VARCHAR(20),
       no_of_items INT,
       amount FLOAT,
       Purchase_date DATE
   );

   CREATE TABLE sales (
       sale_id VARCHAR(30) PRIMARY KEY,
       item_id VARCHAR(20),
       no_of_item_sold INT,
       sale_rate FLOAT,
       amount FLOAT,
       date_of_sale DATE
   );
   ```

4. **Update database credentials in your Python file if needed:**
   ```python
   mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       passwd="pass",
       charset="utf8",
       database="fashion"
   )
   ```

---

## Usage

1. **Run the program:**
   ```bash
   python inventary\ store.py
   ```
   or
   ```bash
   python new.py
   ```

2. **Follow the on-screen menu to manage your inventory.**
   - Enter the number corresponding to the action you want to perform.
   - After each action, you will be prompted if you want to perform another action.

---

## Notes

- Ensure your MySQL server is running before starting the program.
- All data is stored in the MySQL database.
- The program uses parameterized queries to prevent SQL injection.
- The command-line interface is simple and user-friendly.

---

## Screenshots

![Screenshot 2025-06-28 145523](https://github.com/user-attachments/assets/e57dfd1e-a88b-4dbb-8ea7-7f5afa210414)
![Screenshot 2025-06-28 145558](https://github.com/user-attachments/assets/b1e79172-e862-41ff-8726-7ad0d2f0dc63)
![Screenshot 2025-06-28 145633](https://github.com/user-attachments/assets/9b46de7a-fcfd-4cbd-929e-22ea91682a16)


---

## License

This project is for educational purposes.

---

## Author

- Sumit Kumar

---

## Acknowledgements

- [Tabulate](https://pypi.org/project/tabulate/) for pretty-printing tables in the terminal.
- [MySQL Connector/Python](https://pypi.org/project/mysql-connector-python/) for database connectivity.
