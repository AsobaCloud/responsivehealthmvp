import re

health_words = ["disease", "disorder", "illness", "condition",
          "health", "medicine", "fitness"]

health_re = re.compile("|".join(health_words))

cond_ids = {
                0: "mental",
                1: "infectious",
                2: "cardiovascular",
                3: "colorectal",
                4: "respiratory",
                5: "injury",
                6: "skin",
                7: "neonatal",
                8: "blood",
                9: "drug",
                10: "cancer",
                11: "others"
            }


not_words = {
            }

in_words = {
                0: re.compile("mental"),
                1: re.compile("infectious"),
                2: re.compile("cardiovascular"),
                3: re.compile("colorectal"),
                4: re.compile("respiratory"),
                5: re.compile("injury"),
                6: re.compile("skin(?!ny)"),
                7: re.compile("neonatal"),
                8: re.compile("blood"),
                9: re.compile("drug"),
                10: re.compile("cancer"),
                11: re.compile(".*") # match anything
            }