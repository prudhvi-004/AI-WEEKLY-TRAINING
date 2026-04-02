import pandas as pd

#Pandas --> It is a python library used for dta manipulation and analysis.
#it is used to create dataframes and series which are used to store and manipulate data in a tabular format.
#It provides a wide range of functions for data cleaning, transformation, and analysis.

#to create a pandas series
data = [1, 2, 3, 4, 5]
series = pd.Series(data)
print(series)  # it will print the series in pandas format

#to create a pandas dataframe
data = {'Name': ['Prudhvi', 'Harsha', 'Sai'],
        'Age': [25, 30, 35],
        'City': ['Hyderabad', 'Bangalore', 'Chennai']}
df = pd.DataFrame(data)
print(df)  # it will print the dataframe in pandas format

#to access a column in a dataframe
print(df['Name'])  # it will print the 'Name' column of the dataframe
print(df['Age'])  # it will print the 'Age' column of the dataframe
print(df['City'])  # it will print the 'City' column of the dataframe

#to access a row in a dataframe
print(df.loc[0])  # it will print the first row of the dataframe
print(df.loc[1])  # it will print the second row of the dataframe

#to know the use of iloc 
print(df.iloc[0])  # it will print the first row of the dataframe
print(df.iloc[1])  # it will print the second row of the dataframe

#difference between loc and iloc
#loc is used to access the rows and columns by labels or boolean arrays.
#iloc is used to access the rows and columns by integer position.


#to know tha shape of the dataframe
print(df.shape)

#to print first 5 rows of the dataframe
print(df.head())
#to print last 5 rows of the dataframe
print(df.tail())

#to print first 2 rows of the dataframe
print(df.head(2))

#loading data from a csv or excel or json file
#to load data from a csv file
#--->df = pd.read_csv('file.csv')
#to load data from an excel file
#--->df = pd.read_excel('file.xlsx')
#to load data from a json file
#--->df = pd.read_json('file.json')

#info()
#to get the information about the dataframe
print("INFO:",df.info())

#describe()
#to get the statistical summary of the dataframe
print("DESCRIBE:",df.describe())

#to drop a column from the dataframe
df = df.drop('City', axis=1) 
#to drop multiple columns from the dataframe
#--->df = df.drop(columns = ['City', 'Age'], axis=1)

#to drop a row from the dataframe
df = df.drop(0, axis=0)
#to drop multiple rows from the dataframe   
#--->df = df.drop(index = [0, 1], axis=0)

#to fill the missing values in the dataframe.
df = df.fillna(5)  # it will fill the missing values with the specified value

#to drop the missing values in the dataframe
df = df.dropna()  # it will drop the rows with missing values

#to replace the values in the dataframe
df = df.replace(30, 31)  # it will replace the value 30 with 31 in the dataframe

print(df)  

#to save the dataframe to a csv file
#--->df.to_csv('file.csv', index=False)

#to save the dataframe to an excel file
#--->df.to_excel('file.xlsx', index=False)  

#to save the dataframe to a json file
#--->df.to_json('file.json', orient='records') 
#orient='records' will save the dataframe in a list of dictionaries format in json file.

#to know the unique values in a column of the dataframe
print(df['Age'].unique())

#value_count()
#to count the number of occurrences of each unique value in a column of the dataframe
print(df['Age'].value_counts())

#to know the mean, median, mode of a column in the dataframe
print("Mean:",df['Age'].mean()) 
print("Median:",df['Age'].median())
print("Mode:",df['Age'].mode())


