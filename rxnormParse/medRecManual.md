###README.md

#MedRec v0.04

This is Dr. Herskovic's medication reconciliation algorithm. It takes two lists
of medications and returns three lists: a reconciled list, the part of list 1
that could not be reconciled, and the part of list 2 that could not be reconciled.

This implementation requires RXNorm, which is part of the UMLS. You can extract
RXNorm from the UMLS to use with this program by using the included
generate_rxnorm_file.py script. You must have an RRF version of the UMLS to use
this script. Invoke it as:

    python generate_rxnorm_file.py /path/to/umls/metathesaurus rxnorm.pickle.bz2

As of the end of 2013, the UMLS is large enough that generating the RxNorm
dictionaries crashes the Python DBM implementation used internally by the shelve
module. I switched generation to build shelves "manually" (i.e. they can still be
read correctly by the native shelve module) by using a different DBM provider,
semidbm (a highly-performant pure Python implementation).

    pip install semidbm
should be enough to set you up correctly.

It also requires a treatment database in a pickled bz2 file. You may ignore this
file, and treatment intent reconciliation will be skipped. If you want to
provide one, it should be a pickle dictionary of the form

    {'CUI_of_drug': set(['CUI_of_condition', 'CUI_of_another_condition', etc.])}

I apologize in advance, but I can not share the dataset we used to create our
own copy of the treatment file, nor the treatment file itself. The algorithm
will still work without it.

After you have your rxnorm pickled file, please try out:

    python reconcile.py
to perform a demo reconciliation.

I also included the SMARTApp version of the reconciliation algorithm. You will
need Josh Mandel's smart client modules, available from
https://github.com/chb/smart_client_python and placed in the smart_client
subdirectory (and, of course, all its dependencies). Try:

    python reconcile_smart.py 8000
and run it inside the SMART sandbox to play with it.

Our original evaluation of this algorithm was published in the Proceedings of
the AMIA Symposium:
Bozzo Silva PA, Bernstam EV, Markowitz E, Johnson TR, Zhang J, Herskovic JR.
Automated medication reconciliation and complexity of care transitions.
Proc AMIA Ann Symp 2011.

----
Basic documentation of the output format:

The JSON output contains 5 key-value pairs: original_list_1, original_list_2, new_list_1, new_list_2, and reconciled.

* original_list_1 and 2 echo the input to the program.
* reconciled contains the merged list.
* new_list_1 and new_list_2 contain the items from original_list_1 and 2 that could not be reconciled.

The reconciled list is a list of key-value pair stores. Each item in the list has at least four key-value pairs:
med1, score, identical, and mechanism.

mechanism describes the way in which medications were merged (if they were identical, or their ingredients matched, etc.)
identical contains a refinement of mechanism, and specifies which fields matched between two drugs.
score gives the quality of the match (between 0 and 1, with 1 being complete certainty)
med1 contains a single medication. If mechanism is not "identical", there will be a med2 as well; if mechanism is "identical", you can assume that the second medication was identical to the first one, and is therefore not provided.

* med1 contains:
    * id: This is a sequential id generated arbitrarily by the software that uniquely identifies a medication from its input. Every medication the program sees in a single run has a different id; ids *will* repeat between runs.
    * medication_name: This is the medication's name.
    * dose:            The medication's dose (i.e. 100)
    * units:           The units of the medication's dose (i.e. mg)
    * formulation:     The physical format of the medication (tablet, capsule, etc)
    * instructions:    Whatever free-form instructions were provided for the medication.
    * original_string: The original input string
    * provenance:      Whatever provenance was specified in the input
    * normalized_dose: The dose in a normalized format for a day ("W X*Y*Z", W being dose of an individual unit, X being units, Y being the number of times per day (i.e. frequency), and Z is the number of units to be delivered simultaneously. So, for example, 2 500 mg Aspirin tid becomes 500 mg*3*2)
    * frequency:       The number of times per day the drug is administered.

Route is currently not available.

med2 is obviously the same as med1.
