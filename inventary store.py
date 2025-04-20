import platform
import mysql.connector
import datetime
from tabulate import tabulate

# Initialize database connection
now = datetime.datetime.now()
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="pass",
    charset="utf8",
    database="fashion"
)
mycursor = mydb.cursor()

print("=" * 97)
print(" * * * * * * * * * * Welcome to the Project of Inventory Management System * * * * * * * * * * * ")
print("=" * 97)

def AddProduct():
    """
    Function to add a new product to the inventory.
    """
    print("")
    print("=" * 70)
    L = []
    stk = []

    # Fetch the last product ID
    a = "SELECT product_id FROM product;"
    mycursor.execute(a)
    data = mycursor.fetchall()
    print("Your last product ID is:", data[-1][0])
    print("Enter the next number in product ID")

    # Input product details
    pid = input("Enter product ID: ")
    L.append(pid)
    IName = input("Enter the Product Name: ")
    L.append(IName)
    brnd = input("Enter the Product Brand Name: ")
    L.append(brnd)
    fr = input("Male/Female/Kids: ")
    L.append(fr)
    sn = input("Winter/Summer: ")
    L.append(sn)
    rate = int(input("Enter the price for Product: "))
    L.append(rate)

    # Insert product into the database
    product = tuple(L)
    sql = """INSERT INTO product (product_id, PName, brand, gender, Season, rate)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    mycursor.execute(sql, product)
    mydb.commit()

    # Insert stock details
    stk.append(pid)
    stk.append(0)
    stk.append("No")
    st = tuple(stk)
    sql = "INSERT INTO stock (item_id, Instock, status) VALUES (%s, %s, %s)"
    mycursor.execute(sql, st)
    mydb.commit()

    print("One Product inserted")
    print("")
    print("=" * 97)

def EditProduct():
    """
    Function to edit an existing product.
    """
    pid = input("Enter product ID to be edited: ")
    sql = "SELECT * FROM product WHERE product_id = %s"
    ed = (pid,)
    h = ["product_id", "PName", "brand", "gender", "Season", "rate"]
    mycursor.execute(sql, ed)
    res = mycursor.fetchall()
    print(tabulate(res, headers=h, tablefmt="psql"))
    print("")

    fld = input("Enter the field which you want to edit: ")
    val = input("Enter the value you want to set: ")

    sql = f"UPDATE product SET {fld} = %s WHERE product_id = %s"
    mycursor.execute(sql, (val, pid))
    mydb.commit()

    print("Editing Done:")
    print("After correction, the record is:")
    mycursor.execute("SELECT * FROM product WHERE product_id = %s", ed)
    res = mycursor.fetchall()
    print(tabulate(res, headers=h, tablefmt="psql"))

def DelProduct():
    """
    Function to delete a product from the inventory.
    """
    pid = input("Enter the Product ID to be deleted: ")
    sqls = [
        "DELETE FROM sales WHERE item_id = %s",
        "DELETE FROM purchase WHERE item_id = %s",
        "DELETE FROM stock WHERE item_id = %s",
        "DELETE FROM product WHERE product_id = %s"
    ]
    for sql in sqls:
        mycursor.execute(sql, (pid,))
        mydb.commit()
    print("One Item Deleted")

def ViewProduct():
    """
    Function to view product details.
    """
    print("Display Menu: Select the category to display the data")
    print("1. All Details")
    print("2. To show all details with the same Product Name")
    print("3. To show all details with the same Product Brand")
    print("4. To show all details with the same Product For")
    print("5. To show all details with the same Product Season")
    print("6. To show all details with the same Product ID")

    ch = int(input("Enter your choice to display: "))
    if ch == 1:
        sql = "SELECT * FROM product"
        mycursor.execute(sql)
        res = mycursor.fetchall()
        h = ["product_id", "PName", "brand", "gender", "Season", "rate"]
        print(tabulate(res, headers=h, tablefmt="psql"))
    else:
        var = ""
        if ch == 2:
            var = "PName"
        elif ch == 3:
            var = "brand"
        elif ch == 4:
            var = "gender"
        elif ch == 5:
            var = "Season"
        elif ch == 6:
            var = "product_id"
        val = input(f"Enter the value for {var}: ")
        sql = f"SELECT * FROM product WHERE {var} = %s"
        mycursor.execute(sql, (val,))
        res = mycursor.fetchall()
        h = ["product_id", "PName", "brand", "gender", "Season", "rate"]
        print(tabulate(res, headers=h, tablefmt="psql"))

def PurchaseProduct():
    """
    Function to handle product purchase.
    """
    purchaseID = "P" + now.strftime("%Y%m%d%H%M%S")
    L = []
    L.append(purchaseID)

    # Input product details
    itemId = input("Enter Product ID: ")
    L.append(itemId)
    itemNo = int(input("Enter the number of Items: "))
    L.append(itemNo)

    # Fetch product rate
    sql = "SELECT rate FROM product WHERE product_id = %s"
    pid = (itemId,)
    mycursor.execute(sql, pid)
    res = mycursor.fetchone()

    if not res:
        print("Product ID not found!")
        return

    rate = res[0]
    print("Rate is:", rate)

    # Calculate amount
    amount = rate * itemNo
    print("Amount is:", amount)
    L.append(amount)

    # Add purchase date
    dt = now.strftime("%Y-%m-%d")
    L.append(dt)

    # Insert purchase record
    tp = tuple(L)
    sql = """INSERT INTO purchase (purchase_id, item_id, no_of_items, amount, Purchase_date)
             VALUES (%s, %s, %s, %s, %s)"""
    mycursor.execute(sql, tp)
    mydb.commit()

    # Update stock
    sql = "SELECT Instock FROM stock WHERE item_id = %s"
    mycursor.execute(sql, pid)
    res = mycursor.fetchone()

    if not res:
        print("Stock record not found!")
        return

    instock = res[0] + itemNo
    status = "Yes" if instock > 0 else "No"

    sql = """UPDATE stock SET Instock = %s, status = %s WHERE item_id = %s"""
    mycursor.execute(sql, (instock, status, itemId))
    mydb.commit()

    print(f"{itemNo} item(s) purchased and saved in the database.")

def ViewPurchase():
    """
    Function to view purchase details.
    """
    item = input("Enter Product Name: ")
    sql = """SELECT product.product_id, product.PName, product.brand, purchase.no_of_items, 
             purchase.purchase_date, purchase.amount 
             FROM product 
             INNER JOIN purchase ON product.product_id = purchase.item_id 
             WHERE product.PName = %s"""
    itm = (item,)
    mycursor.execute(sql, itm)
    res = mycursor.fetchall()
    h = ["product_id", "PName", "brand", "no_of_items", "purchase_date", "amount"]
    print(tabulate(res, headers=h, tablefmt="psql"))

def ViewStock():
    """
    Function to view stock details.
    """
    item = input("Enter Product Name: ")
    sql = """SELECT product.product_id, product.PName, stock.Instock, stock.status 
             FROM stock 
             INNER JOIN product ON product.product_id = stock.item_id 
             WHERE product.PName = %s"""
    itm = (item,)
    mycursor.execute(sql, itm)
    res = mycursor.fetchall()
    h = ["product_id", "PName", "Instock", "status"]
    print(tabulate(res, headers=h, tablefmt="psql"))

def SaleProduct():
    """
    Function to handle product sales.
    """
    saleID = "S" + now.strftime("%Y%m%d%H%M%S")
    L = []
    L.append(saleID)

    itemId = input("Enter Product ID: ")
    L.append(itemId)
    itemNo = int(input("Enter the number of Items: "))
    L.append(itemNo)

    sql = "SELECT rate FROM product WHERE product_id = %s"
    pid = (itemId,)
    mycursor.execute(sql, pid)
    res = mycursor.fetchone()

    if not res:
        print("Product ID not found!")
        return

    rate = res[0]
    print("The rate of the item is:", rate)

    dis = int(input("Enter the discount: "))
    saleRate = rate - (rate * dis / 100)
    L.append(saleRate)

    amount = itemNo * saleRate
    L.append(amount)

    dt = now.strftime("%Y-%m-%d")
    L.append(dt)

    tp = tuple(L)
    sql = """INSERT INTO sales (sale_id, item_id, no_of_item_sold, sale_rate, amount, date_of_sale)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    mycursor.execute(sql, tp)
    mydb.commit()

    sql = "SELECT Instock FROM stock WHERE item_id = %s"
    mycursor.execute(sql, pid)
    res = mycursor.fetchone()

    if not res:
        print("Stock record not found!")
        return

    instock = res[0] - itemNo
    status = "Yes" if instock > 0 else "No"

    sql = """UPDATE stock SET Instock = %s, status = %s WHERE item_id = %s"""
    mycursor.execute(sql, (instock, status, itemId))
    mydb.commit()

    print(f"{itemNo} item(s) sold. Remaining stock: {instock}")

def ViewSales():
    """
    Function to view sales details.
    """
    item = input("Enter Product Name: ")
    sql = """SELECT product.product_id, product.PName, product.brand, sales.no_of_item_sold, 
             sales.date_of_sale, sales.amount 
             FROM sales 
             INNER JOIN product ON product.product_id = sales.item_id 
             WHERE product.PName = %s"""
    itm = (item,)
    mycursor.execute(sql, itm)
    res = mycursor.fetchall()
    h = ["product_id", "PName", "brand", "no_of_item_sold", "date_of_sale", "amount"]
    print(tabulate(res, headers=h, tablefmt="psql"))

def MenuSet():
    """
    Main menu for the inventory management system.
    """
    print("Enter 1 : To Add Product")
    print("Enter 2 : To Edit Product")
    print("Enter 3 : To Delete Product")
    print("Enter 4 : To View Product")
    print("Enter 5 : To Purchase Product")
    print("Enter 6 : To View Purchases")
    print("Enter 7 : To View Stock Details")
    print("Enter 8 : To Sale the item")
    print("Enter 9 : To View Sales Details")
    print("Enter 0 : To Exit")

    try:
        userInput = int(input("Please Select An Above Option: "))
        if userInput == 1:
            AddProduct()
        elif userInput == 2:
            EditProduct()
        elif userInput == 3:
            DelProduct()
        elif userInput == 4:
            ViewProduct()
        elif userInput == 5:
            PurchaseProduct()
        elif userInput == 6:
            ViewPurchase()
        elif userInput == 7:
            ViewStock()
        elif userInput == 8:
            SaleProduct()
        elif userInput == 9:
            ViewSales()
        elif userInput == 0:
            print("Exiting the program. Goodbye!")
            exit()
        else:
            print("Invalid choice! Please try again.")
    except ValueError:
        print("Invalid input! Please enter a number.")

    # Ask the user if they want to run the menu again
    runAgain = input("\nDo you want to perform another action? (Y/n): ").strip().lower()
    if runAgain != 'y':
        print("Exiting the program. Goodbye!")
        exit()

# Run the menu
while True:
    MenuSet()
