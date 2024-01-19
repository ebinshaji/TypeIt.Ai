# Function to parse sections from a given text file
def parse_sections(filename):
    sections = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():
                section_number = int(lines[i].strip())
                i += 1  # Move to the next line
                section_lines = []
                while i < len(lines) and lines[i].strip():  # Read section lines until an empty line
                    section_lines.append(lines[i])
                    i += 1
                sections.append((section_number, section_lines))
            else:
                i += 1
    return sections

# Parse sections from both files
file1_sections = parse_sections('file1.txt')
file2_sections = parse_sections('file2.txt')

# Find missing sections
missing_sections = []
for section1 in file1_sections:
    if section1 not in file2_sections:
        missing_sections.append(section1)

# Write missing sections to a new file
with open('missing_sections.txt', 'w') as outfile:
    for section in missing_sections:
        outfile.write(str(section[0]) + '\n')
        outfile.writelines(section[1])
        outfile.write('\n')

print("Missing sections have been saved in 'missing_sections.txt'.")
