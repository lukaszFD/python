import csv
import re

# Define the input and output file names
INPUT_FILE = 'account_data.csv'
OUTPUT_FILE = 'parsed_accounts.csv'

DESCRIPTION_PATTERN = re.compile(r"(\w+):(\w+)/(\w+)")

def parse_csv_data(input_filename, output_filename):
    """
    Reads account data from a CSV, parses the Description field using regex,
    and converts the IsActive field to a boolean.
    """
    print(f"INFO: Starting to process file: {input_filename}")

    parsed_data = []

    try:
        with open(input_filename, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)

            # Prepare the fieldnames for the output file
            fieldnames = reader.fieldnames + ['AccountType', 'AccountCode', 'AccountPriority', 'IsActive_Bool']

            for row in reader:
                # 1. Parse the Description field using regex
                description = row['Description']
                match = DESCRIPTION_PATTERN.search(description)

                account_type = None
                account_code = None
                account_priority = None

                if match:
                    account_type = match.group(1)
                    account_code = match.group(2)
                    account_priority = match.group(3)
                else:
                    print(f"WARNING: No regex match found for AccountID {row['AccountID']}. Description: {description}")

                # 2. Convert 'IsActive' field to a boolean representation
                is_active_bool = row['IsActive'].upper() == 'YES'

                # Create the new parsed row
                parsed_row = {
                    'AccountID': row['AccountID'],
                    'Username': row['Username'],
                    'CreationDate': row['CreationDate'],
                    'IsActive': row['IsActive'],
                    'AccessLevel': row['AccessLevel'],
                    'Description': description,
                    'AccountType': account_type,
                    'AccountCode': account_code,
                    'AccountPriority': account_priority,
                    'IsActive_Bool': is_active_bool
                }

                parsed_data.append(parsed_row)

    except FileNotFoundError:
        print(f"ERROR: Input file not found: {input_filename}")
        return

    # Write the parsed data to a new CSV file
    try:
        with open(output_filename, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(parsed_data)

        print(f"INFO: Successfully processed {len(parsed_data)} records.")
        print(f"INFO: Results saved to {output_filename}")

    except Exception as e:
        print(f"CRITICAL: An error occurred during writing the output file: {e}")

if __name__ == "__main__":
    parse_csv_data(INPUT_FILE, OUTPUT_FILE)