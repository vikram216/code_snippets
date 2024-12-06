import os
import csv

def split_csv(file_path, max_size_mb=249):
    """
    Splits a CSV file into smaller files if its size exceeds max_size_mb.
    Ensures records remain intact during the split.
    """
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # File size in MB
    if file_size_mb <= max_size_mb:
        return [file_path]  # No splitting needed

    base_name, ext = os.path.splitext(os.path.basename(file_path))
    output_files = []
    part_number = 1

    with open(file_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Get the header row

        # Start writing the first part
        output_file = f"{base_name}_part{part_number}{ext}"
        output_files.append(output_file)
        outfile = open(output_file, 'w', newline='', encoding='utf-8')
        writer = csv.writer(outfile)
        writer.writerow(header)

        current_size = outfile.tell() / (1024 * 1024)  # Current output file size in MB

        for row in reader:
            writer.writerow(row)
            current_size = outfile.tell() / (1024 * 1024)  # Update file size

            # Check if the current file exceeds the max size
            if current_size >= max_size_mb:
                outfile.close()  # Close current file
                part_number += 1
                output_file = f"{base_name}_part{part_number}{ext}"
                output_files.append(output_file)
                outfile = open(output_file, 'w', newline='', encoding='utf-8')
                writer = csv.writer(outfile)
                writer.writerow(header)  # Write header to the new part

        outfile.close()  # Close the last file

    return output_files


def process_directory(directory_path, max_size_mb=249):
    """
    Processes all CSV files in a directory, splits large files, and returns a list of all resulting file names.
    """
    all_files = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            split_files = split_csv(file_path, max_size_mb)
            all_files.extend(split_files)
    return all_files


# Specify the directory containing the CSV files
directory_path = 'path/to/your/directory'

# Process the directory
resulting_files = process_directory(directory_path)

# Print the list of all resulting file names
print("Resulting Files:", resulting_files)
