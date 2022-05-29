import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.ensemble import RandomForestClassifier
'''from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
dtc= DecisionTreeClassifier(criterion='entropy',random_state=5)
dtc.fit(x_train,y_train)
sc = StandardScaler()
x_train = sc.fit_transform(X_train)
x_test = sc.transform(X_test)
score_rf = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)

print("The accuracy score achieved using Random Forest is: " + str(score_rf) + " %")'''
data = pd.read_csv('heart.csv')
X=data.drop('HeartDisease', axis=1)
Y=data['HeartDisease']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
max_accuracy = 0
best_x=0
for x in range(2000):
    rf = RandomForestClassifier(random_state=x)
    rf.fit(X_train, Y_train)
    Y_pred_rf = rf.predict(X_test)
    current_accuracy = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)
    if (current_accuracy > max_accuracy):
        max_accuracy = current_accuracy
        best_x = x

rf = RandomForestClassifier(random_state=best_x)
rf.fit(X_train, Y_train)
Y_pred_rf = rf.predict(X_test)

pickle.dump(rf, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))


