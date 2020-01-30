# Paper outline
- Section on framing: what is a morality problem? what are some examples in industry? do we need to re-frame existing problems? (are all problems moral problems?)
  + What constitutes a *moral* problem (as opposed to another preferences problem)
  + show how this would look from regulator side, and from industry side - when would a regulator require this system?
  + if we are treating these case studies as unrealistic representations, need to at least describe how this would translate to realistic representations
- Heilmeier's catechism
- Here is a new method
  + Make it clear we are not trying to represent voter's responses - this is an alternate method
- MM use case
  + We tried creating labeling functions based on MM results (as if regular people were the experts)
  + Here's how the label functions performed relative to real users, and here's how much less it cost
    * How well does it agree on random scenarios? on all scenarios?
  + When does this method disagree with Kim, Noothigattu and why?
    * Highlight weaknesses of each method
      - Kim: the same as the limits of utility function morality (what if there aren't estimatable moral variables? similar to KE example)
      - Noothigattu: not very fast; probably super inaccurate, if we can manage to reproduce it
      - Both: rely on democratic voter data
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
  + Inherently problematic case studies - e.g. still limited by choice of representation of ethical dilemmas; implicit choice of moral status (what gets moral status?) by selection of features
  + Succintly, moral machine is deliberately simplified
- Mirror weak supervision trade-offs section of Snorkel paper


## other helpful notes

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
> + Will make it easier to label real-world moral scenarios without actually showing the data to lots of people (privacy)
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

### 16 Jan 19

Starting to see some problems:
- There aren't enough heuristic functions to write here! This example is too simplistic (there aren't enough features to write sophisticated heuristics).
  + UPDATE 20 Jan 20 - this problem is mostly solved
- Even if I get some experts to give me heuristics, they'll 1) be simple, 2) be too if- based and have high coverage (more rules-based), 3) be hard to compare to Noothigattu because so different than the MM audience

Things we might still be able to demonstrate:
- Ability of machine learning approach to generalize beyond experts' heuristics - provide a limited set of heuristics, then still achieve comparable performance.
- A good goal: create some example where similar effect sizes to MM arise. A good strategy might be modeling several ethical camps and writing competing heuristic functions from the perspective of experts from these camps.

### 21 Jan 20 - Williams

Is there a way to prove if this is more extensible (more generalizable) to zero-shot scenarios?
Extrapolate beyond statistical value of life? For instance, regular ML model would value 100 y/o's less than heuristic model

Use case where expert demographic problem might not be such an issue: e.g. decision-making by doctors

Seems like this approach inherently easier to sell for scenarios where lots of expertise required (e.g. medical)

### 28 Jan 20

An interesting framing: moral decisions are those that replace choosing randomly when all alternatives have equal cost, according to the regular problem solving solution

This definition falls short, though - sometimes the difference in cost is outweighed by the moral considerations

So are then those moral considerations ingrained in the cost function? this is the utility max approach to moral AI

What makes this different from a regular machine learning problem?
- Experts should probably be equally weighted? Some sort of social choice considerations are necessary
