import csv

SVM_PRED_SAVE_PATH = "final_pickles/svm/all_results.csv"
RIDGE_PRED_SAVE_PATH = "final_pickles/ridge/all_results.csv"
NEURAL_PRED_SAVE_PATH = "models/neural/all_results.csv"

def main(model_name):
    if model_name == 'svm':
        save_path = SVM_PRED_SAVE_PATH
    elif model_name == 'ridge':
        save_path = RIDGE_PRED_SAVE_PATH
    elif model_name == 'neural':
        save_path = NEURAL_PRED_SAVE_PATH
    else:
        print("Invalid model name")
        return
    
    with open(save_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
        first = True
        file_names = []
        actuals = []
        predictions = []
        titles = []
        authors = []
        
        for parts in reader:
            # skip first line
            if first:
                first = False
                continue

            file_names.append(parts[0])
            actuals.append(int(parts[1]))
            predictions.append(float(parts[2]))
            titles.append(parts[3])
            authors.append(parts[4])

    with open('outliers_and_weird_data.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Filename', 'Actual', 'Predicted', 'Title', 'Author'])
        for i in range(len(file_names)):
            # if actuals[i] >= 1950:
            #     writer.writerow([file_names[i], actuals[i], predictions[i], titles[i], authors[i]])
            if actuals[i] != 1800 and (abs(actuals[i] - predictions[i]) > 100 or actuals[i] < 1600 or actuals[i] > 1990):
                writer.writerow([file_names[i], actuals[i], predictions[i], titles[i], authors[i]])
    
if __name__ == '__main__':
    model_name = input("Input the model you would like to check outliers and weird metadata (svm / ridge / neural): ").strip()
    main(model_name)