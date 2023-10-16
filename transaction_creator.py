import re
import transaction_creator
# Define a dictionary to map patterns to places
placesCorrelatedWithPatterns = {}

# Initialize a dictionary to store transactions at places
transactionsAtPlaces = {"amazon": 0, "clothes": 0, "gas": 0, "cats": 0, "costco": 0, "grocery": 0, "internet": 0, "ups": 0, 
"usps": 0, "utilities": 0, "apple": 0, "entertainment": 0, "food_delivery": 0, "target": 0, "office_supplies": 0, 
"gym": 0,  "eating_out": 0, "other": 0, "allstate": 0}

# Define a Transaction class to represent individual transactions
class Transaction:
    def __init__(self, date_of_transaction, place, key_character_patterns, amount):
        self.date_of_transaction = date_of_transaction
        self.place = place
        self.key_character_patterns = key_character_patterns
        self.amount = amount

    def __str__(self):
        return f"Date: {self.date_of_transaction}, Place: {self.place}, Patterns: {self.key_character_patterns}, Amount: {self.amount}"

#reads in content from the file_path which is a .txt file, looks for from_string
#after from_string is found lines from .txt file each subsequent line is appended to 
#charges list until the to_string is found 
#function returns the charges list generated
def readAndCreateListOfTransactions(file_path, from_string, to_string):
    addSubsequentLinesToTransactions= False
    # Open the file for reading (default mode is 'r')
    transactions = []

    try:
        with open(file_path, 'r') as file:
            # Loop through each line in the file
            for line in file:
                lower_case_line = line.strip().lower()
                #end of transactions 
                if to_string in lower_case_line:
                    break
                #add transaction to transactions list
                if addSubsequentLinesToTransactions:
                    transactions.append(lower_case_line)
                #beginning of transactions 
                if from_string in lower_case_line:
                    addSubsequentLinesToTransactions = True
                    continue
                
                # Process each line as needed
                #print(line.strip())  # .strip() removes the newline character
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    #build the placesCo
    transactions = createTransactionObjects(transactions)
    for i in transactions:
        print(i)
    return transactions

def generatePlacesWithPatternsDict():
    # Read the content from the .txt file
    with open('placesWithPatterns.txt', 'r') as file:
        lines = file.readlines()

    # Iterate through the lines and split into key and value
    for line in lines:
        # Remove leading and trailing whitespaces
        line = line.strip()
        # Split the line into key and value using ":"
        key_value_pairs = line.split(",")

        # Iterate through the key-value pairs and add them to the dictionary
        for pair in key_value_pairs:
            if ":" in pair:
                # Split each pair into key and value using ":"
                key, value = pair.split(":")
                # Remove double quotes and leading/trailing spaces from key and value
                key = key.strip(' "')
                value = value.strip(' "')
                # Add the key-value pair to the dictionary
                placesCorrelatedWithPatterns[key] = value

def generateTransactionsAtPlaces():
    #read in each key with
    # Read the content from the .txt file
    with open('transactions_at_places.txt', 'r') as file:
        lines = file.readlines()

    # Iterate through the lines and split into key and value
    for line in lines:
        # Remove leading and trailing whitespaces
        line = line.strip()
        # Split the line into key and value using ":"
        key_value_pairs = line.split(",")

        # Iterate through the key-value pairs and add them to the dictionary
        for pair in key_value_pairs:
             if ":" in pair:
                # Split each pair into key and value using ":"
                key, value = pair.split(":")
                # Remove double quotes and leading/trailing spaces from key
                key = key.strip(' "')
                value = int(value)
                # Add the key-value pair to the dictionary
                transactionsAtPlaces[key] = value

#create Transaction objects from string
def createTransactionObjects(listOfTransactionStrings):
    transactionObjectList = []
    for i in listOfTransactionStrings:
        transactionObjectList.append(create_transaction_from_string(i))
    generatePlacesWithPatternsDict()    
    transactionsWithPlace  = mapCharacterPatternsToPlace(transactionObjectList)

    return transactionsWithPlace

def create_transaction_from_string(transaction_string):
    # Split the input string into parts using space as a delimiter
    parts_of_transaction_string = transaction_string.split()

    # Find the first occurrence of date (transaction date) and parse it into a date object
    pattern = r'\d{2}/\d{2}'
    
    # Use re.findall to find all matches
    matches = re.findall(pattern, parts_of_transaction_string[1])
    if len(matches) >= 2:
        date_of_transaction = matches[0] #get first date

    key_character_patterns = []
    # Add strings before the cost associated to the list of key_character_patterns
    index = 3
    while index < len(parts_of_transaction_string):
        if parts_of_transaction_string[index][0].isalpha():
           key_character_patterns.append(parts_of_transaction_string[index])
        index += 1

    # Assign "Place" object to "Costco"
    place = ""
    amount = float(parts_of_transaction_string[len(parts_of_transaction_string)-1]) #last element is the amount for the transaction
    # Create and return a Transaction object
    return Transaction(date_of_transaction, place, key_character_patterns, amount)

#map the patterns found in statement to places correlated with patterns data structure
def mapCharacterPatternsToPlace(transactions):
    for i in range(len(transactions)):
        patterns = transactions[i].key_character_patterns
        found_match = False
        for pattern in patterns:
            if placesCorrelatedWithPatterns.get(pattern):
                transactions[i].place = placesCorrelatedWithPatterns[pattern]
                found_match = True
                break
        
        if not found_match:
            transactions[i].place = "other"

    return transactions 



