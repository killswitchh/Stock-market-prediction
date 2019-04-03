#---------------------------------LINEAR REGRESSION PART-------------------------------#
import numpy as np
import pandas as pd

ourdata= pd.read_csv("company.csv")
ourdata.head()
ourdata.describe()

X = ourdata.iloc[:, 3:4:5]
YX = ourdata.iloc[:, 8]
print(X)

from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values='NaN')


from sklearn.model_selection import train_test_split
from sklearn import linear_model
##import matplotlib.pyplot as plt

inputVector = ourdata[['Symbol']]
outputVector = ourdata['Close Price']

XValue = inputVector.values
YValue = outputVector.values
X_train, X_test, Y_train, Y_test = train_test_split(XValue, YValue, test_size=0.5)


linearRegressionModel = linear_model.LinearRegression()
linearRegressionModel.fit(X_train, Y_train)

print('Coefficients: \n', linearRegressionModel.coef_)

linearRegressionModelPredictedValue = linearRegressionModel.predict(X_test)
p=[]
l=['Open Price']
#for i in range(1,10):
#    p.append(len(outputVector)+i)
p=[len(outputVector)+1]
k=np.array(p)
k=np.expand_dims(k,0)
y_pred=linearRegressionModel.predict(k)

print(y_pred)


##plt.scatter(ourdata['Date'], ourdata['Close Price'])
##plt.ylabel("OHL")
##plt.xlabel("close")
##plt.show()








#--------------------------------SENTIMENT ANALYSIS PART------------------------------------------#

import bs4 as bs 
import urllib.request
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
print("ENTER COMPANY NAME ")
cname=input()
if cname=="":
    print("Company name not entered")
    
else:
    cnamee=cname.capitalize()
    ucname=cname.upper()
    site= "https://economictimes.indiatimes.com/headlines.cms"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(site,headers=hdr)
    page = urllib.request.urlopen(req)
    soup = bs.BeautifulSoup(page,'lxml')
    
    
#--------------finding division containing top news--------------------
    div=soup.find(id="pageContent")
    l=[]
    li=[]
    
    
#--------------getting links from the division-------------------------
    for i in div.find_all('a'):
        l.append(i.get('href'))
        
        
#--------------adding https.. to the links got--------------------------
    for i in range(len(l)):        
        if("/articleshow/" in str(l[i])):
            li.append("https://economictimes.indiatimes.com/"+str(l[i]))

            
#------------------removes duplicate links-----------------------------
    lis=list(set(li))

    
#--------------prints list containing non duplicate links---------------
    #for i in range(len(lis)):
    #    print(lis[i])           

    print("No of links found =",len(li))             
    print("No of non duplicate links =",len(lis))    
    count=0
    art=[]
    c1=0
    ss=0
    neg=0
    pos=0
    yi=0

    
#-------CODE FOR SEARCHING THROUGH LINKS TO FIND THE COMPANY NAME-------
    print("SEARCHING LINKS FOR NEWS RELATED TO\t",ucname)
    for i in range(len(lis)):
        yes=0
        site= lis[i]
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(site,headers=hdr)
        response=requests.get(lis[i])
        if(response.status_code==404):
            continue                        
        page = urllib.request.urlopen(req)
        soup = bs.BeautifulSoup(page,'lxml')

        
#---------------finding division containing article text-----------------
        div=soup.find(class_="artText")

        
#---------------getting text and splitting lines from the division-------
        art.append(div.text.split("\n"))
        #print(art[0])

                       
#---------------filters empty list elements from the list of lines-------
        if(len(art[i]))==0:
            continue
        for j in art[i]:
            art[i]= list(filter(None, art[i]))        
        count=count+1

        
#-------Checking if the company name is in each line of every article----        

        for j in range (len(art[i])):
            if(cname in art[i][j] or cnamee in art[i][j] or ucname in art[i][j]):
                yes=1
                yi=1

                
#---------------------If company name is found----------------------------
        if(yes==1):
            c1=c1+1

            
#----------------prints link number along with link ----------------------
            print("\n",count,lis[i])

            
#------------------------------Vader analysis-----------------------------
            analyzer = SentimentIntensityAnalyzer()
            s=0
            for j in range(len(art[i])):
                vs = analyzer.polarity_scores(art[i][j])
                #print(vs['compound'])
                s=s+vs['compound']

                
#-------------------Average compound value for each article---------------
            vsa=s/len(art[i])

            
#-------------------Telling if the article is positive or not-------------            
            print("\nAverage polarity compund value=",vsa)
            if(vsa>0):
                print("Article is positive")
                pos=pos+1
            else:
                print("Article is negative")
                neg=neg+1
            ss=ss+vsa

            
#---------------------------If link not found--------------------------
    if(yi==0):
        print(cnamee,"has no news articles today")
        

            
#---------------------------END RESULT PRINTING--------------------------            
    if(yi==1):
        avsa=ss/c1
        print("\n")
        print("Value predicted using linear regression = ",y_pred)
        print("Positive links =",pos)
        print("Negative links =",neg)
        print("Total number of links containing ",cnamee,"=",c1)
        print("Average compound value for all the articles containing",cnamee,"=",avsa)
        if(avsa>0):
            print("Articles on",cnamee,"give an average positive result")
        else:
            print("Articles on",cnamee,"give an average negative result")
            
            

#---------------------------VALUE CALCULATION---------------------------
    print("value predicted by linear regression =",y_pred)
    if(avsa==0):
        ans=y_pred
        print(ans)

        
#---------------------------POSITIVE VALUE CALCULATION------------------
    if(avsa>0 and avsa<=0.1):
        ans=0+y_pred
        ans1=(0.04*y_pred)+y_pred
        print("code predicted 0-4% increase,estimated value will be between",ans,"and",ans1)
    if(avsa>=0.1 and avsa<=0.2):
        ans=(0.04*y_pred)+y_pred
        ans1=(0.08*y_pred)+y_pred
        print("code predicted 4-8% increase,estimated value will be between",ans,"and",ans1)
    if(avsa>=0.2 and avsa<=0.3):
        ans=(0.08*y_pred)+y_pred
        ans1=(0.12*y_pred)+y_pred
        print("code predicted 8-12% increase,estimated value will be between",ans,"and",ans1)
    if(avsa>=0.3 and avsa<=0.4):
        ans=(0.12*y_pred)+y_pred
        ans1=(0.16*y_pred)+y_pred
        print("code predicted 12-16% increase,estimated value will be between",ans,"and",ans1)
    if(avsa>=0.4 and avsa<=0.5):
        ans=(0.16*y_pred)+y_pred
        ans1=(0.20*y_pred)+y_pred
        print("code predicted 16-20% increase,estimated value will be between",ans,"and",ans1)
#----------------------------NEGATIVE VALUE CALCULATION--------------------

    if(avsa<0 and avsa>=-0.1):
        ans=0+y_pred
        ans1=-(0.04*y_pred)+y_pred
        print("code predicted 0-4% decrease,estimated value will be between",ans,"and",ans1)
    if(avsa<-0.1 and avsa>=-0.2):
        ans=-(0.04*y_pred)+y_pred
        ans1=-(0.08*y_pred)+y_pred
        print("code predicted 4-8% decrease,estimated value will be between",ans,"and",ans1)
    if(avsa<-0.2 and avsa>=-0.3):
        ans=-(0.08*y_pred)+y_pred
        ans1=-(0.12*y_pred)+y_pred
        print("code predicted 8-12% decrease,estimated value will be between",ans,"and",ans1)
    if(avsa<-0.3 and avsa>=-0.4):
        ans=-(0.12*y_pred)+y_pred
        ans1=-(0.16*y_pred)+y_pred
        print("code predicted 12-16% decrease,estimated value will be between",ans,"and",ans1)
    if(avsa<-0.4 and avsa>=-0.5):
        ans=-(0.16*y_pred)+y_pred
        ans1=-(0.20*y_pred)+y_pred
        print("code predicted 16-20% decrease,estimated value will be between",ans,"and",ans1)
