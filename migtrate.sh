#!/bin/bash

directory="/home/eris29/vscode/flask3/images/medium"  # Replace with the actual path to your target directory

# Change to the target directory
cd "$directory" || exit

# Loop through all files in the directory
for file in *; do
  if [[ -f $file ]]; then
    # Get the base name of the file (without extension)
    base_name="${file%.*}"
    
    # Rename the file with the new extension
    mv "$file" "${base_name}.jpg"
  fi
done
