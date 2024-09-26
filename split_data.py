"""This file divides the data into two splits, one that is based
on the prompt "TV-Ads" and one which is based on the prompt "Teacher".
Then the data is preprocessed to meet the requirements of DeepMet."""

from nltk import word_tokenize, pos_tag
import pandas as pd
import os


def split_data():  # splits data into essays
    # based on ads- and teacher-prompts (we use these splits
    # for training and testing)

    path2mewsmet = "data/MEWSMET.txt"
    mewsmet = pd.read_csv(path2mewsmet, sep="\t")

    # filter rows for prompt "TV-Ads":
    ads_dataframe = mewsmet[mewsmet["files"].str.contains('AD')]
    # filter rows for prompt "Teachers":
    teachers_dataframe = mewsmet[mewsmet["files"].str.contains('TE')]

    return ads_dataframe, teachers_dataframe


def get_all_local_contexts(tagged_tokens):  # this function creates all
    # local contexts that occur in a sentence (all words that are
    # contained within two items of punctuation or the start of the
    # sentence and one item of punctuation)
    punctuation = [",", ":", ";"]
    all_loc_cont = []  # list to store all local contexts
    loc_cont = []  # temporary list to store current local contexts

    for token in tagged_tokens:
        token_string = token[0]
        if token_string in punctuation:  # if punctuation is detected,
            # wrap up local context
            all_loc_cont.append(" ".join(loc_cont))
            loc_cont = []  # reset current local context

        else:  # as long as no punctuation is detected,
            # collect tokens for current local contex
            loc_cont.append(token_string)

    all_loc_cont.append(" ".join(loc_cont))  # add the last local context
    return all_loc_cont


class DeepmetDocCreator(object):
    def __init__(self, df, prompt):
        # initialize with DataFrame and prompt type:
        self.df = df
        self.prompt = prompt

        self.essay_id = []
        self.sentences = []
        self.target_words = []
        self.tlms = []
        self.all_mets = []
        self.poss = []
        self.tags = []
        self.locals = []
        self.df_preprocessed = pd.DataFrame

    def get_tag_and_local(self, sentence, target_word, processed_words):  # this method
        # determines the POS-tag of the target verb (see below) as well as the local
        # context of the target verb ()

        # pos_tags_verb = ["VB", "VBD", "VBG", "VBP", "VBZ", "VBN"]  # "VB": base form, "VBD": past tense,
        # "VBG": gerund or present participle, "VBP": non-3rd-sg-present, "VBN": past participle,
        # "VBZ": 3rd-sg-present

        punctuation = [",", ":", ";"]

        list_of_tokens = word_tokenize(sentence)
        tagged = pos_tag(list_of_tokens)
        local_contexts = get_all_local_contexts(tagged)
        index_local_contexts = 0  # keep track of current local context

        for word_pos_tuple in tagged:
            pos = word_pos_tuple[1]
            word = word_pos_tuple[0]
            if word.strip() == target_word.strip():
                if word in processed_words:  # this makes sure target words that
                    # occur multiple times obtain the correct POS-tag and local context
                    processed_words.remove(word)
                    continue
                else:
                    pos_name = pos
                    context = local_contexts[index_local_contexts]
                    self.tags.append(pos_name)  # add POS-tag to class attribute
                    self.locals.append(context)  # add local context class attribute
            elif word in punctuation:  # move to next local context
                index_local_contexts += 1

    def preprocess(self):
        current_sentence = ""
        processed_verbs = []
        for index, row in self.df.iterrows():
            # collect instance properties from MEWSMET.txt
            id_file = row["files"]
            self.essay_id.append(id_file)
            sentence = row["sents"]
            self.sentences.append(sentence)
            target_word = row["target_verbs"]
            self.target_words.append(target_word)
            tlm = row["tlm_labels"]
            self.tlms.append(tlm)
            all_mets = row["all_labels"]
            self.all_mets.append(all_mets)
            self.poss.append("VERB")  # all our target verbs are verbs

            # get local context and the POS-tag:
            if current_sentence != sentence:  # make sure that processed words from
                # previous sentence are not taken into account for current sentence
                current_sentence = sentence
                processed_verbs = []  # track processed words in order to account
                # for multiple occurences of same target verb within a sentence

            # get POS-tag and local context:
            self.get_tag_and_local(sentence, target_word, processed_verbs)
            processed_verbs.append(target_word)

        dict_deepmet = {"id": self.essay_id, "sents": self.sentences,
                        "target_word": self.target_words, "tlms": self.tlms,
                        "all_mets": self.all_mets, "pos": self.poss,
                        "tag": self.tags, "local": self.locals
                        }

        # create dataframe:
        self.df_preprocessed = pd.DataFrame.from_dict(dict_deepmet)

    def save_dfs2targetdir(self):

        # make directory for preprocessed dataframes:
        os.mkdir("mewsmet4deepmet")
        target_directory = "mewsmet4deepmet"

        # preprocess data:
        self.preprocess()

        # save preprocessed data:
        if self.prompt == "TV-Ads":
            self.df_preprocessed.to_csv(target_directory + "/ads.txt", sep="\t")
        else:
            self.df_preprocessed.to_csv(target_directory + "/teachers.txt", sep="\t")


if __name__ == "__main__":
    # split data into split "TV-Ads" and split "Teachers":
    df_ads, df_teachers = split_data()

    # preprocess and save split "TV-Ads":
    ads = DeepmetDocCreator(df_ads, "TV-Ads")
    ads.save_dfs2targetdir()

    # preprocess and save split "Teachers":
    teachers = DeepmetDocCreator(df_teachers, "Teachers")
    teachers.save_dfs2targetdir()
