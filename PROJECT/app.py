import pymongo
from flask import Flask, jsonify, request,render_template
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["trendtrex"]
transaction_collection = db["transactions"]
inventory_collection=db['Inventory']
users_collection=db['user']

product_prices = {
    "rice": 2.5,
    "bread": 1.8,
    "milk": 3.2,
    "salt": 0.5,
    "pasta": 1.2,
    "juice": 1.5,
    "vegetables": 1.8,
    "water": 1.0,
    "juice": 2.2,
    "coffee": 3.5
}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login_page.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    username=''
    password=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    # Check if user exists in the database
    user = users_collection.find_one({'username': username, 'password': password})
    if user:
        return render_template('home_page.html', username=username)
    else:
        error_message = "Invalid username or password"
        return render_template('login_page.html', error=error_message, username=username)

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():

    inventory_data = list(inventory_collection.find())
    
    return render_template('inventory.html', inventory_data=inventory_data)

@app.route('/insight', methods=['GET', 'POST'])
def insight():
        # Retrieve transaction data from MongoDB
    cursor = transaction_collection.find({})
    transactions_data = []
    for doc in cursor:
        items = [(item['name'], item['quantity']) for item in doc['items']]
        transactions_data.append(items)


    
    te = TransactionEncoder()
    te_ary = te.fit(transactions_data).transform(transactions_data)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)

    min_itemset_size = 2
    filtered_itemsets = frequent_itemsets[frequent_itemsets['itemsets'].apply(lambda x: len(x)) >= min_itemset_size]
    itemsets_list = [', '.join(item[0] for item in itemset) for itemset in filtered_itemsets['itemsets']]

    print(itemsets_list)
    # Pass itemsets data to the template
    return render_template('insight.html', itemsets=itemsets_list)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    total_bill = 0

    if request.method == 'POST':
        try:
            transaction_data = request.json
            print('Received Transaction Data:', transaction_data)

            items = transaction_data.get('items', [])
            for item in items:
                name = item.get('name')
                quantity = item.get('quantity')
                if name and name in product_prices and quantity:
                    price = product_prices[name]
                    total_bill += price * quantity

                    # Decrement item quantity in inventory
                    inventory_collection.update_one(
                        {'name': name},
                        {'$inc': {'available': -quantity}}
                    )

            # Insert transaction into MongoDB
            transaction_data['total_bill'] = total_bill
            result = transaction_collection.insert_one(transaction_data)
            print('Insertion Result:', result.inserted_id)  # Print the inserted ID

            print('Total Bill:', total_bill)

            # Return the bill amount back to the client
            return jsonify({'billAmount': total_bill}), 200
        except Exception as e:
            print('Error:', e)
            return jsonify({'error': str(e)}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True)





