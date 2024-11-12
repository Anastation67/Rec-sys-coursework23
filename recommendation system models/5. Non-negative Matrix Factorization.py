#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
import sys
import os

class NMatrixFactorization:
    def __init__(self, num_users, num_items, num_factors=10, learning_rate=0.01, num_epochs=100):
        self.num_users = num_users
        self.num_items = num_items
        self.num_factors = num_factors
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs
        self.user_factors = None
        self.item_factors = None
    
    def fit(self, ratings):
        self.ratings = ratings
        
        self.user_factors = np.ones((int(self.num_users), self.num_factors))
        self.item_factors = np.ones((int(self.num_items), self.num_factors))

        for epoch in range(self.num_epochs):
            for user, item, rating in self.ratings:
                user = int(user)
                item = int(item)
                error = rating - np.dot(self.user_factors[user], self.item_factors[item])
                self.user_factors[user] += self.learning_rate * error * self.item_factors[item]
                self.item_factors[item] += self.learning_rate * error * self.user_factors[user]

                # Ensure non-negativity
                self.user_factors[self.user_factors < 0] = 0
                self.item_factors[self.item_factors < 0] = 0


    def predict(self, user, item):
        user = int(user)
        item = int(item)
        return np.dot(self.user_factors[user], self.item_factors[item])
    
    def evaluate(self, test_ratings):
        test_users = test_ratings[:, 0]
        test_items = test_ratings[:, 1]
        test_ratings = test_ratings[:, 2]
        predicted_ratings = np.array([self.predict(user, item) for user, item in zip(test_users, test_items)])
        mae = mean_absolute_error(test_ratings, predicted_ratings)
        return mae

    def recommend(self, user, top_n=5):
        user_ratings = self.ratings[self.ratings[:, 0] == user]
        user_items = user_ratings[:, 1]
        predictions = np.array([self.predict(user, int(item)) for item in range(int(self.num_items))])
        mask = np.logical_not(np.isin(range(int(self.num_items)), user_items))
        predictions[mask] = -np.inf
        top_items = np.argsort(predictions)[::-1][:top_n]
        return top_items

ratings = pd.read_csv('ratings.csv').drop(['Unnamed: 0'], axis=1)
providers = pd.read_csv('providers.csv').drop(['Unnamed: 0'], axis=1)
train = ratings[:50].to_numpy()
test = ratings[50:].reset_index().drop(['index'], axis=1)

num_users = np.max(train[:, 0]) + 1
num_items = np.max(train[:, 1]) + 1

# Create NMFRecommender instance
nmf = NMatrixFactorization(num_users, num_items, num_factors=10, learning_rate=0.01, num_epochs=100)

# Fit the model
nmf.fit(train)

# test
test = ratings[50:].drop(['User_id'], axis=1).reset_index().drop(['index'], axis=1).reset_index()
test.columns = test.columns.str.replace('index', 'User_id')
test

mae = nmf.evaluate(test.to_numpy())
print("MAE:", mae)

def user2userPredictions(userid, pred_path):
    """
    Сделаем предикт для каждого пользователя и сохраним в файл prediction.csv
    
    :param
        - userid : пользователя id
        - pred_path : куда сохраняем
    """    
    # поиск поставщиков
    reg_num = set(ratings['Registration number'].tolist())
    user = set(ratings[ratings['User_id'] == userid]['Registration number'].tolist())
    diff = list(reg_num - user) 
    
    try:

        # цикл по всем выбраным пользователям для предикта
        for itemid in diff:
            
            # предикт для пользователя, по элементам
            r_hat = nmf.predict(userid, itemid)  
#             print(r_hat)

            # сохраним
            with open(pred_path, 'a+') as file:
                line = '{},{},{}\n'.format(userid, itemid, r_hat)
                file.write(line)
                
    except IndexError:
        pass

def user2userNMF():
    """
    Предикт для всех пользователей, даже с 1 рейтингом   
    """
    # список всех пользователей
    users = ratings['User_id'].unique()
    
    def _progress(count):
        sys.stdout.write('\rRating predictions. Progress status : %.1f%%' % (float(count/len(users))*100.0))
        sys.stdout.flush()
    
    saved_predictions = 'predictionsNMf.csv'    
    if os.path.exists(saved_predictions):
        os.remove(saved_predictions)
    
    with open(saved_predictions, 'a+') as file:
        line = '{},{},{}\n'.format('User_id', 'Registration number', 'predicted_rating')
        file.write(line)
    
    for count, userid in enumerate(users):        
        # делаем предикт
        user2userPredictions(userid, saved_predictions)
        _progress(count)

def user2userRecommendation(userid, N=len(ratings.columns)):
    """
    Делаем предикт для пользователя
    """
    
    saved_predictions = 'predictionsNMf.csv'
    
    predictions = pd.read_csv(saved_predictions, sep=',')
    
    predictions = predictions[predictions['User_id']==userid]
    List = predictions.sort_values(by=['predicted_rating'], ascending=False)[:N]
    
    List = pd.merge(List, providers, on='Registration number', how='inner')
    
    return List

user2userNMF()

user2userRecommendation(0, 5).drop(['Registration number', 'Предмет поставки', 'Важная информация'], axis=1)
