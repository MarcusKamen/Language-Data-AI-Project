import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
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
        
        for parts in reader:
            # skip first line
            if first:
                first = False
                continue

            if len(parts) < 3:
                continue

            file_names.append(parts[0])
            actuals.append(int(parts[1]))
            predictions.append(float(parts[2]))

    # Calculate the Pearson correlation coefficient
    r_value, _ = pearsonr(actuals, predictions)

    # Print the r value
    print(f'Pearson correlation coefficient (r): {r_value:.2f}')

    # Plot the results
    min_val = min(min(actuals), min(predictions), 1000)
    max_val = max(max(actuals), max(predictions), 2000)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=actuals, y=predictions, alpha=0.5)
    plt.xlabel('Actual Year')
    plt.ylabel('Predicted Year')
    plt.title(f'Actual vs Predicted Year for {model_name}')
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')  # Diagonal line
    plt.xlim(1800, max_val)
    plt.ylim(1800, max_val)
    plt.savefig(f'models/{model_name}/{model_name}_actual_vs_predicted.png')
    plt.savefig(f'models/{model_name}/{model_name}_actual_vs_predicted.pdf')
    plt.show()


if __name__ == '__main__':
    model_name = input("Input the model you would like to use and save all results (svm / ridge / neural): ").strip()
    main(model_name)