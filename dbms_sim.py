# dbms_sim.py
# Daniel Pavenko
# This project serves as a DBMS "simulator"

import os, re, time

FILE = "fun.dat"

# Main method that just starts the UI
def main():
  create_file(FILE)
  handle_ui()

# Adds something to the file
def add_to_file(file_name, data):
  with open(file_name, "a") as file:
    data += "\n"
    file.write(data)

# Updates an already existing thing within the file
def update_file(data):
  pass

# Clears console
def clear_console():
  os.system('cls' if os.name == 'nt' else 'clear')

# Prints the entirety of the file
def print_file(file_name):
  with open(file_name, "r") as file:
    print(f"{file_name} data:")
    for line in file:
      print(line)

# Creates a file with the given file_name
def create_file(file_name):
  try:
    with open(file_name, "x") as file:
     pass
  except FileExistsError:
    pass

# Checks if the data matches the pattern via regex: (Color (8 chars), Zipcode (00000-99999), State (2 char abbreviation))
def check_data_format(data):
  pattern = r'^\s*([A-Za-z ]{1,20})\s*,\s*(\d{5})\s*,\s*([A-Z]{2})\s*$'
  if re.match(pattern, data):
    return True
  return False

# Pad the data with spaces so that the data takes up the required space
def pad_data(data):
  split_data = data.split(", ")
  padded_data = split_data[0].ljust(8, " ") + "," + split_data[1] + "," + split_data[2]
  return padded_data

def truncate_data(data):
  split_data = data.split(",")
  truncated_data = split_data[0][0:8] + "," + split_data[1] + "," + split_data[2]
  return truncated_data

# Handles the simple CLI ui
def handle_ui():
  response = ""
  while 1:
    clear_console()
    print_file("fun.dat")
    print("1: Add data to the file.")
    print("2: Update existing data within file.")
    print("9: Exit.")

    response = input()

    match response:
      case "1":
        while 1:
          clear_console()
          print("data format: (Color, Zipcode (00000-99999), State Abbreviation)")
          print("9: Exit.")
          response = input("")
          if response == "9":
            exit()
          elif check_data_format(response):
            add_to_file(FILE, truncate_data(pad_data(response)))
            break
          else:
            print("Invalid format! Please try again.")
            time.sleep(1.5)

      case "2":
        print("2")

      case "9":
        exit()
      
# Entry point for the script 
if __name__ == "__main__":
  main()