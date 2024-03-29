#!/usr/bin/env python
# coding: utf-8


# In[2]:


import pandas as pd


# In[3]:


#Read the given credit_data csv file, drop duplicates and missing values
df = pd.read_csv('credit_data.csv', index_col=0).drop_duplicates().dropna()


# In[4]:


df


# In[5]:


#Changing the BAD column name to 'LOAN' and assigning 0 to 'REPAID' and 1 to 'DEFAULT' (Human Readable values)

BAD = {0: 'REPAID',1: 'DEFAULT'}

df.BAD = [BAD[item] for item in df.BAD]

df= df.rename(columns = {'BAD': 'LOAN'}, inplace = False)


# In[6]:


df


# In[7]:


#Independent data
x = df[['DEBTINC', 'DELINQ', 'DEROG', 'VALUE', 'CLAGE']]
#Dependent Data
y = df['LOAN']


# In[8]:


#Split the data into training data and testing data
from sklearn.model_selection import train_test_split


# In[9]:


x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)


# In[10]:


x_train


# In[11]:


#Importing decision tree classifier 
from sklearn.tree import DecisionTreeClassifier


# In[12]:


#Importing decision tree regressor
from sklearn.tree import DecisionTreeRegressor


# In[13]:


#Create decision tree function
dt_model = DecisionTreeClassifier()


# In[14]:


#Fitting the model
dt_model.fit(x_train, y_train)


# In[15]:


#Check the training score
dt_model.score(x_train, y_train)


# In[16]:


#Check the test score
dt_model.score(x_test, y_test)


# In[17]:


#Predictions on test score
dt_model.predict(x_test)


# In[18]:


#Changing the max_depth to combat overfitting of the model


# In[19]:


#Loop through max_depths of 1-10 to find the most optimal solution
train_accuracy = []
test_accuracy = []
for depth in range(1,10):
    dt_model = DecisionTreeClassifier(max_depth=depth, random_state=10)
    dt_model.fit(x_train, y_train)
    train_accuracy.append(dt_model.score(x_train,y_train))
    test_accuracy.append(dt_model.score(x_test, y_test))


# In[20]:


frame = pd.DataFrame({'max_depth': range(1,10), 'train_acc': train_accuracy, 'test_acc': test_accuracy})
frame.head(11)


# In[21]:


import matplotlib.pyplot as plt


# In[24]:


#Visualize max_depth performance
plt.figure(figsize=(12,6))
plt.plot(frame['max_depth'], frame['train_acc'], marker='o')
plt.plot(frame['max_depth'], frame['test_acc'], marker='o')
plt.xlabel('Depth of Tree')
plt.ylabel('Performance')
plt.legend()


# In[25]:


#Create a new decision tree function with our optimal max_depth of 8
dt_model = DecisionTreeClassifier(max_depth=8, random_state=10)


# In[27]:


#Fit the new model
dt_model.fit(x_train, y_train)


# In[28]:


#Training Score
dt_model.score(x_train, y_train)


# In[29]:


#Test Score
dt_model.score(x_test, y_test)


# In[30]:


from sklearn import tree


# In[31]:


get_ipython().system('pip install graphviz')


# In[44]:


#Plotting/creating the decision tree visual
decision_tree = tree.export_graphviz(dt_model,out_file='tree.dot',feature_names=x_train.columns,max_depth=3,filled=True)


# In[45]:


get_ipython().system('dot -Tpng tree.dot -o tree.png')


# In[46]:


#Printing our decision tree (with a max_depth of 3 for space issues)
image = plt.imread('tree.png')
plt.figure(figsize=(15,15))
plt.imshow(image)


# # Project Report
# 

# I began the analysis by importing pandas to perform data manipulation. By using the pandas library, I imported the 'credit_data.csv' file into Jupyter Lab. I was able to accomplish this by using the .read_csv function.
# 
# My first task for this project was to remove duplicates and drop any rows that were missing values. To accomplish this, I implemented the .drop_duplicates() and dropna() functions. This narrowed the number of rows down to 619, as opposed to the original 624.
# 
# To finish preparing the data, I needed to convert "BAD" from ordinal values to categorical values. To do so, I created a dictionary containing the keys 0 and 1, and the respective values of "REPAID" and "DEFAULT". To apply this to the data frame, I made a for loop that looped through each item in the column "BAD" and applied the correct dictionary value to each entry. Lastly, I renamed the "BAD" column to "LOAN" so the column would read as the status of their last loan (either repaid or defaulted). This process was done to enhance the comprehension of data for humans reading the results.
# 
# Following the data preparation phase, I then began to split the data into training and testing data. To do so, I created my x values and y values as follows:
#
# x = df[['DEBTINC', 'DELINQ', 'DEROG', 'VALUE', 'CLAGE']]
# y = df['LOAN']
# 
# After splitting the data into training and testing data, I imported DecisionTreeClassifier and DecisionTreeRegressor from sklearn.tree to build my model. After creating the DecisionTreeClassifier function, I fit the model, checked both the training scores and the test scores, and then created predictions based on the test score. I learned how to tune my decision tree and make it more accurate by changing the max_depth parameter (the length of the tree's longest path). I needed to make sure that my max_depth value was not too low (underfitting), but not too high (overfitting).
# 
# I noticed that my model's training score was 1.0, indicating that my prediction model might be prone to overfitting. To make my decision tree more accurate, I looped through the max_depths from 1 to 10 to find the most optimal solution. I visualized the results where the yellow line represents the test_acc (test accuracy) and the blue line indicates the train_acc (training accuracy). I observed that the test accuracy declined after the 8th iteration and eventually became a straight horizontal line, whereas the training accuracy eventually approached 1.0. Therefore, I concluded that a max_depth past 8 was where my training model may begin to overfit the data. Thus, I created a new decision tree function that sets the max_depth parameter to 8.
# 
# With the new model, I was able to achieve a training score of around 0.88 with a test score of approximately 0.74. To visualize the decision tree, I decided to import tree from sklearn and installed graphviz using the pip install command. Once I confirmed that the decision tree complied with my model by comparatively analyzing the given data set from 'credit_data.csv', I plotted the decision tree. Currently, the tree only shows a max_depth of 3 due to sizing issues, but it can be expanded up to a max_depth of 8 for complete visualization.
# 
#  
# 
# The numbers that I pulled from my model include an accuracy rate, a training accuracy, and a testing accuracy. The accuracy rate I obtained on the training model is 100% because it calculates the number of correct classifications over the total number of classifications. Since the model was trained with the same data it's tested against, the accuracy logically is 100%. The number that is actually more insightful is the accuracy rate of the testing data. The whole reason I have the testing data is to be able to judge how accurate my model is. It calculates, with data that is new to the model, the number of correct 'test' classifications over the total number of 'test' classifications.
#
# When creating my decision tree, I chose a max depth of 8 to avoid overfitting the data while also capturing enough details to make the most accurate model. In this case, I found that the optimal max depth, or number of layers (splits), in my tree is 8, which allows for not overgeneralizing while also keeping the highest accuracy rate compared to the other outcomes from other depths. 
#
#In my decision tree visualization, the important numbers to note are the gini (gini impurity test), sample size, and the number that the variable in that leaf is less than or equal to. The sample size represents the occurrences that are being evaluated as either true or false within the leaf node, and the gini is a calculation that measures the probability of the node 'incorrectly' classifying an occurrence as true or false against the "<=" condition of the given variable. The closer the gini number is to zero, the higher the purity is, which is more optimal because it means there is less uncertainty or, in other words, less chance of the occurrence being incorrectly evaluated. 
#

# In[ ]:




