import pandas as pd
import os
from essay import Essay
from scipy.stats import pearsonr


def get_prompt_and_t(name):
    prompt = ""
    t = ""
    if name.endswith("1") or name.endswith("2"):
        prompt = "TV_Ads"
        t = "T1"
    elif name.endswith("3") or name.endswith("4"):
        prompt = "Teachers"
        t = "T1"
    elif name.endswith("5") or name.endswith("6"):
        prompt = "TV_Ads"
        t = "T2"
    elif name.endswith("7") or name.endswith("8"):
        prompt = "Teachers"
        t = "T2"
    return prompt, t


class Corpus(object):
    def __init__(self):
        self.essay_path = "data/MEWS/essays"
        self.path2MEWSMET = "data/MEWSMET.txt"
        self.mewsmet = pd.read_csv(self.path2MEWSMET, sep="\t")
        self.path2metadata = "data/MEWS/MEWSscores.tsv"
        self.metadata = pd.read_csv(self.path2metadata, sep="\t")
        self.list_of_essays = []
        self.list_of_ids = []

    def initiate_essays(self):
        for name in os.listdir(self.essay_path):
            if name.startswith("."):
                continue
            else:
                for essay_filename in os.listdir(self.essay_path + "/" + name):
                    if essay_filename.startswith("."):
                        continue
                    else:
                        with open(self.essay_path + "/" + name + "/" + essay_filename) as e:
                            text = e.read()
                            essay_id = essay_filename[:13]
                            essay = Essay(essay_id)
                            essay.prompt, essay.T = get_prompt_and_t(name)
                            essay.text = text
                            self.list_of_essays.append(essay)

    def add_score2essays(self):
        t1_score_column = "T1IHS Task score (H:H)"
        t2_score_column = "T2IHS Task score (H:H)"

        for essay in self.list_of_essays:
            id_num_only = essay.id[:6]
            if essay.T == "T1":
                row = self.metadata.loc[self.metadata["Token T1"] == id_num_only]
                score = row[t1_score_column].values[0]
                if "," in score:
                    score = score[0] + "." + score[2]
                essay.overall_score = score
            elif essay.T == "T2":
                row = self.metadata.loc[self.metadata["Token T2"] == id_num_only]
                score = row[t2_score_column].values[0]
                if "," in score:
                    score = score[0] + "." + score[2]
                essay.overall_score = score

    def add_metaphors2essays(self):
        for essay in self.list_of_essays:
            rows_essay = self.mewsmet.loc[self.mewsmet['files'] == essay.id]
            num_tlms = 0
            num_cms = 0
            for ind, row in rows_essay.iterrows():
                if row["tlm_labels"] == 1:
                    num_tlms += 1
                elif row["tlm_labels"] == 0 and row["all_labels"] == 1:
                    num_cms += 1
            essay.number_cm = num_cms
            essay.number_tlm = num_tlms

    def create_corpus(self):
        self.initiate_essays()
        self.add_score2essays()
        self.add_metaphors2essays()

    def calculate_correlation(self):
        list_tlms = []
        list_cms = []
        list_allmets = []
        list_score = []
        for essay in self.list_of_essays:
            essay_len = len(essay.text)
            list_tlms.append(essay.number_tlm/essay_len)
            list_cms.append(essay.number_cm/essay_len)
            list_allmets.append((essay.number_tlm + essay.number_cm)/essay_len)
            list_score.append(essay.overall_score)

        list_score = [float(e) for e in list_score]
        print("Pearson's correlation for tlm/score:\t", pearsonr(list_score, list_tlms))
        print("Pearson's correlation for cm/score:\t", pearsonr(list_score, list_cms))
        print("Pearson's correlation for allmets/score:\t", pearsonr(list_score, list_allmets))
        print("The number of metaphors is divided by characters in order to control for essay length.")


c = Corpus()
c.create_corpus()
c.calculate_correlation()
