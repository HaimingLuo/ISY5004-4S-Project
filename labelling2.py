
import os
import json

def restructure_json(directory, class_value="z"):
    """
    This function restructures each JSON file in the directory by extracting 'bbox' and 'pts' from 'info' and placing
    them at the top level of the JSON structure, alongside a new 'class' field.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r+', encoding='utf-8') as f:
                        data = json.load(f)
                        # Check if 'info' field is present and extract 'bbox' and 'pts'
                        if 'info' in data and isinstance(data['info'], list) and len(data['info']) > 0:
                            bbox_data = data['info'][0].get('bbox', [])
                            pts_data = data['info'][0].get('pts', {})
                            # Create new structure without 'info'
                            new_data = {
                                'class': class_value,
                                'bbox': bbox_data,
                                'pts': pts_data
                            }
                            # Write the modified data back to the file
                            f.seek(0)  # Reset file pointer to the beginning
                            json.dump(new_data, f, indent=4)
                            f.truncate()  # Truncate the file to the current position
                        else:
                            print(f"No 'info' field or it's incorrectly structured in {file_path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file {file_path}")
                except Exception as e:
                    print(f"An error occurred while processing file {file_path}: {str(e)}")

# Specify the directory containing your JSON files
directory_path = 'dataset2/z'
restructure_json(directory_path)
