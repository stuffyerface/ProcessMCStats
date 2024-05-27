import os
import json
import csv

# Function to find all JSON files in the current directory
def find_json_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json')]

# Function to read a JSON file and return its data
def read_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to get file size
def get_file_size(filepath):
    return os.path.getsize(filepath)

# Function to extract play time from the JSON data
def get_play_time(data):
    try:
        return data['stats']['minecraft:custom']['minecraft:play_time']
    except KeyError:
        return 0
    
# Function to extract joins/leaves from the JSON data
def get_join_leave(data):
    try:
        return data['stats']['minecraft:custom']['minecraft:leave_game']
    except KeyError:
        return 0
    
# Function to extract item uses from the JSON data
def get_uses(data):
    try:
        hold = data['stats']['minecraft:used']
        count = 0
        for x in hold:
            count += hold[x]
        return count
    except KeyError:
        return 0

# Main function to process JSON files and create a CSV file
def process_json_files_to_csv(output_csv):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_files = find_json_files(current_directory)

    # Prepare data for CSV
    csv_data = []

    for json_file in json_files:
        file_path = os.path.join(current_directory, json_file)
        data = read_json_file(file_path)
        file_size = get_file_size(file_path)
        play_time = get_play_time(data)
        join_leave = get_join_leave(data)
        uses = get_uses(data)
        uuid = os.path.splitext(json_file)[0]
        csv_data.append({
            'uuid': uuid,
            'file_size': file_size,
            'play_time': play_time,
            'join_leave': join_leave,
            'uses': uses
        })

    # Write data to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['uuid', 'file_size', 'play_time', 'join_leave', 'uses']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"Data successfully written to {output_csv}")

if __name__ == "__main__":
    output_csv = 'output.csv'
    process_json_files_to_csv(output_csv)