import subprocess
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Initialize a list to store deleted item IDs
deleted_item_ids = []

# Initialize a list to store selected item IDs
selected_item_ids = []

# Initialize a list to store the sections
sections = []

def parse_txt_file(file_path):
    parsed_sections = []
    current_section = None

    with open(file_path, 'r') as file:
        lines = file.readlines()
        skip_next_two_lines = False
        for line in lines:
            line = line.strip()
            if line.isdigit():
                if current_section:
                    parsed_sections.append(current_section)
                current_section = {'id': int(line), 'items': []}
                skip_next_two_lines = False
            elif current_section and not skip_next_two_lines:
                current_section['items'].append(line)
                if current_section['id'] in deleted_item_ids:
                    skip_next_two_lines = True

        if current_section:
            parsed_sections.append(current_section)

    return parsed_sections


# Read and parse the text file at the start of the Flask app
your_text_file_path = 'file2.txt'  # Replace with the actual path to your text file
sections = parse_txt_file(your_text_file_path)
@app.route('/')
def index():
    file_path = 'file2.txt'  # Replace with the actual path to your text file
    sections = parse_txt_file(file_path)
    return render_template('index.html', sections=sections, deleted_item_ids=deleted_item_ids)

@app.route('/delete_item', methods=['POST'])
def delete_item():
    global sections  # Use the global 'sections' variable

    if 'delete_selected' in request.form:
        selected_item_ids = request.form.getlist('selected_items[]')
    
        # Convert selected_item_ids to integers
        selected_item_ids = [int(id) for id in selected_item_ids]

        # Add selected item IDs to the deleted_item_ids list
        deleted_item_ids.extend(selected_item_ids)

        # Filter the sections to exclude the selected items
        sections = [section for section in sections if section['id'] not in selected_item_ids]

        # Update the your_text_file.txt with the modified sections
        with open(your_text_file_path, 'w') as file:
            for section in sections:
                file.write(str(section['id']) + '\n')
                for item in section['items']:
                    file.write(item + '\n')

        # Return a JSON response to the AJAX request
        file_path = 'file2.txt'
        sections = parse_txt_file(file_path)
        return jsonify({'message': 'Items deleted successfully'})

    return jsonify({'message': 'No items selected'})

@app.route('/save_to_file', methods=['POST'])
def save_to_file():
    try:
        # Execute the shell command 'python finder.py'
        subprocess.run(['python', 'finder.py'], check=True)
        return jsonify({'message': 'File saved successfully'})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Error saving file'})
if __name__ == '__main__':
    app.run(debug=True)
