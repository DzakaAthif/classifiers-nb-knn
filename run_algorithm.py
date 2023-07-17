import nb
import knn

def cvt(file_name):
    # Load training data
    data = []
    ls = None
    total_accuracy1 = 0
    total_accuracy2 = 0
    total_accuracy3 = 0

    with open(file_name, 'r') as file:
        for row in file:

            if row[:4] == "fold":
                if (ls != None):
                    data.append(ls)
                ls = []
                continue
            
            if row == '\n':
                continue

            row = row.strip()
            row = row.split(",")

            ls.append(row)

    data.append(ls)

    training_filename = "training-data.csv"
    testing_filename = "testing-data.csv"

    for i in range(len(data)):

        with open(testing_filename, "w") as file:
            for row in data[i]:
                file.write("{}\n".format(",".join(row[:-1])))
        
        with open(training_filename, "w") as file:
            for j in range(len(data)):
                if j == i:
                    continue

                for row in data[j]:
                    file.write("{}\n".format(",".join(row)))

        result_nb = nb.classify_nb(training_filename, testing_filename)
        result_knn1 = knn.classify_nn(training_filename, testing_filename, 1)
        result_knn5 = knn.classify_nn(training_filename, testing_filename, 5)
        correct_nb = 0
        correct_knn1 = 0
        correct_knn5 = 0

        for j in range(len(result_nb)):
            
            if result_nb[j] == data[i][j][-1]:
                correct_nb+=1

            if result_knn1[j] == data[i][j][-1]:
                correct_knn1+=1

            if result_knn5[j] == data[i][j][-1]:
                correct_knn5+=1

        accuracy1 = (correct_nb/len(result_nb))*100
        accuracy2 = (correct_knn1/len(result_nb))*100
        accuracy3 = (correct_knn5/len(result_nb))*100

        total_accuracy1+=accuracy1
        total_accuracy2+=accuracy2
        total_accuracy3+=accuracy3
    
    average1 = round(total_accuracy1/len(data), 4)
    average2 = round(total_accuracy2/len(data), 4)
    average3 = round(total_accuracy3/len(data), 4)
    print("nb: {}".format(average1))
    print("knn1: {}".format(average2))
    print("knn5: {}".format(average3))


cvt("pima-folds.csv")
    