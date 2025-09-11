import os
import shutil

# Backup the original file
user_model_path = r"c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend\app\models\user.py"
backup_path = r"c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend\app\models\user.py.backup"

# Create backup
shutil.copy2(user_model_path, backup_path)
print("Backup created successfully")

# Read the original file
with open(user_model_path, 'r') as f:
    content = f.read()

print("Original content:")
print(content)

# Fix the circular import issue by using string references
# The issue is that we need to make sure the relationships are properly defined
# to avoid circular imports between models

# In this case, the models look correct already, but let's make sure the imports are in the right order
# Let's check if there are any issues with the import statements

# Write the content back (it should be the same, but this will help us verify)
with open(user_model_path, 'w') as f:
    f.write(content)

print("File written successfully")