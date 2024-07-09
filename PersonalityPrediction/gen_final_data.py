import csv
import os
import sys

def is_extroverted(base_line_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size):
    # Corrected logical grouping with parentheses for clarity
    if (letter_size > 3 and -1 < slant_angle <= 1) or top_margin > 20 or line_spacing >= 5 or word_spacing > 4:
        return 1
    else:
        return 0

def is_introverted(base_line_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size):
    # Corrected logical grouping with parentheses for clarity
    if (letter_size < 2.5 and -15 <= slant_angle < 0) and (top_margin < 20 or word_spacing <= 2 or 3 < line_spacing < 5):
        return 1
    else:
        return 0

def has_emotional_stability(base_line_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size):
    if -5 <= base_line_angle <= 5 or 2 < word_spacing < 4:
        return 1
    else:
        return 0

def is_neurotic(base_line_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size):
    if -30 <= base_line_angle <= -5:
        return 1
    else:
        return 0

def is_open_to_experience(base_line_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size):
    if (2.5 <= letter_size <= 3 and 0 <= slant_angle <= 30) or (2 < word_spacing < 4) or (3 < line_spacing < 5 or line_spacing >=5):
        return 1
    else:
        return 0

def is_conscientious(base_line_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size):
    if (1.5 <= letter_size <= 2.5 and top_margin < 10) or 2 < word_spacing < 4:
        return 1
    else:
        return 0

def is_agreeable(base_line_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size):
    if (2.5 <= letter_size <= 3 and 0 <= slant_angle <= 30) or 2 < word_spacing < 4 or 3 < line_spacing < 5:
        return 1
    else:
        return 0

if os.path.isfile("lists/final_data.csv"):
    print("Error: final_data already exists.")
    sys.exit(1)  # Explicitly exit the script to halt execution
else:
    if os.path.isfile("lists/clean_data.csv"):
        with open("lists/clean_data.csv", "r") as features_file, open("lists/final_data.csv", "w", newline='') as labels_file:
            features_reader = csv.reader(features_file, delimiter=',')
            labels_writer = csv.writer(labels_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for content in features_reader:
                baseline_angle = float(content[0])
                top_margin = float(content[1])
                line_spacing = float(content[2])  # Assuming this is a string descriptor
                slant_angle = float(content[3])
                word_spacing = float(content[4])  # Assuming this is a string descriptor
                letter_size = float(content[5])
                file_name = content[6]

                trait_1 = is_extroverted(baseline_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size)
                trait_2 = is_introverted(baseline_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size)
                trait_3 = has_emotional_stability(baseline_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size)
                trait_4 = is_neurotic(baseline_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size)
                trait_5 = is_open_to_experience(baseline_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size)
                trait_6 = is_conscientious(baseline_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size)
                trait_7 = is_agreeable(baseline_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size)

                labels_writer.writerow([baseline_angle, top_margin, line_spacing, slant_angle, word_spacing, letter_size,
                                        trait_1, trait_2, trait_3,trait_4, trait_5, trait_6, trait_7, file_name])
        print("Done!")
    else:
        print("Error: clean_data.csv file not found.")
        sys.exit(1)  # Explicitly exit the script to halt execution if the input file is not found

