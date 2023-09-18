#comment here
import sys
import PyPDF2
import re

class Transaction:
    def __init__(self, date_of_transaction, place, key_character_patterns, amount):
        self.date_of_transaction = date_of_transaction
        self.place = place
        self.key_character_patterns = key_character_patterns
        self.amount = amount

    def __str__(self):
        return f"Date: {self.date_of_transaction}, Place: {self.place}, Patterns: {self.key_character_patterns}, Amount: {self.amount}"

def pdf_to_text(pdf_file_path, txt_file_path):
    pdf_file_path = "081523 WellsFargo.pdf"
    txt_file_path= "test_data.txt"
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
        else:
            break
        index += 1

    # Assign "Place" object to "Costco"
    place = ""
    amount = float(parts_of_transaction_string[len(parts_of_transaction_string)-1]) #last element is the amount for the transaction
    # Create and return a Transaction object
    return Transaction(date_of_transaction, place, key_character_patterns, amount)

def createTransactionObjects(listOfTransactionStrings):
    transactionObjectList = []
    for i in listOfTransactionStrings:
        transactionObjectList.append(create_transaction_from_string(i))
    print("------------------printing objects------------------\n")
    for i in transactionObjectList:
        print(i)
    #mapCharacterPatternsToPlace(transactionObjectList)
        
    return 0
#reads in content from the file_path which is a .txt file, looks for from_string
#after from_string is found lines from .txt file each subsequent line is appended to 
#charges list until the to_string is found 
#function returns the charges list generated
def readAndCreateListOfTransactions(file_path, from_string, to_string):
    addSubsequentLinesToTransactions= False
    # Open the file for reading (default mode is 'r')
    transactions = []
    print("fie_path ", file_path, "from_string ", from_string, "to_string ", to_string)
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
    createTransactionObjects(transactions)
    return transactions

def main():
    # Specify the paths for your PDF and the desired text file
    pdf_file_path = "081523 WellsFargo.pdf"
    txt_file_path = "test_data.txt"

    # Call the function to convert the PDF to text
    print("What pdf file would you like to convert to .txt file?")

    pdf_file_name = input("Enter the path of the .pdf file you would like to read from")
    txt_file_name = input("Enter the name of the .txt file you would like to create")
    
    pdf_to_text(pdf_file_path, txt_file_path)

    from_string = "Purchases, Balance Transfers & Other Charges"
    to_string = "TOTAL PURCHASES, BALANCE TRANSFERS & OTHER CHARGES FOR THIS PERIOD"
    from_string= from_string.lower()
    to_string = to_string.lower()
    
    readAndCreateListOfTransactions(txt_file_path, from_string, to_string )

    #print(charges)
if __name__ == "__main__":
    main()
