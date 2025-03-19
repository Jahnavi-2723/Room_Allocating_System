from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template("front.html")


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'group_csv' not in request.files or 'hostel_csv' not in request.files:
        return jsonify({"error": "Both CSV files are required"}), 400

    group_file = request.files['group_csv']
    hostel_file = request.files['hostel_csv']

    group_df = pd.read_csv(group_file)
    hostel_df = pd.read_csv(hostel_file)

    allocated_rooms = allocate_rooms(group_df, hostel_df)

    # Save allocated rooms to CSV
    allocated_csv_path = os.path.join(UPLOAD_FOLDER, "allocated_rooms.csv")
    allocated_rooms.to_csv(allocated_csv_path, index=False)

    return jsonify({"message": "Allocation Complete", "download_url": "/download"})

@app.route('/download', methods=['GET'])
def download_file():
    allocated_csv_path = os.path.join(UPLOAD_FOLDER, "allocated_rooms.csv")
    return send_file(allocated_csv_path, as_attachment=True)

def allocate_rooms(groups, hostels):
    allocated_data = []
    
    # Sample allocation logic
    for index, row in groups.iterrows():
        student_name = row['Name']
        gender = row['Gender']
        hostel_row = hostels[hostels['Gender'] == gender].sample(n=1)
        room_number = hostel_row['Room Number'].values[0]
        allocated_data.append({"Name": student_name, "Gender": gender, "Room": room_number})
    
    return pd.DataFrame(allocated_data)

if __name__ == '__main__':
    app.run(debug=True)
