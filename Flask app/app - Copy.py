from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Initialize a list to store deleted item IDs
deleted_item_ids = []

def parse_txt_file(file_path):
    sections = []
    current_section = None

    with open(file_path, 'r') as file:
        lines = file.readlines()
        skip_next_two_lines = False
        for line in lines:
            line = line.strip()
            if line.isdigit():
                if current_section:
                    sections.append(current_section)
                current_section = {'id': int(line), 'items': []}
                skip_next_two_lines = False
            elif current_section and not skip_next_two_lines:
                current_section['items'].append(line)
                if current_section['id'] in deleted_item_ids:
                    skip_next_two_lines = True

        if current_section:
            sections.append(current_section)

    return sections


@app.route('/')
def index():
    file_path = 'file1.txt'  # Replace with the actual path to your text file
    sections = parse_txt_file(file_path)
    return render_template('index.html', sections=sections, deleted_item_ids=deleted_item_ids)

@app.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = int(request.form['item_id'])
    deleted_item_ids.append(item_id)
    return redirect('/')

@app.route('/save_to_file', methods=['POST'])
def save_to_file():
    # Define the source text file and new output file
    source_file_path = "file1.txt"
    output_file_path = 'output.txt'  # Replace with your desired output file path

    # Create a flag to indicate if we should save the next two lines
    save_next_two_lines = False

    # Open the source file for reading and the output file for writing
    with open(source_file_path, 'r') as source_file, open(output_file_path, 'w') as output_file:
        # Iterate through the lines in the source file
        for line in source_file:
            line = line.strip()
            if line.isdigit():
                # Check if the current line is a deleted item ID
                item_id = int(line)
                if item_id in deleted_item_ids:
                    # If it's a deleted ID, set the flag to save the next two lines
                    save_next_two_lines = True
                else:
                    # If it's not a deleted ID, clear the flag
                    save_next_two_lines = False
            elif save_next_two_lines:
                # If the flag is set, save the line to the output file
                output_file.write(line + '\n')

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
