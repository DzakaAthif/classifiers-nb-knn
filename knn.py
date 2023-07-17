import math

def classify_nn(training_file, testing_file, k):
    # check if k is an integer
    if not isinstance(k, int):
        return

    # store training data
    tf_data = []
    with open(training_file, 'r') as tf:
        for line in tf:
            new_line = []
            line = line.strip()
            line = line.split(",")

            for d in line:
                if d.replace(".", "", 1).isdigit():  # check whether is float
                    new_line.append(float(d))
                else:
                    new_line.append(d)

            tf_data.append(new_line)

    # store testing data
    test_data = []
    with open(testing_file, 'r') as test:
        for line in test:
            new_line = []
            line = line.strip()
            line = line.split(",")

            for d in line:
                # try:
                    new_line.append(float(d))
                # except:
                #     raise Exception("testing file contains invalid data:(")

            test_data.append(new_line)

    # initialize variables
    number_attr = len(test_data[0])
    output_data = []

    for test_line in test_data:
        index = 0;
        j = 0;
        euclidean_cal = []
        match_class = []
        # euclidean distances with each training data-class
        # contains tuples
        Dresults_class = []
        yes = 0
        no = 0

        for tf_line in tf_data:
            match_class.append(tf_line[-1].lower())
            euclidean = 0
            for i in range(number_attr):
                euclidean += (tf_line[i]-test_line[i])**2

            euclidean_cal.append(math.sqrt(euclidean))

        Dresults_class = list(zip(euclidean_cal, match_class))
        Dresults_class.sort()

        # compare results based on k
        del Dresults_class[k:len(Dresults_class)]
        for distance in Dresults_class:
            if distance[1] == "yes":
                yes += 1
            else:
                no += 1

        if yes >= no:
            output_data.append("yes")
        else:
            output_data.append("no")

    return output_data

if __name__ == '__main__':
    print(classify_nn("pima.csv", "test.csv", 1))


        





        










