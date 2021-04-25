# clover
Clover is an application that utilizes banking data that the user inputs (most often in the form of an excel file) and creates an interactive budget, analyzes the spending, and makes saving suggestions for future purchases.

# User Instructions
- Open terminal, or anaconda prompt
- Navigate to the folder location of format_data.py or create_budget_dict
  - If using format_data go to Banking Website with tabluar data. Highlight the column names and rows hit either Ctrl-C (on PC), or Cmd-C to copy the rows onto the clipboard.
  - once complete follow the instructions below at the **** symbols to change the functionality of Format_data.py 
  - Return to terminal or anaconda prompt. 
  - Type in python Format_data.py // program will execute
  - Type in python create_budget_dict.py // program will execute

# Program Function

- Upon inception this program needed data, in a format that a program could categorize into a database based on a unique identifier. There are many options for inputs that Python will accept, excel files, CSVs, TSVs, and some programs are even able to convert PDFs of table data into DataFrames. For the sake of time Pandas function read_clipboard was used to bring in sample data from a banking website. Once successful a sample csv dataset was created to emulate real data and later passed/ imported to Create_budget.py for formatting. 

## Format_data.py
- This program works with the imported clip_board data. It allows for the renaming of the columns, formatting of an amount type column from string to float, and organizing the by a chosen column. IE arranging the data by date ascending.
- Currently the read_clip() function is disabled and it imports an already saved example of clipboard data from a CSV.

*****
- In order to activate the functionality of the read_clip() function. Open a text editor of the file Format_data.py located line 183 and type in read_clip(). Save the file and exit the text editor. Follow the instructions above to run the program using python. Then when the prompt asks for the name of the CSV that was exported enter the name you gave the CSV that you saved.

- Later functionality will include 
  - input queries to know if the user wants to sort the data by ascending or descending.
  - formatting for TSV's, and excel files
## Create_budget_dict.py

Create budget dict. py takes a given CSV and sorts the data from the CSV
into a dictionary with a budget category as the key
it also asks the user what are the necessary columns for their budget
once the program begins it passes a unique identifier to each row entry
this unique identifier is also stored at the end of the dictionary of lists
so that once it is within the dictionary the program will recognize
all future occurences of identifier and add it without input. 

- Later functionality will include
  - exporting the dictionary into a DataFrame with a column identifier 
  - adding Machine Learning to use sample set with the data and the column identifier to predict categories
  - exporting the created dictionary or DataFrame to mongolDB database
  - a program to interact with the user to determine Budget Percentages, and offer defaults
  - a graphing program to analyze the data into chosen budget percentages
  - a recommendation based on previous data to better meet budget goals
  - the ability for this program to interact with Linux, PC and MacOS, and install dependencies with pip if they are not already installed

