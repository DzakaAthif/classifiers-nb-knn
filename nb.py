from math import sqrt
from math import e
from math import pi

def classify_nb(training_filename, testing_filename):

    # Load training data
    train_data = []
    total_yes = 0
    total_no = 0

    with open(training_filename, 'r') as file:
        for row in file:
            row = row.strip()
            row = row.split(",")

            # convert from str to float
            for i in range(len(row)-1):
                row[i] = float(row[i])

            if row[-1] == "yes":
                total_yes+=1
            else:
                total_no+=1

            train_data.append(row)

    # Calc num of attribute without class
    temp = train_data[0]
    num_atr = len(temp)-1

    # Create the list to store the mean and sd
    mean_yes, mean_no, sd_yes, sd_no = init_var(num_atr)

    # Calc the mean
    mean_yes, mean_no = calc_mean(mean_yes, mean_no, train_data,
                            num_atr, total_yes, total_no)
    
    # Calc the standard deviation
    sd_yes, sd_no = calc_sd(sd_yes, sd_no, train_data,
                        num_atr, total_yes, total_no, 
                        mean_yes, mean_no)

    # Calc P(yes) and P(no)
    p_yes = total_yes/len(train_data)
    p_no = total_no/len(train_data)

    # Apply naive bayes algorithm to the testing data
    result = apply_nb(testing_filename, mean_yes, mean_no, 
                            sd_yes, sd_no, p_yes, p_no)

    return result


def init_var(num_atr):
    mean_yes = []
    mean_no = []
    sd_yes = []
    sd_no = []

    for i in range(num_atr):
        mean_yes.append(0)
        mean_no.append(0)
        sd_yes.append(0)
        sd_no.append(0)

    return mean_yes, mean_no, sd_yes, sd_no


def calc_mean(mean_yes, mean_no, train_data, 
              num_atr, total_yes, total_no):
    
    # Sum all the rows
    for row in train_data:
        if row[-1] == "yes":
            for i in range(num_atr):
                mean_yes[i] = mean_yes[i] + row[i]
        else:
            for i in range(num_atr):
                mean_no[i] = mean_no[i] + row[i]

    # Divide the total with the number of rows for yes
    # or for no
    for i in range(num_atr):
        mean_yes[i] = mean_yes[i]/total_yes
        mean_no[i] = mean_no[i]/total_no

    return mean_yes, mean_no


def calc_sd(sd_yes, sd_no, train_data, 
              num_atr, total_yes, total_no,
              mean_yes, mean_no):
    
    # Sum the (row - mean)^2
    for row in train_data:
        if row[-1] == "yes":
            for i in range(num_atr):
                sd_yes[i] = sd_yes[i] + pow(row[i]-mean_yes[i], 2)
        else:
            for i in range(num_atr):
                sd_no[i] = sd_no[i] + pow(row[i]-mean_no[i], 2)

    # Divide the total with numOfRows-1, then square root
    for i in range(num_atr):
        sd_yes[i] = sqrt(sd_yes[i]/(total_yes-1))
        sd_no[i] = sqrt(sd_no[i]/(total_no-1))

    return sd_yes, sd_no


def apply_nb(testing_filename, mean_yes, mean_no, 
            sd_yes, sd_no, p_yes, p_no):
    
    # Load testing data
    result = []
    correct = 0

    with open(testing_filename, 'r') as file:
        for row in file:

            row = row.strip()
            row = row.split(",")

            # convert from str to float
            num_atr = len(row)-1
            for i in range(num_atr):
                row[i] = float(row[i])

            p_yes_e = p_yes
            p_no_e = p_no

            for i in range(num_atr):
                # Calc the P(Yes|E)
                sd, mean, x = sd_yes[i], mean_yes[i], row[i]

                pow_val = -(pow((x-mean), 2)/(2*pow(sd, 2)))
                val1 = 1/(sd*sqrt(2*pi))
                val2 = pow(e, pow_val)
                pdf_yes = val1*val2
                
                p_yes_e = p_yes_e*pdf_yes

                # Calc the P(No|E)
                sd, mean, x = sd_no[i], mean_no[i], row[i]

                pow_val = -(pow((x-mean), 2)/(2*pow(sd, 2)))
                val1 = 1/(sd*sqrt(2*pi))
                val2 = pow(e, pow_val)
                pdf_no = val1*val2

                p_no_e = p_no_e*pdf_no

            class_var = ""
            if p_no_e > p_yes_e:
                class_var = "no"
            else:
                class_var = "yes"            

            if class_var == row[-1]:
                correct+=1

            result.append(class_var)
        
        accuracy = (correct/len(result))*100

    return result