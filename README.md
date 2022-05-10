# Clover 🍀
Clover is an application that utilizes banking data that the user inputs (.csv, .xls, clipboard), graphs the data, creates an interactive budget, analyzes the spending, and makes saving suggestions for future purchases.<br><br>
# Video Demonstration
<a href="{video-url}" title="Clover Video"><img src="{https://github.com/ph1-618O/clover/blob/main/images/%20clover_vid.png}" alt="Clover Video" width="400"/></a>
# Table Examples

 |   |   |   |   |
|---|---|---|---|
 | **Sunburst**        | **Treemap**         | **Table**   | **BarGraph** |
 |    <img src="https://github.com/ph1-618O/clover/blob/main/notebooks/sunburst.svg" alt="Sunburst" width="250"/>   |<img src="https://raw.githubusercontent.com/ph1-618O/clover/f0333334e149884116ec302aca78353de6c21394/notebooks/fig4.svg" alt="TreeMap" width="250"/>|   <img src="https://raw.githubusercontent.com/ph1-618O/clover/0eda1a103df41657d5cedc2c45903670b4992ff5/notebooks/table_blue.svg" alt="Tables" width="300"/>| <img src="https://raw.githubusercontent.com/ph1-618O/clover/bd7f89d8a958eb0df11997e866e57e2e8bfb78d1/notebooks/bar.svg" alt="Bar Graph" width="250"/> || 
 |||||| 


# User Instructions
- Open terminal, or anaconda prompt
- Navigate to the folder location of format_data.py and budget.py
  - If using format_data go to Banking Website with tabluar data. Highlight the column names and rows hit either ```Ctrl-C``` (on PC), or ```CMD-C``` to copy the rows onto the clipboard.
  - once complete follow the instructions below at the Activating Cliboard Functionality to change the functionality of Format_data.py 
  - Return to terminal or anaconda prompt. 
  - To execute program just to format the data type in
  ```python format_data.py```
  - To both format and cateogorize data type:
  ```python budget.py``` 

# Program Function

- Upon inception this program needed data, in a format that a program could categorize into a database based on a unique identifier. There are many options for inputs that Python will accept, excel files, CSVs, TSVs, and some programs are even able to convert PDFs of table data into DataFrames. For the sake of time Pandas function read_clipboard was used to bring in sample data from a banking website. Once successful a sample csv dataset was created to emulate real data and later passed/ imported to format_data.py for formatting. 

## Format_data.py
- This program works with the imported clip_board data. It allows for the renaming of the columns, formatting of an amount type column from string to float, and organizing the by a chosen column. IE arranging the data by date ascending.

### Activating Clipboard Functionality
- In order to activate the functionality of the read_clip() function. Open a text editor of the file Format_data.py located line 183 and type in read_clip(). Save the file and exit the text editor. Follow the instructions above to run the program using python. Then when the prompt asks for the name of the CSV that was exported enter the name you gave the CSV that you saved.

- Later functionality will include 
  - input queries to know if the user wants to sort the data by ascending or descending.
  - formatting for TSV's
  - Allowing for user to keep all the columns imported and when added to DB it compares new column names and adds NaNs to Dataframe if not matching.
  
## Budget.py
- Create budget dict. py takes data, compares it to a database, or creates a database and parses the data with user guided input. 

1. First the user inputs a given a CSV, Excel file or Cliboard Data.
2. It next asks the user what are the necessary columns for their budget and allows for column renaming and removing.
3. The transaction column is auto selected or if not apparent to program is selected by user input.
4. Attempting to find the distinct identifier the program splits and iterates through the transaction column, removing stopwords, two letter ids, numbers and address/city/state. Utilized NLP, and Google Maps API. 
5. If unsuccessful it queries the user to know which part of data is the identifier.
6. Then sorting of the transaction data by distinct identifier occurs within the data. Such as: Food purchases, Home purchases added as category and passes to a dictionary.
7. The program then searches the entire imported dataset for similar identifiers and attaches the category and adding them to a dictionary as well.
8. Once the entire data set is marked with category and identifier it passes the dictionary to pandas.
9. Pandas creates a dataframe for output, it then queries the user if they'd like to save it as a CSV or add to a Database using MongoDB.
10. Upon repeated uses of the program, once the new data is imported by the user, the app queries the database, and identifies the matching categories and ids.
11. If any data is new and unitentifiable it queries the user for the correct category and identifier.


For example one line of data may be:: 
```"05/17/2021	05/16/2021 WHOLE FOODS #893 ARLINGTON VA	1528	-$200.61	$10,488.61"```
- Budget.py pulls out each column chosen by the user. 
```Date_Posted, Date_Pending, Transaction, Account, Amount, Balance```
- User identifies the Transaction column 
- ```"WHOLE FOODS #893 ARLINGTON VA"```
- Program uses ```"WHOLE"``` as identifier.
- User chooses ```"GROCERIES"```, a category out of the defaults or adds their own. 
- This occurs repeatedly until the dataset is complete.

- Later functionality will include
  - exporting the dictionary into a DataFrame with a column identifier // Completed
  - using Google Maps API to remove the city and state as stopwords, or add as their own columns // Working
  - adding Machine Learning to use sample set with the data and the column identifier to predict categories
  - exporting the created dictionary or DataFrame to mongolDB database // Working
  - a program to interact with the user to determine Budget Percentages, and offer defaults
  - a graphing program to analyze the data into chosen budget percentages
  - a recommendation based on previous data to better meet budget goals
  - the ability for this program to interact with Linux, PC and MacOS, and install dependencies with pip if they are not already installed

