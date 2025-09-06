from flask import Flask, request, jsonify, render_template
import mysql.connector
import bcrypt
from flask_cors import CORS
import os # <-- 1. ADD THIS IMPORT

app = Flask(__name__)
CORS(app, supports_credentials=True)

# --- START: MODIFIED DATABASE CONNECTION FOR DEPLOYMENT ---
# This code will now use the production database URL from Render,
# but will fall back to your local database if the environment variables are not found.
db_host = os.environ.get('DB_HOST', 'localhost')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'Root12345')
db_name = os.environ.get('DB_NAME', 'food_security_db')

db = mysql.connector.connect(
    host=db_host,
    port=3306,
    user=db_user,
    password=db_password,
    database=db_name
)
# --- END: MODIFIED DATABASE CONNECTION ---


inspector_credentials = [
    {'username': 'inspector1', 'password': 'ipass1', 'id': 1},
    {'username': 'inspector2', 'password': 'ipass2', 'id': 2},
    {'username': 'inspector3', 'password': 'ipass3', 'id': 3}
]

@app.route('/')
def index():
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
    return render_template('inspector_dashboard.html')

@app.route('/add_hotel')
def add_hotel_page():
    return render_template('add_hotel.html')

@app.route('/submit_feedback_page')
def submit_feedback_page():
    return render_template('submit_feedback.html')

@app.route('/report_food_poisoning_page')
def report_food_poisoning_page():
    return render_template('report_food_poisoning.html')

@app.route('/customer_signup')
def customer_signup_page():
    return render_template('customer_signup.html')

@app.route('/hotelman_signup')
def hotel_signup_page():
    return render_template('hotel_signup.html')

@app.route('/update_case/<int:case_id>')
def update_case_page(case_id):
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM food_poisoning_cases WHERE case_id = %s"
        cursor.execute(query, (case_id,))
        case = cursor.fetchone()
        cursor.close()
        if case:
            return render_template('update_case.html', case=case)
        else:
            return "Case not found", 404
    except Exception as e:
        return f"Database error: {str(e)}", 500

@app.route('/my_reports_page')
def my_reports_page():
    return render_template('my_reports.html')

# --- API Routes ---

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
        return jsonify({'message': 'Login successful!', 'customer_id': customer['id']}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/inspector_login', methods=['POST'])
def inspector_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    for creds in inspector_credentials:
        if creds['username'] == username and creds['password'] == password:
            return jsonify({'message': 'Login successful!', 'inspector_id': creds['id']}), 200
    
    return jsonify({'message': 'Invalid credentials!'}), 401

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
    if request.method == 'POST':
        try:
            data = request.json
            
            name = data.get('name')
            address = data.get('address')
            contact_number = data.get('contact_number')
            email = data.get('email')
            license_number = data.get('license_number')
            rating = data.get('rating')
            last_inspection_date = data.get('last_inspection_date')
            status = data.get('status')

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
    else:
        try:
            cursor = db.cursor()
            query = "SELECT * FROM hotels WHERE status = 'Active'"
            cursor.execute(query)
            hotels = cursor.fetchall()
            cursor.close()
            return jsonify(hotels)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

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

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
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

@app.route('/feedback_page')
def feedback_page():
    return render_template('hotel_feedback.html')

@app.route('/api/hotel_feedback', methods=['GET'])
def get_hotel_feedback():
    hotel_id = request.args.get('hotel_id')
    if not hotel_id:
        return jsonify({'message': 'Hotel ID is required'}), 400
    
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM customer_feedback WHERE hotel_id = %s ORDER BY feedback_date DESC"
        cursor.execute(query, (hotel_id,))
        feedback = cursor.fetchall()
        cursor.close()
        return jsonify(feedback)
    except Exception as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500

@app.route('/food_poisoning_cases', methods=['POST'])
def add_food_poisoning_case():
    try:
        data = request.json
        customer_id = data.get('customer_id') 

        query = """
            INSERT INTO food_poisoning_cases (hotel_id, report_date, symptoms, number_of_people_affected, investigation_status, conclusion, customer_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get('hotel_id'), 
            data.get('report_date'), 
            data.get('symptoms'),
            data.get('number_of_people_affected'),
            'Pending', 
            '',
            customer_id
        )
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        return jsonify({'message': 'Report submitted successfully. An inspector will review it shortly.'}), 201
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'message': 'An error occurred while submitting the report.'}), 500

@app.route('/view_food_poisoning_cases')
def view_food_poisoning_cases_page():
    return render_template('view_food_poisoning_cases.html')

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

@app.route('/start_inspection_page')
def start_inspection_page():
    return render_template('start_inspection.html')

@app.route('/inspection_form/<int:hotel_id>')
def inspection_form(hotel_id):
    return render_template('inspection_form.html', hotel_id=hotel_id)

@app.route('/api/inspections', methods=['POST'])
def add_inspection():
    try:
        data = request.json
        
        query = """
            INSERT INTO inspections (hotel_id, inspection_date, inspector_id, overall_result, comments)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data.get('hotel_id'),
            data.get('inspection_date'),
            data.get('inspector_id'),
            data.get('overall_result'),
            data.get('comments')
        )

        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return jsonify({'message': 'Inspection submitted successfully!'}), 201

    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'message': 'An error occurred while submitting the inspection.'}), 500

@app.route('/api/inspections_summary')
def inspections_summary():
    hotel_id = request.args.get('hotel_id')
    if not hotel_id:
        return jsonify({"error": "Hotel ID is required"}), 400

    try:
        cursor = db.cursor()
        
        query_passed = "SELECT COUNT(*) FROM inspections WHERE hotel_id = %s AND overall_result = 'Passed'"
        cursor.execute(query_passed, (hotel_id,))
        passed_count = cursor.fetchone()[0]

        query_failed = "SELECT COUNT(*) FROM inspections WHERE hotel_id = %s AND overall_result IN ('Failed', 'Needs Improvement')"
        cursor.execute(query_failed, (hotel_id,))
        failed_count = cursor.fetchone()[0]
        
        cursor.close()

        summary = {
            "passed": passed_count,
            "failed": failed_count
        }
        return jsonify(summary)

    except Exception as e:
        print(f"Database error in inspections_summary: {str(e)}")
        return jsonify({"error": "Database error"}), 500

@app.route('/inspections_page')
def inspections_page():
    return render_template('inspections.html')

@app.route('/api/hotel_inspections')
def get_hotel_inspections():
    hotel_id = request.args.get('hotel_id')
    if not hotel_id:
        return jsonify({"error": "Hotel ID is required"}), 400

    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM inspections WHERE hotel_id = %s ORDER BY inspection_date DESC"
        cursor.execute(query, (hotel_id,))
        inspections = cursor.fetchall()
        cursor.close()
        return jsonify(inspections)

    except Exception as e:
        print(f"Database error in get_hotel_inspections: {str(e)}")
        return jsonify({"error": "Database error"}), 500

@app.route('/api/update_case/<int:case_id>', methods=['POST'])
def update_case(case_id):
    try:
        data = request.json
        status = data.get('investigation_status')
        conclusion = data.get('conclusion')
        
        cursor = db.cursor()
        query = "UPDATE food_poisoning_cases SET investigation_status = %s, conclusion = %s WHERE case_id = %s"
        cursor.execute(query, (status, conclusion, case_id))
        db.commit()
        cursor.close()
        
        return jsonify({'message': 'Case updated successfully!'})
    except Exception as e:
        db.rollback()
        return jsonify({'message': f'Database error: {str(e)}'}), 500

@app.route('/api/my_reports', methods=['GET'])
def get_my_reports():
    customer_id = request.args.get('customer_id')
    if not customer_id:
        return jsonify({'message': 'Customer ID is required'}), 400
    
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM food_poisoning_cases WHERE customer_id = %s ORDER BY report_date DESC"
        cursor.execute(query, (customer_id,))
        reports = cursor.fetchall()
        cursor.close()
        return jsonify(reports)
    except Exception as e:
        return jsonify({'message': f'Database error: {str(e)}'}), 500

# --- 2. REMOVE THIS BLOCK ---
# if __name__ == '__main__':
#     app.run(debug=True)

