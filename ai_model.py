from sklearn.tree import DecisionTreeClassifier

def train_model():
    X = [
        [255, 0, 0, 30, 4],   # Fruit
        [0, 0, 0, 20, 6],     # Bomb
        [0, 255, 0, 25, 5],   # Fruit
        [0, 0, 0, 18, 8]      # Bomb
    ]
    y = ["fruit", "bomb", "fruit", "bomb"]
    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model