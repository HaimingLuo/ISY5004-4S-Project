import os
import json

def restructure_json(directory, class_value="y"):
    """
    This function restructures each JSON file in the directory by removing
    'bbox' and maintaining 'pts' under its original key, while adding 'class' at the top level.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r+', encoding='utf-8') as f:
                        data = json.load(f)
                        # Extracting 'pts' from the first element of 'info' list
                        if isinstance(data['info'], list) and len(data['info']) > 0:
                            pts_data = data['info'][0].get('pts', {})
                            new_data = {'class': class_value, 'pts': pts_data}  # Combine 'class' and 'pts' at the same level

                            # Write the modified data back to the file
                            f.seek(0)  # Reset file pointer to the beginning
                            json.dump(new_data, f, indent=4)
                            f.truncate()  # Truncate the file to the current position
                        else:
                            print(f"No 'info' list found or it's empty in {file_path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file {file_path}")
                except Exception as e:
                    print(f"An error occurred while processing file {file_path}: {str(e)}")

# Specify the directory containing your JSON files
directory_path = 'dataset/y'
restructure_json(directory_path)

