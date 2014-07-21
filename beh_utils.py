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


not_words = {5: re.compile("job")}

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

counts = {0: 12,
          1: 136,
          2: 3,
          3: 2,
          4: 1064,
          5: 12,
          6: 25,
          7: 6,
          8: 10,
          9: 7,
          10: 273210,
          - 1: 6047}
