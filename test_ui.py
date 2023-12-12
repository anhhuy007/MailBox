import os

# Get the current directory
current_directory = "D:\MailBox\Filter\hahuy@fitus.edu.vn"

# Get a list of all subdirectories in the current directory
subdirectories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]

# Print the list of subdirectories
print("Subdirectories in", current_directory, ":", subdirectories)
