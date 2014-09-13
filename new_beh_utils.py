import re

beh_ids = {
               0: "Frequent Exercise",
               1: "Good Diet",
               2: "Bad Diet",
               3: "Alcohol",
               4: "Lack of Sleep",
               5: "Smoking",
               6: "Negative Mental State",
               7: "Others",
           }

beh_words = [".*"]
beh_re = re.compile("|".join(beh_words))


not_words = {}

in_words = {
                0: re.compile("running|swimming|walking|((?=.*weight)(?=.*lifting))|crossfit|swimming|zumba|yoga|soccer|football|fitness"),
                1: re.compile("vegan|((?=.*gluten)(?=.*free))|((?=.*low)(?=.*carb))|fruit|vegetable|veggies|diet|((?=.*good)(?=.*food))|foodie"),
                2: re.compile("candy|donut|piza|soda|cake|((?=.*fast)(?=.*food))|burger|((?=.*junk)(?=.*food))"),
                3: re.compile("beer|drinking|drunk|party|drugs|((?=.*jim)(?=.*beam))|pimms|vodka|bourbon|whiskey|scotch"),
                4: re.compile("exhausted|so tired|stressed|((?=.*sleep)(?=.*deprived))|need sleep|cant sleep"),
                5: re.compile("tobacco|smoking"),
                6: re.compile("depressed|alone|stressed|suicidal|sad|crying|unhappy|lonely|((?=.*self)(?=.*harm))|angry"),
                7: re.compile(".*") # match anything
            }