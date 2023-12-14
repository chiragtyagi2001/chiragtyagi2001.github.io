import sqlite3

#Open database
conn = sqlite3.connect('database.db',host='localhost', port=3306)

#Create table
conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		firstName TEXT,
		lastName TEXT,
		address1 TEXT,
		address2 TEXT,
		zipcode TEXT,
		city TEXT,
		state TEXT,
		country TEXT, 
		phone TEXT,
		)''')
        
conn.execute('''CREATE TABLE usrinfo
		(userId INTEGER PRIMARY KEY, 
		name TEXT,
		email TEXT,
		sex TEXT,
		state TEXT,
		city TEXT,
		address TEXT,
		contact TEXT,
		password TEXT,
		)''')
        
conn.execute('''CREATE TABLE docinfo
		(docId INTEGER PRIMARY KEY, 
		name TEXT,
		email TEXT,
		sex TEXT,
		state TEXT,
		city TEXT,
		address TEXT,
		contact TEXT,
        specialization TEXT,
        description TEXT,
		password TEXT,
		)''')
        
conn.execute('''CREATE TABLE pharmainfo
		(pharmaId INTEGER PRIMARY KEY, 
		name TEXT,
		email TEXT,
		sex TEXT,
		state TEXT,
		city TEXT,
		address TEXT,
		contact TEXT,
		password TEXT,
		)''')
        
conn.execute('''CREATE TABLE deliveryaddress
		(email TEXT, 
		productId TEXT,
		productNames TEXT,
		quantity TEXT,
		noOfItems INT,
		price TEXT,
		username TEXT,
		address TEXT,
        city TEXT,
        state TEXT,
		contact_number TEXT,
		)''')
        
conn.execute('''CREATE TABLE appoint 
		(doc_name TEXT
		email TEXT,
		patient_name TEXT,
		gender TEXT,
		patient_age TEXT,
		date TEXT,
		time TEXT,
		phn_number TEXT,
		fee TEXT,
		)''')

conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		description TEXT,
		image TEXT,
		stock INTEGER,
		categoryId INTEGER,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')

conn.execute('''CREATE TABLE kart
		(userId INTEGER,
		productId INTEGER,
        quantity INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId),
        FOREIGN KEY(quantity) REFERENCES products(quantity)
		)''')
        
#cur.execute('''ALTER TABLE kart ADD COLUMN quantity INTEGER
#        ''')

conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')
        

conn.close()

