import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

path = "spam.csv"
features = ['label', 'message']
sms = pd.read_csv(path, header=0, names=features,encoding="latin_1",usecols=[0,1])

# convert label to a numerical variable
sms['label_num'] = sms.label.map({'ham':0, 'spam':1})


vect = CountVectorizer()
X = sms.message
y = sms.label_num

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)


nb = MultinomialNB()

X_train_dtm = vect.fit_transform(X_train)

nb.fit(X_train_dtm, y_train)

def makePrediction(message):
    X_test = pd.DataFrame([ {'message': message}]).message
    X_test_dtm = vect.transform(X_test)
    prediction=nb.predict(X_test_dtm)[0]
    if (prediction == 0):
        return "ham"
    else:
        return "spam"


#answer = makePrediction("hello world you call me")
#print(answer)

#print(makePrediction("winner customer you have won"))

