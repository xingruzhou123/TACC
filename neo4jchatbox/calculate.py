import pandas as pd

def count_unique_numbers(file_path):
    # Load the ODS file
    data = pd.read_excel(file_path, engine='odf')

    # Extract non-NaN values from both columns and combine them into a single list
    node_ids = data['nodeId'].dropna().tolist()
    connected_node_ids = data['connectedNodeId'].dropna().tolist()

    # Combine the lists
    all_numbers = node_ids + connected_node_ids

    # Convert to a set to remove duplicates and then back to a list to count occurrences
    unique_numbers = list(set(all_numbers))

    # Create a dictionary to count occurrences of each unique number
    number_counts = {int(num): all_numbers.count(num) for num in unique_numbers}

    # Convert the dictionary to a DataFrame for better visualization
    number_counts_df = pd.DataFrame(list(number_counts.items()), columns=['Number', 'Count'])
    
    return number_counts_df

# Specify the path to your ODS file
file_path = '/home/xingru/tacctest/datafull.ods'

# Get the counts of unique numbers
number_counts_df = count_unique_numbers(file_path)

# Extract numbers and counts into separate lists
numbers = number_counts_df['Number'].tolist()
counts = number_counts_df['Count'].tolist()

# Print the results in the desired format
print(f"number[{','.join(map(str, numbers))}]")
print(f"Count[{','.join(map(str, counts))}]")

