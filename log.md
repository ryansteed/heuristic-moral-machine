# Project Log File

## 10 Jan 20

Looking for data! Goal: load up a sample dataset of binary survey responses in a Jupyter/R env

## 13 Jan 20

## Snorkel questions?
A standing question: how to prove that this method works?? Namely, how to prove it achieves as moral results as a massive survey?
> Snorkel simply evaluates F1 accuracy in comparison to hand labels for a supervised case - this is equivalent to comparing accuracy on MM data or kidney MTurk data
> Demonstrating efficiency (time/cost taken to achieve performance) will probably be more circumspect
> Easy to say that this method achieves the same for much less cost; harder to say that this method produces more moral outcomes

Label-generator can be used to train another classifier - but isn't it a classifier itself? What's the distinction?
> Per Snorkel paper, generative model produces a linear combo of labeling fxns; discriminative model generalizes beyond the combo to handle unseen data (somehow).
> Also betting on these technologies to improve - make something that works for any model with a standard loss function, and performance will increase with discriminative techniques
> For use cases (text modalities and medical imaging), used LSTM and ResNet respectively

Why bother with the generative model at all? Why not feed labeling functions directly?
> There is some performance improvement with the generative model - will need to demonstrate this

Why not just aggregate expert votes?
> Takes too long to accumulate a suitably sized dataset

**A note - the generative model may be super simple for such a low-dimensional problem - really, the issue is fairly combining the labeling functions (by removing correlations, double counting) - focus more on this**

Each labeling function is a noisy, independent voter (i.i.d.?)

Works best with 10-100 labeling functions?

Choice of epsilon matters (selection threshold for which dependencies to include in generative model)

**How simple should labeling functions be?**

What are some other Snorkel capabilities that might be useful? Check out the website
> - Distant supervision?

What are differences between Snorkel and this model?
> - Snorkel typically uses real-world training data - the training data for MM is made up (though kidney exchange might not be)

### Heilmeier's Catechism
- What are you trying to do? Articulate your objectives using absolutely no jargon.
> Build an algorithm/model to make moral decisions (in self-driving cars, in kidney exchange)
- How is it done today, and what are the limits of current practice?
> Survey data! MIT Moral Machine, Amazon Turk. Then use a computational social choice model or classifier to fairly aggregate conflicting responses.
- What is new in your approach and why do you think it will be successful?
> My approach surveys a few experts instead of a lot of the general public, and asks for decision-making heuristics instead of actual answers.
- Who cares? If you are successful, what difference will it make?
> + Will make moral machines cheaper
> + Will make moral machines work in complicated domains
> + Will make it possible to teach machines institutional morals (legal, cultural) directly
> + Will make moral inputs more transparent
- What are the risks?
> + De-democratize moral decision-making - experts may be missing something valuable
> + SME expertise may not compensate for lower sample size
> + Labeling function may have less coverage than direct surveying - maybe people's heuristics differ from their actual behavior (do we trust experts to not have this quirk?)
> + May be impossible to prove if this is working - how to prove labeling functions are honored?
> + The requirements for being an SME labeler exclude certain groups from being able to provide input: The profile of the best performing user by F1 score was a MS or Ph.D. degree in any field, strong Python coding skills, and intermediate to advanced experience with machine learning (Snorkel). How to make this accessible to lower-educated, non Python coders?
- How much will it cost?
> + Time
> + Data costs??
- How long will it take?
> + A long time... prototype done for thesis hopefuly
- What are the mid-term and final “exams” to check for success?
> + Midterm exam: Does this method functionally work? Are moral decisions comparable to existing methods?
> + Final exam: Is this method better than existing methods? How to prove this?

### Learning MM data struct
No published data description... working backwards from figures in [paper](https://www.mendeley.com/viewer/?fileId=3b917119-bbe5-3ee3-7969-b7991da2abf7&documentId=f71b5d60-0d88-323a-a078-960daa3a63c5) using code from [repo](https://osf.io/3hvt2/files/?view_only=4bb49492edee4a8eb1758552a362a2cf)

<!-- - Run through Heilmeier Catechism -->
<!-- - Read remaining papers -->
    <!-- + Answer Snorkel questions -->

## 14 Jan 20
Sent an email to Edmond asking for field descriptions...

Next step: run the R scripts for producing the figures to see if that helps at all

Figure 2 especially - should be able to develop the labeling functions from that code

### Possible Values for SharedResponses.csv
ResponseID
['2222bRQqBTZ6dLnPH' '2222sJk4DcoqXXi98' '2223CNmvTr2Coj4wp' ...
 '22BSSc45dijDan7fD' '22BSb5vzyoeu2csFZ' '22BSp55p9c9LGeibw']
ExtendedSessionID
['32757157_6999801415950060.0' '1043988516_3525281295.0'
 '-1613944085_422160228641876.0' ... '1703715954_8686429570804792.0'
 '-2057390477_171517308543305.0' '-610773260_4701943483744748.0']
UserID
[6.99980142e+15 3.52528130e+09 4.22160229e+14 ... 8.68642957e+15
 1.71517309e+14 4.70194348e+15]
ScenarioOrder
[ 7  2 10 11  8  6 12  3  4  1  5 13  9]
Intervention
[0]
PedPed
[0 1]
Barrier
[0 1]
CrossingSignal
[1 0 2]
AttributeLevel
['Fit' 'Rand' 'Female' 'Old' 'More' 'Low' 'Hoomans' 'Less' 'Male' 'Pets'
 'Fat' 'Young' 'High']
ScenarioTypeStrict
['Fitness' 'Random' 'Gender' 'Age' 'Utilitarian' 'Social Status' 'Species']
ScenarioType
['Fitness' 'Random' 'Gender' 'Age' 'Utilitarian' 'Social Status' 'Species']
DefaultChoice
['Fit' nan 'Male' 'Young' 'More' 'High' 'Hoomans']
NonDefaultChoice
['Fat' nan 'Female' 'Old' 'Less' 'Low' 'Pets']
DefaultChoiceIsOmission
[ 1. nan  0.]
NumberOfCharacters
[5 1 4 2 3]
DiffNumberOFCharacters
[0 2 1 4 3]
Saved
[1 0]
Template
['Desktop' 'Mobile' nan]
DescriptionShown
[ 1.  0. nan]
LeftHand
[ 1.  0. nan]
UserCountry3
['USA' 'BEL' 'ISR' 'MEX' 'CHE' 'RUS' 'TUR' 'CAN' 'DEU' 'SAU' 'GBR' 'PHL'
 'AUT' nan 'BRA' 'EGY' 'ITA' 'FRA' 'ARG' 'IDN' 'ESP' 'IND' 'UKR' 'JPN'
 'PAN' 'LTU' 'SGP' 'PRT' 'HUN' 'FIN' 'POL' 'CHL' 'AUS' 'SWE' 'SVN' 'NLD'
 'TWN' 'ABW' 'NZL' 'VEN' 'GRC' 'CZE' 'CHN' 'SVK' 'BGR' 'AZE' 'ROU' 'VNM'
 'LVA' 'LUX' 'MKD' 'NOR' 'HKG' 'ZAF' 'DNK' 'IRN' 'MYS' 'HND' 'GUM' 'COL'
 'MAR' 'SRB' 'GTM' 'IRL' 'BGD' 'KOR' 'PRY' 'HRV' 'KAZ' 'PER' 'BLR' 'PAK'
 'PSE' 'THA' 'ARE' 'GEO' 'CRI' 'LKA' 'EST' 'URY' 'JEY' 'JOR' 'DZA' 'NPL'
 'GIB' 'MNP']
Man
[1 0 2 3]
Woman
[1 0 2 3 4]
Pregnant
[0 1 2 3]
Stroller
[0 1 2]
OldMan
[0 2 1 3 4]
OldWoman
[0 3 1 2 4]
Boy
[0 1 3 2 4]
Girl
[0 1 2 3 4]
Homeless
[0 2 1 3 4 5]
LargeWoman
[0 1 3 2 4]
LargeMan
[0 1 2 3]
Criminal
[0 1 2]
MaleExecutive
[0 1 2 3]
FemaleExecutive
[0 1 2 3]
FemaleAthlete
[1 0 2 3 4]
MaleAthlete
[2 0 1 3 5 4]
FemaleDoctor
[0 1 2]
MaleDoctor
[0 1 2 3]
Dog
[0 1 2 4 3 5]
Cat
[0 1 3 2 4 5]

---

starting to think intervention might be the target; sorted by whether intervened or not

looks like only 1 of 13 sessions was totally randomized - so what data was Noothigattu using?

New theory - each row is one card, and `Saved` is whether that card was chosen; but how to tell which cards were being compared? no obvious session ID or pointer

but it seems impossible that each card has its own row! since each row seems like it should be the answer! only possible answer is that they didn't include the other alternative in the data? or not?

need to find an example where it would have been necessary for the coders to know both alternatives at once

maybe this information isn't available... did Noothigattu use this? is it necessary to know? for labeling functions it is...

Ending with: the answer must lie in Noothigattu's paper... if necessary, contact him (did he ever actually use pairwise alternative comparisons - or am I misunderstanding?)

- Figure out what MM fields mean
    <!-- + Get all possible values for each field -->
        <!-- * Try first on SharedResponses -->
        <!-- * Then compare to SharedResponsesFullFirstSession -->
    <!-- ~ Try to view just one user, one session, all 13 pairwise choices for a randomized session -->

## 15 Jan 20

Received a response - no help, but answered a single question
Might be able to ask again if desperate

Central problem: I think the MM study could have been conducted without knowing the alternatives as pairs - but how could the Noothigattu study have been conducted?

BREAKTHROUGH: random sample works for finding repeated response IDs, passes the eye test

### SQLite implementation
Now creating a SQL table to hold all data to make querying faster:
```
sqlite> .mode csv
sqlite> .import /Users/steed/heuristic-moral-machine/data/moralmachine/SharedResponses.csv sharedresponses
```

Double checking no data loss/gain
Originally 70332356 lines, including header
SQLLite reports 70332355
Perfect!

Used https://www.sqlitetutorial.net/sqlite-import-csv/


Fixing the schema using https://www.sqlite.org/lang_altertable.html

CREATE TABLE sharedresponses_strict(ResponseID TEXT, ExtendedSessionID TEXT, UserID TEXT, ScenarioOrder INT, Intervention INT, PedPed INT, Barrier INT, CrossingSignal INT, AttributeLevel TEXT, ScenarioTypeStrict TEXT, ScenarioType TEXT, DefaultChoice TEXT, NonDefaultChoice TEXT, DefaultChoiceIsOmission INT, NumberOfCharacters INT, DiffNumberOFCharacters INT, Saved INT, Template TEXT, DescriptionShown INT, LeftHand INT, UserCountry3 TEXT, Man INT, Woman INT, Pregnant INT, Stroller INT, OldMan INT, OldWoman INT, Boy INT, Girl INT, Homeless INT, LargeWoman INT, LargeMan INT, Criminal INT, MaleExecutive INT, FemaleExecutive INT, FemaleAthlete INT, MaleAthlete INT, FemaleDoctor INT, MaleDoctor INT, Dog INT, Cat INT);

Still reports COUNT 70332355

<!-- - Figure out what MM fields mean -->
    <!-- + Try to find common session/response IDs - this is the most likely matching element (does the negative sign mean something?) -->
    <!-- + Try loading a random sample of the entire dataset - maybe responses are scattered so much that the common IDs can't be found - best way would be to host an SQL db (SQLAlchemy, perhaps - to integrate with Snorkel) -->
<!-- ~ Transition data to SQLLite for easier querying -->
    <!-- + Create indices -->

## 16 Jan 19

Starting to see some problems:
- There aren't enough heuristic functions to write here! This example is too simplistic (there aren't enough features to write sophisticated heuristics).
  + UPDATE 20 Jan 20 - this problem is mostly solved
- Even if I get some experts to give me heuristics, they'll 1) be simple, 2) be too if- based and have high coverage (more rules-based), 3) be hard to compare to Noothigattu because so different than the MM audience

Things we might still be able to demonstrate:
- Ability of machine learning approach to generalize beyond experts' heuristics - provide a limited set of heuristics, then still achieve comparable performance.
- A good goal: create some example where similar effect sizes to MM arise. A good strategy might be modeling several ethical camps and writing competing heuristic functions from the perspective of experts from these camps.

Log:
Managed to write some labeling functions! and did some preliminary analysis
Using https://www.snorkel.org/use-cases/01-spam-tutorial#4-combining-labeling-function-outputs-with-the-label-model

- Create a working example with Snorkel
    <!-- + Figure out how to SQL query the responses in pairs - debugging -->

## 17 Jan 20
Index(['ExtendedSessionID', 'UserID', 'ScenarioOrder', 'Intervention',
       'PedPed', 'CrossingSignal', 'AttributeLevel', 'ScenarioTypeStrict',
       'ScenarioType', 'DefaultChoice', 'NonDefaultChoice',
       'DefaultChoiceIsOmission', 'Template', 'UserCountry3', 'Barrier_int',
       'NumberOfCharacters_int', 'DiffNumberOFCharacters_int',
       'DescriptionShown_int', 'LeftHand_int', 'Man_int', 'Woman_int',
       'Pregnant_int', 'Stroller_int', 'OldMan_int', 'OldWoman_int', 'Boy_int',
       'Girl_int', 'Homeless_int', 'LargeWoman_int', 'LargeMan_int',
       'Criminal_int', 'MaleExecutive_int', 'FemaleExecutive_int',
       'FemaleAthlete_int', 'MaleAthlete_int', 'FemaleDoctor_int',
       'MaleDoctor_int', 'Dog_int', 'Cat_int', 'Barrier_noint',
       'NumberOfCharacters_noint', 'DiffNumberOFCharacters_noint',
       'DescriptionShown_noint', 'LeftHand_noint', 'Man_noint', 'Woman_noint',
       'Pregnant_noint', 'Stroller_noint', 'OldMan_noint', 'OldWoman_noint',
       'Boy_noint', 'Girl_noint', 'Homeless_noint', 'LargeWoman_noint',
       'LargeMan_noint', 'Criminal_noint', 'MaleExecutive_noint',
       'FemaleExecutive_noint', 'FemaleAthlete_noint', 'MaleAthlete_noint',
       'FemaleDoctor_noint', 'MaleDoctor_noint', 'Dog_noint', 'Cat_noint'],
      dtype='object')


Do the labeling functions have to be mostly accurate??? Hopefully not...

<!-- + Draft some labeling functions from the effect sizes in the MM paper (highlighted in purple in Mendeley - https://www.mendeley.com/viewer/?fileId=3b917119-bbe5-3ee3-7969-b7991da2abf7&documentId=f71b5d60-0d88-323a-a078-960daa3a63c5) -->
    <!-- * Heuristic to save most lives -->
    <!-- * Heuristics to spare the four most spared characters: baby, little girl, little boy, pregnant woman -->
    <!-- * Heuristic to save most *human* lives -->
    <!-- * Heuristics to prefer: -->
        <!-- - inaction -->
        <!-- - pedestrians -->
        <!-- - females -->
        <!-- - the fit -->
        <!-- - rich -->
        <!-- - lawful (crossing-wise) -->
        <!-- - young -->
    <!-- * Heuristics not to prefer: -->
        <!-- - criminals -->
        <!-- - homeless -->
        <!-- - Pets -->


## 19 Jan 20

    <!-- ~ Debug labeling functions - write unit tests -->
    <!-- + Continue with Snorkel analysis example - https://www.snorkel.org/use-cases/01-spam-tutorial#4-combining-labeling-function-outputs-with-the-label-model -->
        <!-- * Finish the labeler (generative model) - get single label for whole test set -->

## 20 Jan 20

### Noothigattu deep dive
From [MIT Media Lab](https://www.media.mit.edu/projects/a-voting-based-system-for-ethical-decision-making/overview/):
> Our proof of concept shows that the decision the system takes is likely to be the same as if we could go to each of the 1.3 million voters, ask for their opinions, and then aggregate their opinions into a choice that satisfies mathematical notions of social justice. 

How do they prove this in the paper?
By proving that theoretically their system matches a monotonic SCC (i.a. Borda or Copeland)
By showing that their system achieves enormously high accuracy on 3000 test instances (is this a function of high N, though?)

One possible explanation for high accuracy: Noothigattu achieves astronomical accuracy by increasing number of pairwise comparisons per voter (equivalently, decreasing number of voters) - try filtering for high response voters in the query (if necessary, create the same synthetic data as in Noothigattu) - though in their final analysis, they used all 1.3 million voters

<!-- ! Obtain kidney exchange data -->
<!-- - Prep for Williams meet -->
- Create a working example with Snorkel
    <!-- + Train a simple ML model on outputted labels and test final performance! -->

## 21 Jan 20

### Williams meet
- Run through Heilmeier's catechism, roughly.
- Lay out methods/results so far
  + Obtained MoralMachine data - pairwise alternatives
  + Wrote labeling functions
  + Built label aggregator - got labels, aggregated
    * Labeling model 66.9% accurate when compared with human voters
  + Built machine learning model on top of regular data, label aggregator, compared performance
    * 90% accuracy with ML model trained on gold labels
    * 66.7% accuracy with ML model trained on label model
- Some concerns:
  + The measurement problem
    * How to empirically prove this method is better? Is that necessary?
      - How does Noothigattu do it? mainly, estimate accuracy (extremely high @ 98% - is this what I think it is?); also use a synthetic data approach to measure accuracy loss as a result of summarization
      - Snorkel does it just by comparing accuracy/f1 score to hand labeled data - we've done that already
      - Easy to say that this method achieves the same for much less cost; harder to say that this method produces more moral outcomes
  + The case study
    * Inherently problematic representation - disputed usefulness
    * Too simple?? Snorkel usually works more dramatically with text data, 
- Lay out future steps
  + Figure out how to prove supermorality
  + Same methods, kidney exchange use case - almost better because respondents included their rationales
  + Survey of real experts for a use case

<!-- Ryan> Send Williams the papers -->

Is there a way to prove if this is more extensible (more generalizable) to zero-shot scenarios?
Extrapolate beyond statistical value of life? For instance, regular ML model would value 100 y/o's less than heuristic model

Use case where expert demographic problem might not be such an issue: e.g. decision-making by doctors

Seems like this approach inherently easier to sell for scenarios where lots of expertise required (e.g. medical)

## 22 Jan 20

N.B. increasing sample size by an order of magnitude increases average pairwise comparisons per voter by .16

Found a bug with joining - had dupes

Another bug - there are two seperate crossing signals, one for each in ped v. ped

Things to measure (outputs):
- MajorityLabelVoter() acc vs LabelModel() acc
- LabelModel() weights

Things to vary (inputs):
- LF inclusion
- Model
- Model parameters
- Data content
- Label threshold

### Paper outline
- Heilmeier's catechism
- Here is a new method
  + Make it clear we are not trying to represent voter's responses - this is an alternate method
- MM use case
  + We tried creating labeling functions based on MM results (as if regular people were the experts)
  + Here's how the label functions performed relative to real users, and here's how much less it cost
    * How well does it agree on random scenarios? on all scenarios?
  + When does this method disagree and why?
- Kidney use case
  + Same thing, but this time users explicitly told us their rationales; let's pretend they're trained experts
  + Now how do the results compare?
  + When does this method disagree and why?
- Discuss benefits
  + Cost - as demonstrated by comparability
  + Zero-shot applications - theoretical argument about info gain from heuristics
  + For highly complex scenarios when gathering training data is literally not feasible
- Discuss drawbacks
  + Barriers to entry (education)
  + Demographic problem (smaller sample, less representative demographically) - experts must be proxies for larger populations
  + Inherently problematic case studies - e.g. still limited by choice of representation of ethical dilemmas
  + Succintly, moral machine is deliberately simplified
- Mirror weak supervision trade-offs section of Snorkel paper

## 23 Jan 20
Found new paper by Awad et al. from MM website - Switch-Loop-Footbridge preference
Here, really just one variable of interest; not good for our use case
https://www.mendeley.com/viewer/?fileId=732291c7-0367-658b-5676-1f0cceb766c3&documentId=e78041ab-0432-3e5e-84dd-3f47bd64edd7

### Model Label vs. Voter Label Analysis
Some observations about model errors

First, taking off "random" type restriction - all scenarios allowed

In small sample (100000) scraped, one FP:
> What should the self-driving car do?
> 
>       🚘 
>      |  \ 
>      v   v
>   🔴🚸  🚧 
>    NOINT  INT 
> INT saves: 
> ['Man', 'OldWoman']
> NOINT saves: 
> ['Homeless', 'Homeless']

On the other hand, 10 FNs (many more false negatives - need to raise threshold?)

Cases where user for some reason decided not to be utilitarian - and where there isn't a clear balance of characters

Which ScenarioTypes does the model most often get wrong? Do this analysis

Which ScenarioTypes does the model most often get wrong?
> Worst at gender, but still better than random - 55% accuracy

---
<!-- - Create a respectable example with Snorkel
  + Figure out why the LabelModel vote accuracy is so low - this accoutns for nearly all of the ML model performance
    ~ Hand-verify each step in exploration file - passes the eye test?
    * Refactor test environment
      - Stay in the Jupyter file - reloading data every time will take too long
      <!-- - Have a nice, compact view of alternatives - will make debugging much easier -->

## 25 Jan 20

Fantastic! Only a 2% difference in performance between gold label trained ML model and heuristic trained model

Seems like the previous values were bugs - due to small sample size, probably

So seems like it would be really great to ask experts to write the heuristic functions

Things to measure (outputs):
- MajorityLabelVoter() acc vs LabelModel() acc
- LabelModel() weights

Things to vary (inputs):
- LF inclusion
> Turns out inaction LF costs a whole point of accuracy - removed
> doctors: 0.0
> utilitarian: -0.002488638822765621
> utilitarian_anthro: -0.0022181346028997684
> inaction: 0.014715429560701154
> pedestrians: -0.001839428695087686
> females: -0.04712183510062762
> fitness: -0.006383899588833564
> status: -0.0007033109716512165
> legal: -0.0012443194113828104
> illegal: -0.0002705042198658525
> youth: -0.0036247565462020903
> criminals: -0.0007033109716512165
> homeless: -0.004273966673880136
> pets: -0.000108201687946341
> spare_strollers: -0.001406621943302322
> spare_girl: -0.008656135035706614
> spare_boy: -0.000649210127678046
> spare_pregnant: -0.0008115126595975575
- Model
```
## Random Forest ##
Accuracy with gold labels: 0.6962778619346461
Accuracy with heuristic labels: 0.6708504652672582
## Log Reg ##
Accuracy with gold labels: 0.7052045011902186
Accuracy with heuristic labels: 0.6623566327634711
## KNN ##
Accuracy with gold labels: 0.653862800259684
Accuracy with heuristic labels: 0.6633304479549881
## SVC Linear ##
Accuracy with gold labels: 0.7033650724951309
Accuracy with heuristic labels: 0.6637632547067734
## SVC Nonlinear ##
-
```
- Model parameters

<!-- - Data content? -->


NB: had to do a refactor, now need to run `python -m hmm.labeling_functions.tests` to run labeling function unit tests

## TODO
- Create a respectable example with Snorkel
  <!-- + Figure out why the LabelModel vote accuracy is so low - this accounts for nearly all of the ML model performance -->
    <!-- ~ Revamp SQL query - get only full sessions -->
    * Do a quick write up on the false positives / false negatives
      - What are typical differences in decisions from MM users to the label model?
      <!-- - Which ScenarioTypes does the model most often get wrong? -->
    ~ Refactor for grid search
- Replicate for the kidney exchange problem
  + First need to go through and export generalizable functions to utils
  + Load the data
  + Try using this use case for label modeling - https://www.snorkel.org/use-cases/crowdsourcing-tutorial
- Look for use cases in Williams' papers (email), others - preferably high expertise and ripe for a survey experiment - what complicated ethical dilemmas exist that we could solve?
- Write up Snorkel in a research paper - see [paper outline](#paper-outline)
- Replicate some other models for a literal baseline (to better compare performance - only way to know if actually comparable)
  + ! Obtain Noothigattu code
  + Kim et al.
  + Nootigatthu et al.
- Find more ethical algorithm use cases in the literature - maybe start with that one ethical alg lit review with the collective/individual taxonomy

## Future features
- (Bonus) Add a method for strategically weighting heuristics based on the expert's "strength of belief" in them
- (Bonus) Compare effect sizes in label model to effect sizes in MM paper
- (Hard) Re-write Snorkel source to make this an original aggregation approach; might be easiest to do this while writing the manuscript
- (Hard) Decide how to prove this method is better (supermoral), not just comparable
- (Hard) Design an experiment to actually gather heuristics from experts for one of the case studies 
    + try to demonstrate that the method works by asking SMEs, instead of just making up heuristics that get a good performance 
    + try to collect demographics to see what expert profile typically performs best, where performance is measured against the hand-labeled data

