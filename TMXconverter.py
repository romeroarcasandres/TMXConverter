import os
import xml.etree.ElementTree as ET
import csv

def find_and_replace(text, chars_to_replace):
    for char in chars_to_replace:
        text = text.replace(char, "")
    return text

def preprocess_tmx_file(file_path, chars_to_replace):
    with open(file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()
    for char in chars_to_replace:
        xml_content = xml_content.replace(char, "")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(xml_content)

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

    # Process each translation unit (<tu>) in the TMX.
    source_texts = []
    target_texts = []
    for tu in root.findall(".//tu"):
        src = ""
        tgt = ""
        for tuv in tu.findall("tuv"):
            lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', '').lower()
            seg = tuv.find("seg")
            if seg is None:
                continue
            text = "".join(seg.itertext())
            if lang.startswith(source_lang.lower()):
                src = text
            elif lang.startswith(target_lang.lower()):
                tgt = text
        source_texts.append(src)
        target_texts.append(tgt)
    return source_texts, target_texts

def remove_empty_and_whitespace_only(source_texts, target_texts):
    cleaned_source = []
    cleaned_target = []
    for src, tgt in zip(source_texts, target_texts):
        if src and tgt and src.strip() and tgt.strip():
            cleaned_source.append(src.strip())
            cleaned_target.append(tgt.strip())
    return cleaned_source, cleaned_target

def escape_newlines(text):
    """
    Replace any actual newline characters with the literal two-character sequence "\n".
    This ensures that each translation unit (TU) is output as a single physical line.
    """
    if text is None:
        return ""
    return text.replace("\n", "\\n")

def generate_output_files(directory, source_lang, target_lang, output_formats):
    output_folder = os.path.join(directory, "output")
    os.makedirs(output_folder, exist_ok=True)

    for root_dir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tmx"):
                file_path = os.path.join(root_dir, file)
                source_texts, target_texts = parse_tmx_file(file_path, source_lang, target_lang)
                source_texts, target_texts = remove_empty_and_whitespace_only(source_texts, target_texts)

                # Escape internal newlines so that each TU becomes one physical line.
                escaped_source = [escape_newlines(text) for text in source_texts]
                escaped_target = [escape_newlines(text) for text in target_texts]

                for output_format in output_formats:
                    output_format = output_format.strip().lower()
                    if output_format == "tsv":
                        output_filename = f"{os.path.splitext(file)[0]}_{output_format}.{output_format}"
                        output_filepath = os.path.join(output_folder, output_filename)
                        with open(output_filepath, "w", encoding="utf-8", newline="") as tsv_file:
                            writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
                            writer.writerows(zip(escaped_source, escaped_target))
                        print(f"Generated TSV: {output_filepath}")
                    elif output_format == "txt":
                        # Combined TXT file: each line contains source and target separated by a tab.
                        output_filename = f"{os.path.splitext(file)[0]}_{output_format}.{output_format}"
                        output_filepath = os.path.join(output_folder, output_filename)
                        with open(output_filepath, "w", encoding="utf-8") as txt_file:
                            for src, tgt in zip(escaped_source, escaped_target):
                                txt_file.write(f"{src}\t{tgt}\n")
                        print(f"Generated TXT: {output_filepath}")
                    elif output_format == "csv":
                        output_filename = f"{os.path.splitext(file)[0]}_{output_format}.{output_format}"
                        output_filepath = os.path.join(output_folder, output_filename)
                        with open(output_filepath, "w", encoding="utf-8", newline="") as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerows(zip(escaped_source, escaped_target))
                        print(f"Generated CSV: {output_filepath}")
                    elif output_format == "bitext":
                        # For bitext, generate two separate text files.
                        # The extension of each file is now the corresponding language code.
                        source_file_name = f"{os.path.splitext(file)[0]}.{source_lang.lower()}"
                        target_file_name = f"{os.path.splitext(file)[0]}.{target_lang.lower()}"
                        source_filepath = os.path.join(output_folder, source_file_name)
                        target_filepath = os.path.join(output_folder, target_file_name)
                        with open(source_filepath, "w", encoding="utf-8") as source_txt_file:
                            for text in escaped_source:
                                source_txt_file.write(text + "\n")
                        with open(target_filepath, "w", encoding="utf-8") as target_txt_file:
                            for text in escaped_target:
                                target_txt_file.write(text + "\n")
                        print(f"Generated bitext files: {source_filepath} and {target_filepath}")
                    else:
                        print(f"Unsupported output format: {output_format}")

if __name__ == "__main__":
    directory = input("Enter the directory location of the .tmx files with the same source and target language: ")
    source_lang = input("Enter the source language code: ")
    target_lang = input("Enter the target language code: ")
    output_formats = input("Enter desired output format(s) separated by commas (e.g., tsv,txt,csv,bitext): ").split(',')
    generate_output_files(directory, source_lang, target_lang, output_formats)
    print("Conversion completed successfully.")
