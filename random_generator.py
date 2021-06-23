import json
import random 
import sys

class Distribution(dict):

    def normalize(self):
        # normalize the distribution by summing over the distribution
        distribution_sum = sum(val for val in self.values())
        for key in self:
            self[key] /= distribution_sum
    
    def get_random_sample(self):
        key_list = list(self.keys())
        random_index = random.randint(0, len(key_list)-1)
        return key_list[random_index]


    def __missing__(self, key):
        # item not included in the distribution
        return 0

    @staticmethod
    def uniform(keys):
        # allows suer to make distribution that is uniform distribution with the given keys
        n = len(keys)
        dist = Distribution()
        for key in keys: dist[key] = 1/n

        return dist

    @staticmethod
    def from_json(filename):
        
        # get the data from the 
        with open(filename, "r") as f:
            json_data = json.load(f)


        # generate uniform distributions
        if json_data.get("type", 0) == "uniform":
            keys = json_data.get("keys", [])
            return Distribution.uniform(keys)

        # non-uniform
        elif json_data.get("type", 0) == "variable":
            stored_distribution = Distribution(json_data.get("dict", dict()))
            stored_distribution.normalize()
            return stored_distribution

        # if neither of these types, generate an empty distribution
        else:
            return Distribution()
        
    


if __name__ == "__main__":

    print("Welcome to the random generator. Let's get started")

    # no command line argument for the file given
    if len(sys.argv) < 2:
        filename = input("No file given, please enter a json file you want to read from: ")
    else:
        # first command line argument should be the name of the json file to use
        filename = sys.argv[1]

    print("Okay, going to generate from", filename)

    # load in the Distribution object
    dist = Distribution.from_json(filename)

    print("Great, evreything's loaded. How many samples would you like to generate?")
    iterations = int(input(">> "))
    user_input = ""
    STOP_WORDS = ("stop", "n", "quit")

    # generate the given number of samples 
    while user_input not in STOP_WORDS:
        print("Generating samples. Press ENTER after each one to generate another")

        for i in range(iterations):
            input(f"{i+1}: {dist.get_random_sample()}")
        
        print("Would you like to go again? Enter 'stop' to end or anything else to go again")
        user_input = input(">> ").lower()


    print("Thanks for using the generator")