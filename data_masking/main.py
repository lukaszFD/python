import csv
from cipher import transform_id, transform_host, hash_name, reverse_transform_id, reverse_transform_host


def mask_file(input_path, output_path):
    """Masks the input CSV file and saves the result to the output CSV file."""
    with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)  # Add quoting
            writer.writeheader()

            for row in reader:
                row['ID'] = transform_id(row['ID'])
                row['Host'] = transform_host(row['Host'])
                row['Name'] = hash_name(row['Name'])
                writer.writerow(row)

def unmask_file(input_path, output_path):
    """Unmasks the input CSV file and saves the result to the output CSV file."""
    with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for row in reader:
                row['ID'] = reverse_transform_id(row['ID'])
                row['Host'] = reverse_transform_host(row['Host'])
                # Note: 'Name' cannot be reversed from hash
                row['Name'] = 'HASHED (Cannot be reversed)'
                writer.writerow(row)

if __name__ == "__main__":
    # Input and output file paths
    input_file = r"C:\...\data_masking\platform.csv"
    output_file = r"C:\...\data_masking\platform_out.csv"

    unmask_input_file = r"C:\...\data_masking\platform_out.csv"
    unmask_output_file = r"C:\...\data_masking\platform_unmasked.csv"

    # Mask the file
    mask_file(input_file, output_file)

    # Unmask the file
    unmask_file(unmask_input_file, unmask_output_file)