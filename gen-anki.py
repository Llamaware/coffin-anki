import csv
import re
import string

input_file = 'dialogue.csv'
output_file = 'output.csv'

rows_by_id = {}
sort_number = 1
written_rows = set()

HEADER_ROW = ['ID', 'Source', 'English', 'Translation']

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

def contains_only_punctuation(text):
    return all(char in string.punctuation or char.isspace() for char in text)

def remove_tags(text):
    # Remove backslash tags (e.g., \fi, \fr, etc.)
    text = re.sub(r'\\\w+', '', text)

    # Remove bracket tags (e.g., \c[1], \f[2], etc.)
    text = re.sub(r'\[.*?\]', '', text)
    
    return text

# Initialize an empty dictionary to store the speaker to translated name mapping
speaker_translation_map = {}

# First, read the input file and process the "Speakers" section to build the mapping
with open(input_file, newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)

    # Skip rows until we find the "Speakers" section header
    while True:
        row = next(reader)
        if row == ['Speakers', 'English', 'Translation', '']:
            break  # We found the "Speakers" section header, exit the loop

    # Now, read the speaker data until we hit `,,,`
    for row in reader:
        if row == ['','','','']:  # Detect the row with three commas (,,,) and stop reading the speaker section
            break

        if len(row) >= 3:  # Ensure it's a valid row with at least 3 columns
            speaker_id = row[1]
            translated_name = row[2]  # Assuming the second column contains the translated name
            speaker_translation_map[speaker_id] = translated_name

    # Debug: Print the speaker translation map
    print("Speaker Translation Map:")
    print(speaker_translation_map)

    while True:
        row = next(reader)
        if row == HEADER_ROW:
            break

    # Now, start processing the remaining rows (the actual data rows)
    for row in reader:
        # Skip rows that exactly match the header row
        if row == HEADER_ROW:
            continue
        
        # Skip rows that have fewer than 4 columns or any blank column
        if len(row) < 4 or any(col.strip() == '' for col in row):
            continue
        
        # Extract relevant columns: ID, English, Translation, Speaker
        row_id = row[0]
        english = remove_tags(normalize_whitespace(row[2].strip('"')))
        translation = remove_tags(normalize_whitespace(row[3].strip('"')))
        speaker_name = row[1].strip()

        # Skip rows where the speaker contains the word "CHOICE"
        if "CHOICE" in speaker_name.upper():  # .upper() to make the check case-insensitive
            continue

        # Skip rows where English contains only punctuation
        if contains_only_punctuation(english):
            continue

        if len(english.split()) < 2:
            continue

        # Store the rows in rows_by_id, without concatenating during the loop
        if row_id not in rows_by_id:
            rows_by_id[row_id] = {
                'english': english,
                'translation': translation,
                'speaker_name': speaker_name
            }
        else:
            # Concatenate the English and translation only if needed
            rows_by_id[row_id]['english'] += " " + english
            rows_by_id[row_id]['translation'] += " " + translation


# Now that all rows have been processed, write them to the output file
with open(output_file, 'a', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile, delimiter='|')

    # Write each row from rows_by_id, ensuring no duplicates
    for row_id, data in rows_by_id.items():
        row_tuple = (data['translation'], data['english'], data['speaker_name'])

        # If this row has already been written, skip it
        if row_tuple in written_rows:
            continue

        # Get the translated name for the speaker from the mapping, if it exists
        translated_name = speaker_translation_map.get(data['speaker_name'], "Other")  # Default to "Unknown" if not found

        # Write this row and add it to the set of written rows
        writer.writerow([sort_number, data['translation'], data['english'], translated_name, data['speaker_name']])
        written_rows.add(row_tuple)
        sort_number += 1

print("CSV file has been processed and saved to:", output_file)
