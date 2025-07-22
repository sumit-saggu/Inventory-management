from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="pass",
    database="fashion"
)
mycursor = mydb.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def view_products():
    mycursor.execute("SELECT * FROM product")
    products = mycursor.fetchall()
    return render_template('view_products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        pid = request.form['product_id']
        pname = request.form['PName']
        brand = request.form['brand']
        gender = request.form['gender']
        season = request.form['Season']
        rate = request.form['rate']
        sql = """INSERT INTO product (product_id, PName, brand, gender, Season, rate)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        mycursor.execute(sql, (pid, pname, brand, gender, season, rate))
        mydb.commit()
        # Add to stock table
        mycursor.execute("INSERT INTO stock (item_id, Instock, status) VALUES (%s, %s, %s)", (pid, 0, "No"))
        mydb.commit()
        flash('Product added successfully!')
        return redirect(url_for('view_products'))
    return render_template('add_product.html')

@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    mycursor.execute("SELECT * FROM product WHERE product_id=%s", (product_id,))
    product = mycursor.fetchone()
    if request.method == 'POST':
        field = request.form['field']
        value = request.form['value']
        sql = f"UPDATE product SET {field}=%s WHERE product_id=%s"
        mycursor.execute(sql, (value, product_id))
        mydb.commit()
        flash('Product updated successfully!')
        return redirect(url_for('view_products'))
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    for table, col in [('sales', 'item_id'), ('purchase', 'item_id'), ('stock', 'item_id'), ('product', 'product_id')]:
        mycursor.execute(f"DELETE FROM {table} WHERE {col}=%s", (product_id,))
        mydb.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('view_products'))

@app.route('/purchase_product', methods=['GET', 'POST'])
def purchase_product():
    if request.method == 'POST':
        item_id = request.form['item_id']
        item_no = int(request.form['item_no'])
        now = datetime.datetime.now()
        purchase_id = "P" + now.strftime("%Y%m%d%H%M%S")
        mycursor.execute("SELECT rate FROM product WHERE product_id=%s", (item_id,))
        res = mycursor.fetchone()
        if not res:
            flash('Product ID not found!')
            return redirect(url_for('purchase_product'))
        rate = res['rate']
        amount = rate * item_no
        date = now.strftime("%Y-%m-%d")
        sql = """INSERT INTO purchase (purchase_id, item_id, no_of_items, amount, Purchase_date)
                 VALUES (%s, %s, %s, %s, %s)"""
        mycursor.execute(sql, (purchase_id, item_id, item_no, amount, date))
        mydb.commit()
        # Update stock
        mycursor.execute("SELECT Instock FROM stock WHERE item_id=%s", (item_id,))
        res = mycursor.fetchone()
        if not res:
            flash('Stock record not found!')
            return redirect(url_for('purchase_product'))
        instock = res['Instock'] + item_no
        status = "Yes" if instock > 0 else "No"
        mycursor.execute("UPDATE stock SET Instock=%s, status=%s WHERE item_id=%s", (instock, status, item_id))
        mydb.commit()
        flash('Product purchased successfully!')
        return redirect(url_for('view_purchases'))
    return render_template('purchase_product.html')

@app.route('/view_purchases')
def view_purchases():
    mycursor.execute("""SELECT product.product_id, product.PName, product.brand, purchase.no_of_items, purchase.Purchase_date, purchase.amount
                        FROM product INNER JOIN purchase ON product.product_id=purchase.item_id""")
    purchases = mycursor.fetchall()
    return render_template('view_purchases.html', purchases=purchases)

@app.route('/view_stock')
def view_stock():
    mycursor.execute("""SELECT product.product_id, product.PName, stock.Instock, stock.status
                        FROM stock INNER JOIN product ON product.product_id=stock.item_id""")
    stocks = mycursor.fetchall()
    return render_template('view_stock.html', stocks=stocks)

@app.route('/sale_product', methods=['GET', 'POST'])
def sale_product():
    if request.method == 'POST':
        item_id = request.form['item_id']
        item_no = int(request.form['item_no'])
        discount = int(request.form['discount'])
        now = datetime.datetime.now()
        sale_id = "S" + now.strftime("%Y%m%d%H%M%S")
        mycursor.execute("SELECT rate FROM product WHERE product_id=%s", (item_id,))
        res = mycursor.fetchone()
        if not res:
            flash('Product ID not found!')
            return redirect(url_for('sale_product'))
        rate = res['rate']
        sale_rate = rate - (rate * discount / 100)
        amount = item_no * sale_rate
        date = now.strftime("%Y-%m-%d")
        sql = """INSERT INTO sales (sale_id, item_id, no_of_item_sold, sale_rate, amount, date_of_sale)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        mycursor.execute(sql, (sale_id, item_id, item_no, sale_rate, amount, date))
        mydb.commit()
        # Update stock
        mycursor.execute("SELECT Instock FROM stock WHERE item_id=%s", (item_id,))
        res = mycursor.fetchone()
        if not res:
            flash('Stock record not found!')
            return redirect(url_for('sale_product'))
        instock = res['Instock'] - item_no
        status = "Yes" if instock > 0 else "No"
        mycursor.execute("UPDATE stock SET Instock=%s, status=%s WHERE item_id=%s", (instock, status, item_id))
        mydb.commit()
        flash('Product sold successfully!')
        return redirect(url_for('view_sales'))
    return render_template('sale_product.html')

@app.route('/view_sales')
def view_sales():
    mycursor.execute("""SELECT product.product_id, product.PName, product.brand, sales.no_of_item_sold, sales.date_of_sale, sales.amount
                        FROM product INNER JOIN sales ON product.product_id=sales.item_id""")
    sales = mycursor.fetchall()
    return render_template('view_sales.html', sales=sales)

if __name__ == '__main__':
    app.run(debug=True)