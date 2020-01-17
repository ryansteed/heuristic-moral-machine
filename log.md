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

but it seems impossible that each card has its own row! since each row seems like it should be the answer! only possible answer is that they didn't include the other alternative in the data? or not? fuck me, man

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
- Even if I get some experts to give me heuristics, they'll 1) be simple, 2) be too if- based and have high coverage (more rules-based), 3) be hard to compare to Noothigattu because so different than the MM audience

Things we might still be able to demonstrate:
- Ability of machine learning approach to generalize beyond experts' heuristics - provide a limited set of heuristics, then still achieve comparable performance.
- A good goal: create some example where similar effect sizes to MM arise. A good strategy might be modeling several ethical camps and writing competing heuristic functions from the perspective of experts from these camps.

Log:
Managed to write some labeling functions! and did some preliminary analysis
Using https://www.snorkel.org/use-cases/01-spam-tutorial#4-combining-labeling-function-outputs-with-the-label-model

TODO
! Obtain kidney exchange data
- Create a working example with Snorkel
    <!-- + Figure out how to SQL query the responses in pairs - debugging -->
    + Draft some labeling functions from the effect sizes in the MM paper (highlighted in purple in Mendeley - https://www.mendeley.com/viewer/?fileId=3b917119-bbe5-3ee3-7969-b7991da2abf7&documentId=f71b5d60-0d88-323a-a078-960daa3a63c5)
        * Heuristics to spare the four most spared characters: baby, little girl, little boy, pregnant woman
        * Heuristic to save most *human* lives
        * Heuristic to save most *pet* lives
        * Heuristics to prefer:
            - inaction
            - pedestrians
            - females
            - the fit
            - higher status (rich)
            - lawful
            - young
    + Test with Snorkel analysis example - https://www.snorkel.org/use-cases/01-spam-tutorial#4-combining-labeling-function-outputs-with-the-label-model, try tuning the fxns
    + Figure out a way to weight the strength of each heuristic? Would probably improve performance
- Replicate some other models for a baseline
    + Kim et al.
    + Nootigatthu et al.
- Find more ethical algorithm use cases in the literature - maybe start with that one ethical alg lit review with the collective/individual taxonomy


- (Hard) Decide how to prove this method is better, not just comparable
- (Hard) Design an experiment to actually gather heuristics from experts for one of the case studies 
    + try to demonstrate that the method works by asking SMEs, instead of just making up heuristics that get a good performance 
    + try to collect demographics to see what expert profile typically performs best, where performance is measured against the hand-labeled data

