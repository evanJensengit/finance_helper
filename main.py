#comment here
import sys
import PyPDF2

def pdf_to_text(pdf_file_path, txt_file_path):
    pdf_file_path = "/Users/evanjensen/Documents/sideProjects/finance_helper/081523 WellsFargo.pdf"
    txt_file_path= "/Users/evanjensen/Documents/sideProjects/finance_helper/test_data.txt"
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

def readAndOpenFile(file_path):
    # Specify the file path
    file_path = "example.txt"

    # Open the file for reading (default mode is 'r')
    try:
        with open(file_path, 'r') as file:
            # Loop through each line in the file
            for line in file:
                # Process each line as needed
                print(line.strip())  # .strip() removes the newline character
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    # Specify the paths for your PDF and the desired text file
    pdf_file_path = "081523 WellsFargo.pdf"
    txt_file_path = "test_data.txt"

    # Call the function to convert the PDF to text
    print("What pdf file would you like to convert to .txt file?")

    pdf_file_name = input("Enter the path of the .pdf file you would like to read from")
    txt_file_name = input("Enter the name of the .txt file you would like to create")
    
    pdf_to_text(pdf_file_path, txt_file_path)

    fromString = "Purchases, Balance Transfers & Other Charges"
    toString = "TOTAL PURCHASES, BALANCE TRANSFERS & OTHER CHARGES FOR THIS PERIOD"

    #readAndOpenFile(txt_file_path)
       
if __name__ == "__main__":
    main()
