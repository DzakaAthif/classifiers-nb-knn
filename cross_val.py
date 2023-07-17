import math
import heapq

class Fold:
    fold_num = None
    n_num = None
    y_num = None
    no_ls = None
    yes_ls = None

    def __init__(self, fold_num):
        self.fold_num = fold_num
        self.n_num = 0
        self.y_num = 0
        self.no_ls = []
        self.yes_ls = []

    def __str__(self):
        return "{}".format(self.fold_num)

    def append_no(self, line):
        self.no_ls.append(line)
        self.n_num+=1

    def append_yes(self, line):
        self.yes_ls.append(line)
        self.y_num+=1

def create_folds(filename, fold_num):

    lines = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            line = line.split(",")
            lines.append(line)

    # calculate the ratio of yes and no in a fold.
    yes = 0
    no = 0

    for line in lines:

        if line[-1] == "yes":
            yes+=1
        else:
            no+=1

    per_fold = math.floor(len(lines)/10)
    yes_ratio = round((yes/len(lines))*per_fold)
    no_ratio = round((no/len(lines))*per_fold)
    print("total rows: {}\nyes ratio: {}".format(len(lines), yes_ratio)+
          "\nno ratio: {} \n".format(no_ratio))

    # creates the folds.
    yes_ls = []
    no_ls = []
    folds_dict = {}
    for i in range(fold_num):
        fold_num = i+1

        fold = Fold(fold_num)
        folds_dict[fold_num] = fold

        yes_ls.append((0, fold_num))
        no_ls.append((0, fold_num))

    heapq.heapify(yes_ls)
    heapq.heapify(no_ls)

    # put the rows in the folds.
    for line in lines:
        
        if line[-1] == "yes":
            yes_num, fold_num = heapq.heappop(yes_ls)
            fold = folds_dict[fold_num]
            fold.append_yes(line)
            yes_num = fold.y_num
            heapq.heappush(yes_ls, (yes_num, fold_num))
        else:
            no_num, fold_num = heapq.heappop(no_ls)
            fold = folds_dict[fold_num]
            fold.append_no(line)
            no_num = fold.n_num
            heapq.heappush(no_ls, (no_num, fold_num))

    res = ""
    
    folds = list(folds_dict.values())

    for fold in folds:
        print("fold{}".format(fold))
        print("no rows: {}".format(fold.n_num))
        print("yes rows: {}\n".format(fold.y_num))

        res+="fold{}\n".format(fold)

        for row in fold.yes_ls:
            res+=",".join(row)+"\n"
        
        for row in fold.no_ls:
            res+=",".join(row)+"\n"

        res+="\n"
    
    res = res.strip()

    with open("pima-folds.csv", 'w') as file:
        file.write(res)

if __name__ == '__main__':
    create_folds("pima.csv", 10)