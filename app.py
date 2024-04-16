from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


class Knapsack:
    def __init__(self):
        self.items = []
        self.dimensions = 10



    def create_data(self):
        for i in range(self.dimensions):
            row = []
            for j in range(self.dimensions):
                weight = random.randint(0, 20)
                value = random.randint(0, 20)
                row.append((weight, value))
            self.items.append(row)

@app.route('/')
def index():
    knapsack = Knapsack()
    knapsack.create_data()
    return render_template('index.html', knapsack=knapsack)


if __name__ == '__main__':
    app.run(debug=True)
