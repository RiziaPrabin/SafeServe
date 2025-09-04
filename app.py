from flask import Flask, request, jsonify, render_template
import mysql.connector
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

# --- Database Connection ---
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Root12345",
    database="food_security_db"
)

# --- Route to Serve the Main HTML Page ---
inspector_credentials = [
    {'username': 'inspector1', 'password': 'inspectpass1'},
    {'username': 'inspector2', 'password': 'inspectpass2'},
    {'username': 'inspector3', 'password': 'inspectpass3'}
]


@app.route('/')
def index():
    # This renders the mainsignup_page.html file from your 'templates' folder.
    return render_template('mainsignup_page.html')

# --- Page Rendering Routes ---

@app.route('/customer_login_page')
def customer_login_page():
    return render_template('customer_login.html')

@app.route('/home')
def home():
    return render_template('customer_home.html')

@app.route('/hotel_login_page')
def hotel_login_page():
    return render_template('hotel_login.html')

@app.route('/hotel_dashboard')
def hotel_dashboard():
    return render_template('hotel_dashboard.html')


@app.route('/inspector_login_page')
def inspector_login_page():
    return render_template('inspector_login.html')

@app.route('/inspector_dashboard')
def inspector_dashboard():
    # This route will find and display your 'dashbo.html' file.
    return render_template('inspector_dashboard.html')

@app.route('/add_hotel')
def add_hotel_page():
    # This route will find and display your 'add_hotel.html' file.
    return render_template('add_hotel.html')
# Add these new page rendering routes to your app.py

@app.route('/submit_feedback_page')
def submit_feedback_page():
    # Make sure you have a file named 'submit_feedback.html' in your templates folder
    return render_template('submit_feedback.html')

@app.route('/report_food_poisoning_page')
def report_food_poisoning_page():
    # Make sure you have a file named 'report_food_poisoning.html' in your templates folder
    return render_template('report_food_poisoning.html')
# --- ADD THIS NEW ROUTE ---
@app.route('/customer_signup')
def customer_signup_page():
    # This tells Flask what to do when the user clicks the "Sign Up" link
    return render_template('customer_signup.html')
# -------------------------
@app.route('/hotelman_signup')
def hotel_signup_page():
    # This tells Flask what to do when the user clicks the "Sign Up" link
    return render_template('hotel_signup.html')
# -------------------------

@app.route('/customer_login', methods=['POST'])
def customer_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM customers WHERE username = %s"
    cursor.execute(query, (username,))
    customer = cursor.fetchone()
    cursor.close()

    if customer and bcrypt.checkpw(password.encode('utf-8'), customer['password'].encode('utf-8')):
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401
# --- Inspector API Routes ---



@app.route('/inspector_login', methods=['POST'])
def inspector_login():
    # MODIFIED: This now checks against the hardcoded list instead of the database.
    data = request.json
    username = data.get('username')
    password = data.get('password')

    for creds in inspector_credentials:
        if creds['username'] == username and creds['password'] == password:
            return jsonify({'message': 'Login successful!'}), 200
    
    return jsonify({'message': 'Invalid credentials!'}), 401


# --- Hotel Manager API Routes ---

@app.route('/register_hotel_manager', methods=['POST'])
def register_hotel_manager():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hotel_id = data.get('hotel_id')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = db.cursor()
    query = "INSERT INTO hotel_managers (username, email, password, hotel_id) VALUES (%s, %s, %s, %s)"
    values = (username, email, hashed_password.decode('utf-8'), hotel_id)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    return jsonify({'message': 'Hotel manager registered successfully!'}), 201

@app.route('/hotel_login', methods=['POST'])
def hotel_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM hotel_managers WHERE username = %s"
    cursor.execute(query, (username,))
    manager = cursor.fetchone()
    cursor.close()
    
    if manager and bcrypt.checkpw(password.encode('utf-8'), manager['password'].encode('utf-8')):
        return jsonify({'message': 'Login successful!', 'hotel_id': manager['hotel_id']}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401


@app.route('/hotels', methods=['GET', 'POST'])
def manage_hotels():
    # This block handles ADDING a new hotel
    if request.method == 'POST':
        try:
            data = request.json
            
            # Extract data from the received JSON
            name = data.get('name')
            address = data.get('address')
            contact_number = data.get('contact_number')
            email = data.get('email')
            license_number = data.get('license_number')
            rating = data.get('rating')
            last_inspection_date = data.get('last_inspection_date')
            status = data.get('status')

            # Insert into the database
            cursor = db.cursor()
            query = """
                INSERT INTO hotels (name, address, contact_number, email, license_number, rating, last_inspection_date, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, address, contact_number, email, license_number, rating, last_inspection_date, status)
            
            cursor.execute(query, values)
            db.commit()
            cursor.close()

            return jsonify({'message': 'Hotel added successfully!'}), 201

        except Exception as e:
            db.rollback()
            return jsonify({'message': f'Database error: {str(e)}'}), 500

    # This block handles LISTING all hotels
    else: # This is a GET request
        try:
            cursor = db.cursor()
            query = "SELECT * FROM hotels WHERE status = 'Active'"
            cursor.execute(query)
            hotels = cursor.fetchall()
            cursor.close()
            return jsonify(hotels)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# --- Customer (Public User) API Routes ---

@app.route('/register_customer', methods=['POST'])
def register_customer():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = db.cursor()
    query = "INSERT INTO customers (username, email, password) VALUES (%s, %s, %s)"
    values = (username, email, hashed_password.decode('utf-8'))
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    
    return jsonify({'message': 'Customer registered successfully!'}), 201

# --- START: Add these three new routes to your app.py file ---

# Route 1: Handles the form submission from the customer's 'submit_feedback.html' page.
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
        # These default values are used for fields the customer doesn't fill out
        action_taken = data.get('action_taken', 'Pending Review')
        status = data.get('status', 'New')

        query = """
            INSERT INTO customer_feedback (hotel_id, feedback_date, customer_name, feedback_content, action_taken, status) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get('hotel_id'), data.get('feedback_date'), data.get('customer_name'), 
            data.get('feedback_content'), action_taken, status
        )
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        return jsonify({'message': 'Feedback submitted successfully!'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'message': f'Database error: {str(e)}'}), 500

# Route 2: Renders the HTML page for the hotel owner to view their feedback.
# This is the destination for a link or button on the hotel owner's dashboard.
@app.route('/feedback_page')
def feedback_page():
    return render_template('hotel_feedback.html')

# Route 3: The API endpoint that fetches feedback for a SPECIFIC hotel.
# This is called by the JavaScript on the 'hotel_feedback.html' page.
@app.route('/api/hotel_feedback', methods=['GET'])
def get_hotel_feedback():
    # Gets the hotel_id from the URL (e.g., /api/hotel_feedback?hotel_id=123)
    hotel_id = request.args.get('hotel_id')
    if not hotel_id:
        return jsonify({'message': 'Hotel ID is required'}), 400
    
    try:
        cursor = db.cursor(dictionary=True) # dictionary=True is essential for JSON
        # Selects only the feedback for the specified hotel_id
        query = "SELECT * FROM customer_feedback WHERE hotel_id = %s ORDER BY feedback_date DESC"
        cursor.execute(query, (hotel_id,))
        feedback = cursor.fetchall()
        cursor.close()
        return jsonify(feedback)
    except Exception as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500

# --- END: New routes ---

# Route 1: Handles the POST request from the customer's report form
@app.route('/food_poisoning_cases', methods=['POST'])
def add_food_poisoning_case():
    try:
        data = request.json
        query = """
            INSERT INTO food_poisoning_cases (hotel_id, report_date, symptoms, number_of_people_affected, investigation_status, conclusion) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        # MODIFIED: This now gets the 'number_of_people_affected' directly from the form data
        # sent by the customer's JavaScript.
        values = (
            data.get('hotel_id'), 
            data.get('report_date'), 
            data.get('symptoms'),
            data.get('number_of_people_affected'), # This now comes from the customer's input
            'Pending', # Default status for a new report
            ''         # Default conclusion is empty until an inspector reviews it
        )
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        return jsonify({'message': 'Report submitted successfully. An inspector will review it shortly.'}), 201
    except Exception as e:
        db.rollback()
        # It's good practice to log the error for debugging
        print(f"Database error: {str(e)}")
        return jsonify({'message': 'An error occurred while submitting the report.'}), 500

# Route 2: Renders the page for the inspector to view all cases
@app.route('/view_food_poisoning_cases')
def view_food_poisoning_cases_page():
    return render_template('view_food_poisoning_cases.html')

# Route 3: The API endpoint that provides the data for the inspector's table
@app.route('/api/food_poisoning_cases', methods=['GET'])
def get_food_poisoning_cases():
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM food_poisoning_cases ORDER BY report_date DESC"
        cursor.execute(query)
        cases = cursor.fetchall()
        cursor.close()
        return jsonify(cases)
    except Exception as e:
        print(f"Database error: {str(e)}")
        return jsonify({'message': 'An error occurred while fetching the cases.'}), 500

# --- END: New routes ---



# --- This should be at the very end of the file ---
if __name__ == '__main__':
    app.run(debug=True)
