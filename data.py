# Script to generate 100,000 data points via a json file
import random
import json


class Data:
    def __init__(self, max_val):
        self.max_val = max_val
        self.data = []

    def generate(self):
        for i in range(100000):
            weight = random.randint(1, self.max_val)
            value = random.randint(1, self.max_val)
            self.data.append((weight, value))
        with open('data.json', 'w') as json_file:
            json.dump(self.data, json_file)


if __name__ == '__main__':
    data = Data(20)
    data.generate()
