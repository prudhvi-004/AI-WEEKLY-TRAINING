#------------------------------------NUMPY--------------------------------
#Numpy --> it is a python library used to perform mathematical operations on large multi-dimensional arrays and matrices.
# Numpy is a powerful library that provides a wide range of functions for working with arrays, including mathematical operations, statistical analysis, and linear algebra. It is widely used in scientific computing, data analysis, and machine learning.

import numpy as np

array = [1,2,3,4,5]
print(type(array))   # it is list dtype in python

numpy_array = np.array(array)
print(type(numpy_array)) #here it is numpy.ndarray dtype in python
 
#to create a numpy array 
array = np.array([1,2,3,4,5])
print(array)  # it will print the array in numpy format

#to create a 2D numpy array
array_2d = np.array([[1,2,3],[4,5,6]])
print("Array:\n",array_2d)  # it will print the 2D array in numpy format
print("Shape:",array_2d.shape)  # it will print the shape of the array (2,3) means 2 rows and 3 columns
print("Dim:",array_2d.ndim)  # it will print the number of dimensions of the array (2 in this case)
print("Size:",array_2d.size)  # it will print the total number of elements in the array (6 in this case)


#Accessing elements in a numpy array
arr = np.array([[-1, 2, 0, 4],
                [4, -0.5, 6, 0],
                [2.6, 0, 7, 8],
                [3, -7, 4, 2.0]])

arr2 = arr[:2, ::2]
print ("first 2 rows and alternate columns(0 and 2):\n", arr2)
 

#basic operations on numpy arrays 
a = np.array([[1, 2],[3, 4]])
 
b = np.array([[4, 3],[2, 1]])
               
print ("Adding 1 to every element:", a + 1)
print ("\nSubtracting 2 from each element:", b - 2)
print ("\nSum of all array elements: ", a.sum())
print ("\nArray sum:\n", a + b)

#Math Operations on ARRAY
arr1 = np.array([[4, 7], [2, 6]], dtype = np.int32)

arr2 = np.array([[3, 6], [2, 8]], dtype = np.int32) 
 
Sum = np.add(arr1, arr2)
print("SUM:", Sum)

Sum1 = np.sum(arr1)
print("Sum of arr1:", Sum1)
 
Sqrt = np.sqrt(arr1)
print("Square root of arr1:", Sqrt)

Trans_arr = arr1.T
print("Transpose of arr1:", Trans_arr)

#to know the unique elements in an array
arr = np.array([1, 2, 3, 4, 5, 1, 2, 3])
unique_elements = np.unique(arr)    
print("Unique elements in the array:", unique_elements)

#to know the mean of an array
arr = np.array([1, 2, 3, 4, 5])
mean = np.mean(arr)
print("Mean of the array:", mean)

#to know the median of an array
arr = np.array([1, 2, 3, 4, 5]) 
median = np.median(arr)
print("Median of the array:", median)

#to know the standard deviation of an array
arr = np.array([1, 2, 3, 4, 5])
std_dev = np.std(arr)
print("Standard deviation of the array:", std_dev)

