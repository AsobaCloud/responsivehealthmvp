import re

beh_ids = {
               0: "Weightlifting",
               1: "Yoga",
               2: "Cardio: Low Impact",
               3: "Cardio: High Impact",
               4: "Walking",
               5: "Physical Therapies",
               6: "Vegan",
               7: "Low Carb",
               8: "Gluten-Free",
               9: "Organic Foods",
               10: "Others"
           }

beh_words = [".*"]
beh_re = re.compile("|".join(beh_words))


not_words = {}

in_words = {
                0: re.compile("(?=.*weight)(?=.*lift)"),
                1: re.compile("yoga"),
                2: re.compile("(?=.*cardio)(?=.*low)"),
                3: re.compile("(?=.*cardio)(?=.*high)"),
                4: re.compile("walk"),
                5: re.compile("(?=.*therap)(?=.*physic)"),
                6: re.compile("vegan"),
                7: re.compile("(?=.*carb)(?=.*low)"),
                8: re.compile("(?=.*gluten)(?=.*free)"),
                9: re.compile("(?=.*organic)(?=.*food)"),
                10: re.compile(".*") # match anything
            }