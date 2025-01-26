# dbms_sim.py
# Daniel Pavenko
# This project serves as a DBMS "simulator"

import os
import re
import time

FILE = "fun.dat"

# Main
def main():
    create_file(FILE)
    handle_ui()

# Adds an entry to the file
def add_to_file(file_name, data):
    with open(file_name, "a") as file:
        data += "\n"
        file.write(data)

# Creates a file if one doesnt already exist
def create_file(file_name):
    try:
        with open(file_name, "x"):
            pass
    except FileExistsError:
        pass

# Clears console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Returns a list of all lines in file_name stripped of trailing newlines
def read_file_entries(file_name):
    entries = []
    with open(file_name, "r") as file:
        for line in file:
            entries.append(line.rstrip("\n\r"))
    return entries

# Prints each entry from the file with a line number
def print_file_entries(file_name):
    entries = read_file_entries(file_name)
    print(f"{file_name} data:")
    for idx, entry in enumerate(entries, start = 1):
        print(f"{idx}: {entry}")
    return entries

# Checks if the data matches the pattern (Color, Zipcode, State Abbreviation)
def check_data_format(data):
    pattern = r'^\s*([A-Za-z ]{1,20})\s*,\s*(\d{5})\s*,\s*([A-Z]{2})\s*$'
    return bool(re.match(pattern, data))

# Ensures that:
# - Color is exactly 8 chars (padded or truncated).
# - Zipcode is left as-is for now; we rely on separate zfill logic on update
# - State is 2 chars.
def pad_data(data):
    split_data = data.split(", ")
    if len(split_data) == 3:
        color, zipcode, state = split_data
        # Color padded to 8 chars
        color_padded = color.ljust(8)[:8]
        return f"{color_padded},{zipcode},{state}"
    else:
        # If user input doesn't have 3 parts, just handle color part
        return data[:8].ljust(8)

# Truncates data (really just our color)
def truncate_data(data):
    split_data = data.split(",")
    if len(split_data) == 3:
        color = split_data[0][:8]
        zipcode = split_data[1]
        state = split_data[2]
        return f"{color},{zipcode},{state}"
    else:
        return data[:8].ljust(8)

# Checks if entry exists
def check_entries_existance(entry):
    with open(FILE, "r") as file:
        for line in file:
            if line.rstrip("\n\r") == entry:
                return True
    return False

# Overwrites just color portion of line
def update_color(entry, new_color):
    with open(FILE, "r+") as file:
        while True:
            pos = file.tell()
            line = file.readline()

            # If we're at the eol
            if not line:
                break

            stripped_line = line.rstrip('\n').rstrip('\r') # For more accurate comparison
            if stripped_line == entry:
                # Color is at positions [0..7]
                file.seek(pos)
                file.write(new_color)
                return

# Overwrites just zipcode portion of line
def update_zipcode(entry, new_zipcode):
    new_zipcode = new_zipcode.strip()
    new_zipcode_padded = new_zipcode.zfill(5)[:5]  # "123" -> "00123" (pads with zeros from the front)

    with open(FILE, 'r+') as file:
        while True:
            pos = file.tell()
            line = file.readline()

            # If we're at the eol
            if not line:
                break

            stripped_line = line.rstrip('\n').rstrip('\r') # For more accurate comparison
            if stripped_line == entry:
                # Format: Color (8 chars) + "," (1 char) => total 9 chars
                # Zipcode is next 5 characters => positions [9..13]
                zipcode_start_pos = pos + 9
                file.seek(zipcode_start_pos)
                file.write(new_zipcode_padded)
                return

# Overwrites just state portion of line
def update_state(entry, new_state):
    new_state_padded = new_state.ljust(2)[:2]

    with open(FILE, 'r+') as file:
        while True:
            pos = file.tell()
            line = file.readline()

            # If we're at the eol
            if not line:
                break

            stripped_line = line.rstrip('\n').rstrip('\r') # For more accurate comparison
            if stripped_line == entry:
                # Format:
                #  Color (8 chars) + "," (1 char) + Zipcode (5 chars) + "," (1 char) = 15 chars total
                #  State is at positions [15..16]
                state_start_pos = pos + 15
                file.seek(state_start_pos)
                file.write(new_state_padded)
                return

# Handles the CLI ui
def handle_ui():
    while True:
        clear_console()
        entries = print_file_entries(FILE)
        print("\n1: Add data to the file")
        print("2: Update existing data within file")
        print("9: Exit")

        response = input().strip()

        match response:
            case "1":
                while True:
                    clear_console()
                    print("data format: (Color, Zipcode (00000-99999), State Abbreviation)")
                    print("9: Exit.")
                    entry_response = input("").strip()
                    if entry_response == "9":
                        exit()

                    # Check if the format is valid
                    if check_data_format(entry_response):
                        # Format/pad the input
                        formatted_entry = truncate_data(pad_data(entry_response))
                        # Check if that exact line already exists
                        if check_entries_existance(formatted_entry):
                            print("Entry already exists! Please try again.")
                            time.sleep(1.5)
                        else:
                            add_to_file(FILE, formatted_entry)
                            break
                    else:
                        print("Invalid format! Please try again.")
                        time.sleep(1.5)

            case "2":
                while True:
                    clear_console()
                    entries = print_file_entries(FILE)
                    if not entries:
                        print("\nNo entries to update. Returning to main menu.")
                        time.sleep(1.5)
                        break

                    print("\nEnter the line number you would like to update")
                    print("9: Exit")
                    line_choice = input("").strip()
                    if line_choice == "9":
                        exit()

                    # Check if our line choice is a digit or not
                    if not line_choice.isdigit():
                        print("Invalid input! Please enter a line number.")
                        time.sleep(1.5)
                        continue

                    line_index = int(line_choice)
                    if line_index < 1 or line_index > len(entries):
                        print("Invalid line number! Please try again.")
                        time.sleep(1.5)
                        continue

                    # We have a valid entry index
                    entry_to_update = entries[line_index - 1]  # zero-based index
                    while True:
                        clear_console()
                        print_file_entries(FILE)
                        print(f"\nYou selected line #{line_index}: {entry_to_update}")
                        print("\n1: Change color")
                        print("2: Change Zipcode")
                        print("3: Change state abbreviation")
                        print("9: Exit")

                        entry_update_section_response = input("").strip() # Strip so that we get rid of trailing spaces
                        match entry_update_section_response:
                            case "1":
                                # Change color logic
                                clear_console()
                                split_entry = entry_to_update.split(",")
                                entry_color = split_entry[0]
                                print(f"Current entry's color: '{entry_color}'")
                                print("Enter the new color (up to 8 chars)")
                                print("9: Exit")
                                new_color_response = input("").strip()
                                if new_color_response == "9":
                                    exit()

                                # Pad/truncate the color to exactly 8 chars
                                new_color = pad_data(new_color_response)[:8]
                                update_color(entry_to_update, new_color)
                                break

                            case "2":
                                # Change zipcode logic
                                clear_console()
                                split_entry = entry_to_update.split(",")
                                entry_zip_code = split_entry[1]
                                print(f"Current entry's zip code: '{entry_zip_code}'")
                                print("Enter the new zip code (will be zero-padded to 5 digits)")
                                print("9: Exit")
                                new_zip_code_response = input("").strip()
                                if new_zip_code_response == "9":
                                    exit()

                                # Call update_zipcode directly with user input
                                update_zipcode(entry_to_update, new_zip_code_response)
                                break

                            case "3":
                                # Change state logic
                                clear_console()
                                split_entry = entry_to_update.split(",")
                                entry_state = split_entry[2] if len(split_entry) > 2 else ""
                                print(f"Current entry's state abbreviation: '{entry_state}'")
                                print("Enter the new 2-letter state abbreviation")
                                print("9: Exit")
                                new_state_response = input("").strip()
                                if new_state_response == "9":
                                    exit()

                                # Overwrite the 2-char state in place
                                update_state(entry_to_update, new_state_response)
                                break

                            case "9":
                                exit()

                            case _:
                                print("Invalid response! Please try again.")
                                time.sleep(1.5)

                    # After any single update, break to show the main menu again
                    break

            case "9":
                exit()

            case _:
                print("Invalid response! Please try again.")
                time.sleep(1.5)

# Entry point
if __name__ == "__main__":
    main()
    