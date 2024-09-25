"""These helper functions are needed for the class Corpus."""


def get_prompt_and_t(filename):  # filenames reveal whether
    # the essays were written at beginning (T1) or end
    # of schoolyear (T2) and which prompt the students
    # were given.

    prompt = ""
    t = ""
    if filename.endswith("1"):
        t = "T1"
    elif filename.endswith("2"):
        t = "T2"
    if "ads" in filename:
        prompt = "TV_Ads"
    elif "teachers" in filename:
        prompt = "Teachers"
    return prompt, t

def hidden(path):  # checks if file or directory is a hidden file
    hidden_file = path.startswith(".")
    return hidden_file

def replace_comma_with_decimal_point(score):  # turns comma into decimal point
    if "," in score:
        score = score[0] + "." + score[2]
    return score
