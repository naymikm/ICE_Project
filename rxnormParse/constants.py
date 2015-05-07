#!/usr/bin/python
"""
constants.py

Defines the strings used to build regular expressions and parse medication 
strings.

Created by Jorge Herskovic 
Copyright (c) 2011 UTHealth School of Biomedical Informatics. All rights reserved.
"""

# %FORM% will get replaced with each of the known physical forms below to obtain
# the regular expressions that detect administration frequency
# Second element of each tuple indicates frequency per day, or, if -1,
# that the first element is to be treated as a regexp that captures the frequency.
known_times_per_day=[
               ('%FORM% DAILY', 1),
               ('%FORM%S DAILY', 1),
               ('%FORM%S A DAY', 1),
               ('%FORM% TWICE A DAY', 2),
               ('%FORM% TWICE DAILY', 2),
               ('%FORM% THREE TIMES DAILY', 3),
               ('%FORM% THREE TIMES A DAY', 3),
               (r'(\d+) TIME[S]? PER DAY', -1),
               (r'(\d+) TIME[S]? DAILY', -1),
               (r'(\d+) TIME[S]? A DAY', -1),
               ('QD', 1),
               ('Q.D.', 1),
               ('Q.D', 1),
               ('BID', 2),
               ('TID', 3),
               ('QID', 4),
               ('T.I.D.', 3),
               ('T.I.D', 3),               
               ('B.I.D.', 2),
               ('B.I.D', 2),
               ('Q.I.D.', 4),
               ('Q.I.D', 4),
               ('A DAY', 1),
               ('AT NIGHT', 1),
              ]

# Second element of each tuple, if -1, indicates that the first element
# is a regular expression; otherwise, the first element is a literal
# string to be matched.                
known_number_of_doses=[
               (r'TAKE (\d+) %FORM%[S]?', -1),
               ('TAKE %FORM%', 1),
               (r'(\d+) %FORM%[S]?', -1),
              ]

MEDLIST_SEPARATOR="******"
UNDESIRABLE_PUNCTUATION=".,;:!?@#$%^&*()"

# Physical forms extracted from SNOMED-CT and augmented by JRH
physical_forms="""Drop - unit of product usage (qualifier value)
Suppository - unit of product usage (qualifier value)
Puff - unit of product usage (qualifier value)
Base - unit of product usage (qualifier value)
Bottle - unit of product usage (qualifier value)
Box - unit of product usage (qualifier value)
Packet - unit of product usage (qualifier value)
Tube - unit of product usage (qualifier value)
Glassful - unit of product usage (qualifier value)
Inhalation - unit of product usage (qualifier value)
Dropperful - unit of product usage (qualifier value)
Swab - unit of product usage (qualifier value)
Pad - unit of product usage (qualifier value)
Implant - unit of product usage (qualifier value)
Sponge - unit of product usage (qualifier value)
Lozenge - unit of product usage (qualifier value)
Patch - unit of product usage (qualifier value)
Bar - unit of product usage (qualifier value)
Kit - unit of product usage (qualifier value)
Bag - unit of product usage (qualifier value)
Case - unit of product usage (qualifier value)
Spray - unit of product usage (qualifier value)
Blister - unit of product usage (qualifier value)
Sachet - unit of product usage (qualifier value)
Can - unit of product usage (qualifier value)
Pellet - unit of product usage (qualifier value)
Disc - unit of product usage (qualifier value)
Insert - unit of product usage (qualifier value)
Scoop - unit of product usage (qualifier value)
Tablet - unit of product usage (qualifier value)
Cup - unit of product usage (qualifier value)
Application - unit of product usage (qualifier value)
Vial - unit of product usage (qualifier value)
Gum - unit of product usage (qualifier value)
Teaspoonful - unit of product usage (qualifier value)
Tablespoonful - unit of product usage (qualifier value)
Capsule - unit of product usage (qualifier value)
Ampule - unit of product usage (qualifier value)
Tablet delayed release -
Gelcaps -
Gel caps -""".split('\n')
# Extract everything before the hyphen, uppercase it, and strip whitespace
physical_forms=[x.split('-')[0].upper().strip() for x in physical_forms]

abbreviations={'HCL': 'HYDROCHLORIDE'}

# The first three match types imply that *everything* but the drug name matches
# The last match type is more of a wildcard 
MATCH_STRING="Identical strings"
MATCH_COMPOUND="Identical compound (RxNorm)"
MATCH_BRAND_NAME="Brand name and generic"
MATCH_INGREDIENTS="Ingredient lists match"
MATCH_TREATMENT_INTENT="Similar treatment intent"

MEDICATION_FIELDS={"_name":         "DRUG_NAME",
                   "_dose":         "DOSE",
                   "_units":        "UNITS",
                   "_formulation":  "FORMULATION",
                   "_instructions": "SIG",
                   "_norm_dose":    "NORMALIZED_DOSE",
                   }

# 
KNOWN_MATCHING_FIELDS={MATCH_STRING:          [x for x in 
                                               MEDICATION_FIELDS.itervalues()],  
                       MATCH_BRAND_NAME:      [x for x in
                                               MEDICATION_FIELDS.itervalues() 
                                               if x != "DRUG_NAME"],
                       MATCH_INGREDIENTS:     [x for x in 
                                               MEDICATION_FIELDS.itervalues()
                                               if x != "DRUG_NAME"],
                       MATCH_TREATMENT_INTENT: None}

# Test lists of medications
demo_list_1 = """Zoloft 50 MG Tablet;TAKE 1 TABLET DAILY.; RPT
Warfarin Sodium 2.5 MG Tablet;TAKE AS DIRECTED.; Rx
Lipitor 10 MG Tablet;TAKE 1 TABLET DAILY.; Rx
Protonix 40 MG Tablet Delayed Release;TAKE 1 TABLET DAILY.; Rx
Warfarin Sodium 5 MG Tablet;TAKE 1 TABLET DAILY AS DIRECTED.; Rx
Mirapex 0.5 MG Tablet;TAKE 1 TABLET 3 TIMES DAILY.; Rx
Lisinopril 5 MG Tablet;TAKE  TABLET TWICE DAILY; Rx
Coreg 25 MG Tablet;TAKE 1 TABLET TWICE DAILY,  WITH MORNING AND EVENING MEAL; RPT
""".split('\n')
demo_list_2 = """Warfarin Sodium 2.5 MG Tablet;TAKE AS DIRECTED.; Rx
Warfarin Sodium 5 MG Tablet;TAKE 1 TABLET DAILY AS DIRECTED.; Rx
Carvedilol 25 MG Tablet;TAKE 1 TABLET TWICE DAILY,  WITH MORNING AND EVENING MEAL; Rx
Lipitor 10 MG Tablet;TAKE 1 TABLET DAILY.; Rx
Lisinopril 5 MG Tablet;TAKE 1 TABLET TWICE DAILY; Rx
Synthroid 100 MCG Tablet;TAKE 1 TABLET DAILY.; Rx
Pantoprazole Sodium 40 MG Tablet Delayed Release;TAKE 1 TABLET DAILY.; Rx
Sertraline HCl 50 MG Tablet;TAKE 1 TABLET DAILY.; Rx
Mirapex 0.5 MG Tablet;TAKE 1 TABLET 3 TIMES DAILY.; Rx.""".split('\n')