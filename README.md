# Finance Helper CLI
## Purpose
I was using online finance trackers on my phone to check how much I was spending and the finance tracker was not reading in data correctly to different categories. The third party finance trackers also had a error readings in the values from my checking account. I have been using a excel sheet up to this point to manually batch each expense into a general category such as "Clothes", "Amazon", "Grocery", "Gym" etc.       

Each month this process of looking through my credit statement and adding up the expenses into 
different categories took about ** 1.5 hours** each month. 

I created this CLI to streamline this process for myself and others. At this point, this is just a CLI that uses RAM and 
text files to store and manipulate data.   

I look forward to linking the backend to a database for persistent storage and
implementing a front end to make the creation of expense categories easier to create and update. 

## Functionality
The Finance Helper program reads in a banking statement PDF file and creates a "Spending.txt" file that shows what places 
you are spending money at from greatest amount to least amount

## Getting started 
### Mac
Make sure python3 is installed  
Install pip and run `pip install PyPDF2`  

## Using Finance Helper CLI
Navigate to directory finance_helper is in and run `python3 main.py`   
Enter in the path to the pdf file of banking statment on local file storage device
Enter the path for the Spending.txt file to be created from the pdf file

The program will pause to allow user to make any adjustments to the text file generated from the pdf file 
