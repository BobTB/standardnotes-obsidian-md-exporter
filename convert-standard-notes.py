import json
import os
import re
import sys
import argparse
from datetime import datetime


def to_camel_case(title):
    """Convert a title to camel case."""
    return "".join(word.capitalize() for word in title.split())


def windows_compatible_filename(filename):
    """Make filename compatible with Windows filesystem."""
    windows_illegal_chars = r'[<>:"/\\|?*]'
    new_filename = re.sub(windows_illegal_chars, '_', filename)
    return new_filename


def unique_filename(filename):
    """Generate a unique filename."""
    counter = 1
    name, extension = os.path.splitext(filename)
    while os.path.exists(filename):
        filename = f"{name}_{counter}{extension}"
        counter += 1
    return filename


def check_exported_notes(data, exported_notes, tags):
    """Check if all notes have been exported and print any missing ones."""
    notes_in_json = sum(1 for item in data['items'] if item['content_type'] == "Note")
    md_files_count = sum(1 for file in os.listdir() if file.endswith('.md'))

    print(f"Total notes in JSON: {notes_in_json}")
    print(f"Total markdown files created: {md_files_count}")

    if notes_in_json != md_files_count:
        print("Some notes were not exported to files. Missing notes:")
        for item in data['items']:
            if item['content_type'] == "Note" and item['uuid'] not in exported_notes:
                tag_uuids = [ref['uuid'] for ref in item['content']['references'] if ref['content_type'] == "Tag"]
                tag_names = [tags[uuid] for uuid in tag_uuids]
                print(f"Title: {item['content']['title']}")
                print(f"Tags: {', '.join(tag_names)}")
                print(f"Text: {item['content']['text']}")
                print("-----")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert Standard Notes JSON export to individual Markdown files.")
    parser.add_argument("input_file", help="Path to the Standard Notes JSON export file.")
    args = parser.parse_args()
    input_file = args.input_file

    # Load data from input file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Check if data is in the new format
    is_new_version = "version" in data and data["version"] == "004"

    # Initialize tags and note_tags dictionaries
    tags = {}
    note_tags = {}

    # Process tags
    for item in data['items']:
        if item['content_type'] == "Tag":
            uuid = item['uuid']
            title = item['content']['title']
            camel_case_title = to_camel_case(title)
            tags[uuid] = camel_case_title

            # If data is in the new format, process note_tags
            if is_new_version:
                for ref in item['content']['references']:
                    if ref['content_type'] == "Note":
                        note_uuid = ref['uuid']
                        if note_uuid not in note_tags:
                            note_tags[note_uuid] = []
                        note_tags[note_uuid].append(camel_case_title)

    print("Processing notes...")

    exported_notes = set()

    # Process notes
    for item in data['items']:
        if item['content_type'] == "Note":
            note = item
            title = re.sub(r'/', '-', note['content']['title'])
            text = note['content']['text']
            note_uuid = note['uuid']

            # Handle tags based on the data format
            if is_new_version:
                tag_line = " ".join([f"#{tag.lstrip('#')}" for tag in note_tags.get(note_uuid, [])])
            else:
                tag_uuids = [ref['uuid'] for ref in note['content']['references'] if ref['content_type'] == "Tag"]
                tag_line = " ".join([f"#{tags[uuid]}" for uuid in tag_uuids])

            # Add tags to the text
            if tag_line:
                text = f"{tag_line}\n\n{text}"

            # Create markdown file if the title is not empty
            if title:
                filename = f"{title}.md"
                windows_safe_filename = windows_compatible_filename(filename)
                unique_name = unique_filename(windows_safe_filename)
                with open(unique_name, "w") as note_file:
                    note_file.write(text)
                print(f"Created: ./{unique_name}")
                exported_notes.add(note['uuid'])
            else:
                print(f"Note with error text: {text}")
                print("Skipping note with empty title.")

            def set_file_time(filename, created_at_str, updated_at_str):
                """Set the file's creation and modification time."""
                created_at = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
                updated_at = datetime.strptime(updated_at_str, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
                os.utime(filename, (created_at, updated_at))

            # Set file's creation and modification time
            set_file_time(unique_name, note['created_at'], note['updated_at'])

    # Check for any missing notes
    check_exported_notes(data, exported_notes, tags)


if __name__ == "__main__":
    main()
