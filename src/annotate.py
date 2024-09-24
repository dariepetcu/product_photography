import os

# Specify the directory path
directory = 'nivea/dataset/'

# Iterate through each file in the directory
for filename in os.listdir(directory):
    
    new_filename = f"{os.path.splitext(filename)[0]}.txt"
    
    # Create the full path for the new file
    new_filepath = os.path.join(directory, new_filename)
    
    # Write 'perfume' to the new text file
    with open(new_filepath, 'w') as f:
        f.write("TOK aftershave")
    
    print(f"Created: {new_filename}")

print("Process completed.")