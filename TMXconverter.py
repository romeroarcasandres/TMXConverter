import os
import xml.etree.ElementTree as ET
import csv

# Function to find and replace characters in a text
def find_and_replace(text, chars_to_replace):
    for char in chars_to_replace:
        text = text.replace(char, "")
    return text

# Function to preprocess the TMX file by finding and replacing specified characters
def preprocess_tmx_file(file_path, chars_to_replace):
    with open(file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    for char in chars_to_replace:
        xml_content = xml_content.replace(char, "")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(xml_content)

# Function to parse the TMX file and extract source and target texts
def parse_tmx_file(file_path, source_lang, target_lang):
    chars_to_replace = [
        "&#x0;", "&#x1;", "&#x2;", "&#x3;", "&#x4;", "&#x5;", "&#x6;", "&#x7;",
        "&#x8;", "&#x9;", "&#xA;", "&#xB;", "&#xC;", "&#xD;", "&#xE;", "&#xF;",
        "&#x10;", "&#x11;", "&#x12;", "&#x13;", "&#x14;", "&#x15;", "&#x16;", "&#x17;",
        "&#x18;", "&#x19;", "&#x1A;", "&#x1B;", "&#x1C;", "&#x1D;", "&#x1E;", "&#x1F;"
    ]
    preprocess_tmx_file(file_path, chars_to_replace)

    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {"xml": "http://www.w3.org/XML/1998/namespace"}

    source_texts = []
    target_texts = []

    for tu in root.findall(".//tuv[@xml:lang='{0}']/seg".format(source_lang), namespaces=ns):
        source_text = tu.text
        source_texts.append(source_text)

    for tu in root.findall(".//tuv[@xml:lang='{0}']/seg".format(target_lang), namespaces=ns):
        target_text = tu.text
        target_texts.append(target_text)

    return source_texts, target_texts

# Function to generate output files based on specified formats
def generate_output_files(directory, source_lang, target_lang, output_formats):
    output_folder = os.path.join(directory, "output")
    os.makedirs(output_folder, exist_ok=True)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tmx"):
                file_path = os.path.join(root, file)

                source_texts, target_texts = parse_tmx_file(file_path, source_lang, target_lang)

                for output_format in output_formats:
                    output_filename = f"{os.path.splitext(file)[0]}_{output_format}.{output_format}"
                    output_filepath = os.path.join(output_folder, output_filename)

                    if output_format == "tsv":
                        with open(output_filepath, "w", encoding="utf-8", newline="") as tsv_file:
                            writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
                            writer.writerows(zip(source_texts, target_texts))
                    elif output_format == "txt":
                        with open(output_filepath, "w", encoding="utf-8") as txt_file:
                            for source, target in zip(source_texts, target_texts):
                                txt_file.write(f"{source}\t{target}\n")
                    elif output_format == "csv":
                        with open(output_filepath, "w", encoding="utf-8", newline="") as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerows(zip(source_texts, target_texts))
                    elif output_format == "bitext":
                        source_file_name = f"{os.path.splitext(file)[0]}_{source_lang}.txt"
                        target_file_name = f"{os.path.splitext(file)[0]}_{target_lang}.txt"
                        
                        source_filepath = os.path.join(output_folder, source_file_name)
                        target_filepath = os.path.join(output_folder, target_file_name)

                        with open(source_filepath, "w", encoding="utf-8") as source_txt_file:
                            source_txt_file.write('\n'.join([str(text) for text in source_texts if text is not None]))

                        with open(target_filepath, "w", encoding="utf-8") as target_txt_file:
                            target_txt_file.write('\n'.join([str(text) for text in target_texts if text is not None]))

                    else:
                        print(f"Unsupported output format: {output_format}")

if __name__ == "__main__":
    # User input for directory, source language, target language, and output formats
    directory = input("Enter the directory location of the .tmx files with the same source and target language: ")
    source_lang = input("Enter the source language code: ")
    target_lang = input("Enter the target language code: ")
    output_formats = input("Enter desired output format(s) separated by commas (e.g., tsv,txt,csv,bitext): ").split(',')

    # Generate output files based on user input
    generate_output_files(directory, source_lang, target_lang, output_formats)

    # Print completion message
    print("Conversion completed successfully.")
