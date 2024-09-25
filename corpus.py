import pandas as pd
import os
from essay import Essay
from scipy.stats import pearsonr
from helper_functions import (get_prompt_and_t,
                              hidden,
                              replace_comma_with_decimal_point)


class Corpus(object):
    """A class used to gather a collection of essays and to analyze this collection."""
    def __init__(self):
        self.essay_path = "data/MEWS/essays"  # leads to original essays
        self.path2MEWSMET = "data/MEWSMET.txt"  # leads to metaphor annotations for MEWS-essays
        self.mewsmet = pd.read_csv(self.path2MEWSMET, sep="\t")
        self.path2metadata = "data/MEWS/MEWSscores.tsv"  # leads to raters' essay scores
        self.metadata = pd.read_csv(self.path2metadata, sep="\t")
        self.list_of_essays = []

    def initiate_essays(self):  # initializes a list of essays, where
        # each essay object contains ID, prompt, T, and the original text

        for directory in os.listdir(self.essay_path):  # directory names refer to prompt and T
            # of essay subgroup: "Ads + T1", "Ads + T2", "Teachers + T1", "Teachers + T2"

            if hidden(directory):
                continue
            else:
                directory_path = self.essay_path + "/" + directory
                for essay_filename in os.listdir(directory_path):
                    if hidden(essay_filename):
                        continue
                    else:
                        essay_path = self.essay_path + "/" + directory + "/" + essay_filename
                        with open(essay_path, mode="r", encoding='utf-8-sig') as e:
                            text = e.read()
                            essay_id = essay_filename[:13]
                            essay = Essay(essay_id)
                            essay.prompt, essay.T = get_prompt_and_t(directory)
                            essay.text = text
                            self.list_of_essays.append(essay)
                            self.list_of_essays = self.list_of_essays

    def add_score2essays(self):  # adds raters' score to each essay object
        t1_score_column = "T1IHS Task score (H:H)"
        t2_score_column = "T2IHS Task score (H:H)"

        for essay in self.list_of_essays:
            id_number_only = essay.id[:6]
            t1 = essay.T == "T1"
            t2 = essay.T == "T2"

            if t1:
                essay_row = self.metadata.loc[self.metadata["Token T1"] == id_number_only]
                score = essay_row[t1_score_column].values[0]
                score = replace_comma_with_decimal_point(score)
                essay.overall_score = score

            elif t2:
                essay_row = self.metadata.loc[self.metadata["Token T2"] == id_number_only]
                score = essay_row[t2_score_column].values[0]
                score = replace_comma_with_decimal_point(score)
                essay.overall_score = score

    def add_metaphors2essays(self):  # counts how many metaphors (TLMs and CMs)
        # the annotators found for each essay and stores numbers in essay object

        for essay in self.list_of_essays:
            rows_essay = self.mewsmet.loc[self.mewsmet['files'] == essay.id]
            num_tlms = 0
            num_cms = 0
            for ind, row in rows_essay.iterrows():
                if row["tlm_labels"] == 1:  # tlms were labelled by both annotators as a L1-metaphor
                    num_tlms += 1
                elif row["tlm_labels"] == 0 and row["all_labels"] == 1:  # the column all metaphors
                    # contains all metaphors where no annotator labelled the instance as incomprehensible and
                    # where at least one annotator labelled the instance as comprehensible only plus all instances
                    # where both annotators labelled the instance as being a L1-metaphor. Those instances that do
                    # not contain a 1 in the column tlm_labels but a one in the column all_labels are therefore cms.
                    num_cms += 1
            essay.number_cm = num_cms
            essay.number_tlm = num_tlms

    def create_corpus(self):  # creates corpus of essay objects containing ID,
        # prompt, T, text, score, and number of CMs and TLMs

        self.initiate_essays()
        self.add_score2essays()
        self.add_metaphors2essays()

    def calculate_correlation(self):  # calculates correlation between
        # the raters' score and the number of CMs/TLMs/all metaphors

        list_tlms = []
        list_cms = []
        list_allmets = []
        list_score = []
        for essay in self.list_of_essays:
            essay_len = len(essay.text)  # number of TLMs and CMs is divided by
            # number of each essay's characters in order to control for essay length
            list_tlms.append(essay.number_tlm/essay_len)
            list_cms.append(essay.number_cm/essay_len)
            list_allmets.append((essay.number_tlm + essay.number_cm)/essay_len)
            list_score.append(essay.overall_score)

        list_score = [float(e) for e in list_score]

        print("Pearson's correlation for tlm/score:\t", pearsonr(list_score, list_tlms))
        print("Pearson's correlation for cm/score:\t", pearsonr(list_score, list_cms))
        print("Pearson's correlation for allmets/score:\t", pearsonr(list_score, list_allmets))
        print("The number of metaphors is divided by characters in order to control for essay length.")

    def __str__(self):
        final_str = ""
        for essay in self.list_of_essays:
            final_str += str(essay) + "\n"
        return final_str


if __name__ == "__main__":
    c = Corpus()
    c.create_corpus()
    c.calculate_correlation()
