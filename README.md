# TMXConverter
It converts .tmx files into different output formats.

## Overview
This tool facilitates the conversion of .tmx files with identical language combinations (same source and target languages) within a specified folder into various file formats: .tsv, .txt, .csv, or bitext (comprising two .txt files, one with the source language content and another with the target language content). These converted files are stored in an "output" folder created within the .tmx directory.

The user needs to specify the location of the .tmx files, provide the source and target languages (which must match those in the .tmx files), and indicate the desired output format(s) for the tmx file conversion (.tsv, .txt, .csv, bitext).

See "TMXConverter_1".png and "TMXConverter_2.png"

## Requirements:
Python 3
The utilized libraries are included with the Python installation by default.

## Files
TMXConverter.py

## Usage
1. Ensure the .tmx files that you intend to convert have the same language combinations and are located in an empty directory.
2. Run the "TMXConverter.py" script.
3. Enter the directory location of the .tmx files, the source language code, the target language code and the desired output format(s) separated by commas.
4. The script will generate the specified output file formats in an "output" folder within the same directory as the .tmx files.

## Important Note
The script eliminates all control characters prior to parsing the .tmx files to prevent errors.

## License
This project is governed by the GNU Affero General Public License v3.0. For comprehensive details, kindly refer to the LICENSE file included with this project.
