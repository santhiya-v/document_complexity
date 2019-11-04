# Document Complexity

This module aims in finding complexity score of a document. Complexity score, here means how difficult it is to comprehend the text. Based on the score, grade levels are assigned. 

## Score and Grade Level Information

| Score        | Grade Level    |
| ------------- |:-------------:| 
| 0 | Kids (4th grade and lower) | 
| 1 | 7th to 5th grade      |  
| 2 | 10th to 8th grade     |
| 3 | High School Student     |  
| 4 | College Student    |  
| 5 | College Graduate and higher    |  

## Demo Web App
[Click here](https://text-complexity.herokuapp.com)

## Installation

1. Clone or download the repository.
2. Create a new virtual environment and activate it.
```
 virtualenv -p python3 document_complexity
 source document_complexity/bin/activate
 ```

3. Navigate to project root folder and run ``` pip install -r requirements.txt```
4. Run ``` python setEnv.py ``` to download necessary files for the application.

## Run as web application
1. Navigate to project root folder and run the following commands:
```
FLASK_APP=app.py
flask run
```

## Run as console application

1. Navigate to project root folder and run the following command : 
```
python main.py --inputDoc {path/to/txtfile}
```
2. To validate document using particular metric ( Flesch Reading Ease, Gunning fog Index , Automated Readability Index), using the following command :
```
python main.py --inputDoc {path/to/txtfile} --metric {flesch|gfog|ari}
```


