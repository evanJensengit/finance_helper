#comment here
import sys
import pdf_to_txt
import transaction_creator
testing = True


def calculateTransactionsAtPlaces(transactions):
    for i in transactions:
        transaction_creator.transactionsAtPlaces[i.place] += i.amount
        transaction_creator.transactionsAtPlaces[i.place] = round(transaction_creator.transactionsAtPlaces[i.place],2)
    periodOfTransactions = transactions[0].date_of_transaction + " " + transactions[len(transactions)-1].date_of_transaction
    return periodOfTransactions

#write data to spending.txt
def writeTransactionsAtPlacesToFile(file_path, totalSum, periodOfTransactions):
    # Open the file in write mode
    try:
        with open(file_path, 'w') as file:
            file.write( periodOfTransactions+ "\n")
            # Write the contents of the list to the file
            for key,val in transaction_creator.transactionsAtPlaces.items():
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
    pdf_file_path = input("Enter the path of the .pdf file you would like to read from")
    txt_file_path = input("Enter the name of the .txt file you would like to create")

    # Call the function to convert the PDF to text
    if testing:
        pdf_file_path = "/Users/evanjensen/Documents/sideProjects/finance_helper/banking_statements/101523 WellsFargo.pdf"
        txt_file_path = "Spending.txt"
    
    # Call the function pdf_to_text to convert the PDF to text
    pdf_to_txt.pdf_to_text(pdf_file_path, txt_file_path)

    from_string = "Purchases, Balance Transfers & Other Charges"
    to_string = "TOTAL PURCHASES, BALANCE TRANSFERS & OTHER CHARGES FOR THIS PERIOD"
    from_string= from_string.lower()
    to_string = to_string.lower()

    edits = input("edit text file if you want")

    transactions = transaction_creator.readAndCreateListOfTransactions(txt_file_path, from_string, to_string )
    periodOfTransactions = calculateTransactionsAtPlaces(transactions)
    totalSum = 0
    for key,value in transaction_creator.transactionsAtPlaces.items():
        print(key,":",value)
        totalSum += value
    totalSum = round(totalSum,2)  

    writeTransactionsAtPlacesToFile(txt_file_path, totalSum, periodOfTransactions)
    
    #print(charges)
if __name__ == "__main__":
    main()
