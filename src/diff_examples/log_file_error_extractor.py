***REMOVED***

def extract_errors(log_file):
    """
    Reads a log file and extracts error messages.

    :param log_file: Path to the log file.
    :return: A list of extracted error messages.
    """
    error_pattern = re.compile(r'ERROR:\s*(.*)')
    errors = []

    try:
        with open(log_file, 'r', encoding='utf-8') as file:
            for line in file:
                match = error_pattern.search(line)
                if match:
                    errors.append(match.group(1))
    except FileNotFoundError:
        print(f"File '{log_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return errors

if __name__ == "__main__":
    log_path = "system.log"
    extracted_errors = extract_errors(log_path)

    if extracted_errors:
        print("Extracted Errors:")
        for error in extracted_errors:
            print(f"- {error}")
    else:
        print("No errors found in the log file.")
