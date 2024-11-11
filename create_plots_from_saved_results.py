import matplotlib.pyplot as plt
import seaborn as sns

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
        lines = file.readlines()
        first = True
        file_names = []
        actuals = []
        predictions = []
        
        for line in lines:
            # skip first line
            if first:
                first = False
                continue

            parts = line.strip().split(',')
            file_names.append(parts[0])
            actuals.append(int(parts[1]))
            predictions.append(float(parts[2]))

    # Plot the results
    min_val = min(min(actuals), min(predictions), 1000)
    max_val = max(max(actuals), max(predictions), 2000)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=actuals, y=predictions, alpha=0.5)
    plt.xlabel('Actual Year')
    plt.ylabel('Predicted Year')
    plt.title(f'Actual vs Predicted Year for {model_name}')
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')  # Diagonal line
    plt.show()
    plt.savefig(f'models/{model_name}/{model_name}_actual_vs_predicted.png')
    plt.savefig(f'models/{model_name}/{model_name}_actual_vs_predicted.pdf')


if __name__ == '__main__':
    model_name = input("Input the model you would like to use and save all results (svm / ridge / neural): ").strip()
    main(model_name)