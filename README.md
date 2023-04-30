# Standard Notes Markdown Export for Obsidian

A Python script to convert Standard Notes JSON export to individual Markdown files compatible with Obsidian https://obsidian.md/ while maintaining tags and file timestamps. 

## Compatibility with Other Markdown Editors

While this tool is designed with Obsidian users in mind, the generated Markdown files are compatible with any Markdown editor. This means you can easily import and use your Standard Notes content in other Markdown-based applications as well.

## Features

- Converts Standard Notes JSON export to individual Markdown files

- Supports two formats, old format with no version in the json file (from old Standard File server) and version '004' of the JSON export format (current one)

- Maintains tags - adds them at the beginning of each exported note, not tested with nested tags as I dont have Standard Notes subscription. 

- Transforms tags to CamelCase and removes spaces, since Obsidian doesn't allow spaces in tag names

- Updates the created file timestamps to keep the creation and modification time for the notes

- Automatically handles Windows-incompatible filenames since Standard Notes allows characters like '?', '/' etc. in note titles

- Ensures unique filenames to prevent overwriting, as multiple notes with the same name are possible in Standard Notes

## Usage

1. Export your Standard Notes data as an unencrypted JSON file.

2. Clone or download this repository to your local machine.

3. Install Python 3.6 or higher if you haven't already.

4. Open a terminal or command prompt and navigate to the directory containing the `convert-standard-notes.py` script. 

5. Run the script with your JSON export file as an argument:

    ```python3 convert-standard-notes.py exportFile.json```

6. The script will create individual Markdown files for each note in the same directory as the script.

8. Open the directory from Obisidan as a new Vault

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)