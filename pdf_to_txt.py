import PyPDF2

def pdf_to_text(pdf_file_path, txt_file_path):

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