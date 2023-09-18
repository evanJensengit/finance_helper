#comment here
import sys
import PyPDF2
import re

testing = True
placesCorrelatedWithPatterns = {
    "amzn":"amazon", "amzn.com/bill":"amazon", "amazon.com":"amazon","audible":"amazon",
    "allstate": "allstate",
    "circle":"gas", "shell":"gas", "gas":"gas", "oil":"gas",
    "veterinary":"cats",
    "costco": "costco",
    "yokes":"grocery","safeway":"grocery", "yoke's":"grocery","fresh":"grocery", "qfc":"grocery",
    "spectrum":"internet", "verizon":"internet", "ziply":"internet",
    "usps": "usps", "ups":"ups",
    "city":"utilities",
    "pp*apple.com/bill":"apple",
    "amc":"entertainment", "spotify":"entertainment",
    "doordash":"food_delivery",
    "target":"target",
    "reebok":"clothes", "uniqlo":"clothes",
    "office":"office_supplies",
    "planet":"gym", "fitness":"gym", "golds":"gym",
    "chipotle":"eating_out", "dining":"eating_out", "mod":"eating_out",
    "other":"other"
    }
transactionsAtPlaces = { "amazon": 0, "clothes": 0, "gas": 0, "cats": 0, "costco": 0, "grocery": 0, "internet": 0, "ups": 0, 
                        "usps": 0, "utilities": 0, "apple": 0, "entertainment": 0, "food_delivery": 0, "target": 0, "office_supplies": 0, 
                        "gym": 0,  "eating_out": 0, "other": 0, "allstate": 0, }

class Transaction:
    def __init__(self, date_of_transaction, place, key_character_patterns, amount):
        self.date_of_transaction = date_of_transaction
        self.place = place
        self.key_character_patterns = key_character_patterns
        self.amount = amount

    def __str__(self):
        return f"Date: {self.date_of_transaction}, Place: {self.place}, Patterns: {self.key_character_patterns}, Amount: {self.amount}"

def pdf_to_text(pdf_file_path, txt_file_path):
    if testing:
        pdf_file_path = "081523 WellsFargo.pdf"
        txt_file_path= "Spending.txt"
    try:
        # Open the PDF file
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Initialize an empty text string
            text = ""
            
            # Loop through each page and extract text
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            
            # Save the extracted text to a text file
            #creates new text file if text file doesnt exist
            #overwrites content in text file if text file does exist
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
        
        print(f"Text extracted from '{pdf_file_path}' and saved to '{txt_file_path}'.")
    
    except FileNotFoundError:
        print(f"The file '{pdf_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

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

#create Transaction objects from string
def createTransactionObjects(listOfTransactionStrings):
    transactionObjectList = []
    for i in listOfTransactionStrings:
        transactionObjectList.append(create_transaction_from_string(i))

    for i in transactionObjectList:
        print(i)
    transactionsWithPlace  = mapCharacterPatternsToPlace(transactionObjectList)

    return transactionsWithPlace
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
                #add charge to charges list
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
    transactions = createTransactionObjects(transactions)
    for i in transactions:
        print(i)
    return transactions

def calculateTransactionsAtPlaces(transactions):

    for i in transactions:
        transactionsAtPlaces[i.place] += i.amount
        transactionsAtPlaces[i.place] = round(transactionsAtPlaces[i.place],2)

#write data to spending.txt
def writeTransactionsAtPlacesToFile(file_path, totalSum):
    # Open the file in write mode
    try:
        with open(file_path, 'w') as file:
            item = "Total Sum: " + str(totalSum)
            file.write( item+ "\n")
            # Write the contents of the list to the file
            for key,val in transactionsAtPlaces.items():
                item = str(key) + " " + str(val)
                file.write( item+ "\n")  # Add a newline character to separate items
            file.write("\n")
            item = "Total Sum: " + str(totalSum) + "\n"
            file.write(item + "\n")

        print(f"Data written to '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Specify the paths for your PDF and the desired text file
  

    # Call the function to convert the PDF to text

    pdf_file_path = input("Enter the path of the .pdf file you would like to read from")
    txt_file_path = input("Enter the name of the .txt file you would like to create")
    if testing:
        pdf_file_path = "081523 WellsFargo.pdf"
        txt_file_path = "Spending.txt"
    pdf_to_text(pdf_file_path, txt_file_path)

    from_string = "Purchases, Balance Transfers & Other Charges"
    to_string = "TOTAL PURCHASES, BALANCE TRANSFERS & OTHER CHARGES FOR THIS PERIOD"
    from_string= from_string.lower()
    to_string = to_string.lower()
    
    transactions = readAndCreateListOfTransactions(txt_file_path, from_string, to_string )
    calculateTransactionsAtPlaces(transactions)
    totalSum = 0
    for key,value in transactionsAtPlaces.items():
        print(key,":",value)
        totalSum += value
    totalSum = round(totalSum,2)  

    writeTransactionsAtPlacesToFile(txt_file_path, totalSum)
    
    #print(charges)
if __name__ == "__main__":
    main()
