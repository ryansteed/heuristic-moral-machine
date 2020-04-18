# Paper outline

## Intro
Heilmeier's catechism
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
>
> Use case where expert demographic problem might not be such an issue: e.g. decision-making by doctors
>
> Seems like this approach inherently easier to sell for scenarios where lots of expertise required (e.g. medical)
> 
> Even in a domain where data is already labeled, what if that data isn't labeled ethically? Could counterbalance with an ethical labeler

## Framing - what is a moral AI? (Problem Statement)
- what is a morality problem? what are some examples in industry? do we need to re-frame existing problems? (are all problems moral problems?)
- What constitutes a *moral* problem (as opposed to another preferences problem)
- show how this would look from regulator side, and from industry side - when would a regulator require this system?
- if we are treating these case studies as unrealistic representations, need to at least describe how this would translate to realistic representations

- Degree of contingency of preferences vsx   non-contingency (kidney vs moral machine)
- Idea of "independency" - when the moral decision is independent of other objectives

Per Yu et al. lit review:
> Ethical dilemmas refer to situations in which any available choice leads to infringing some accepted ethical principle and yet a decision has to be made

Specifically focusing on dilemmas - like Bonnefon

"moral philosophy in intelligent machines"

Would be good to reference James Moor here - see Stanford Phil Encyclopedia entry on Philosophy of AI - will be good for framing approaches in related work section

## Related Work
Mostly reflects Yu et al. review, Conitzer position paper
Position this as a machine learning based collective framework

### Moral Dilemmas

### Moral AI

#### Bottom Up


Describe bottom up approaches

Some general shortcomings:
- representativeness
- representation complexity problem

#### Top Down

Tensions in the literature (make each of these a section):
### deontological vs. consequentialist (social welfare approaches, e.g. Wu?) vs. virtue
deontic:
- Wright
- Davoust - contractual deontology
consequentialist: social welfare approach (Lucy Wu?)
virtue: ?? see lit review

### Measuring Morals

## Approach
- Make it clear we are not trying to represent voter's responses - this is an alternate method
- Definitely falls under consequentialist frame (not deontic or the other one)
- Somewhere between massive emphasis on experts (reasoning systems, ideals) and voter estimation (democracy) - meta-system (combines mutliple appraoches to morality), but not totally democratic
- Describe the method
  + Reference Snorkel training/fitting steps, reproduce equations

```latex
\begin{enumerate}
    \item \emph{Data programming:} Ask experts to source or create labeling functions to compare pairs of alternatives, or sets of alternatives (some optimization criterion). An alternative is simply a set of parameters (in autonomous vehicles, number of passengers and their gender, age, health, whether they follow the law).
    \item \emph{Labeling:} Denoise the labeling functions to label a representative set of alternative choices.
    \item \emph{Learning:} Learn the generative model's preferences - no need for summarization or voter aggregation.
\end{enumerate}
```

- Ability of machine learning approach to generalize beyond experts' heuristics - provide a limited set of heuristics, then still achieve comparable performance.
- A good goal: create some example where similar effect sizes to MM arise. A good strategy might be modeling several ethical camps and writing competing heuristic functions from the perspective of experts from these camps.

## Experiments

things to prove:
- cheaper but just as good
- reconciles conflicting viewpoints effectively
- can add expertise of multiple specialists (USE CASE NEEDED)
- interpretable labels, interpretable decisions - look at output for each heuristic individually to explain the decision made
- combining moral heuristics with existing heuristics optimizing for other things
- hierarchical feature represenations - go granular for some experts, but stay abstract for others - how to represent this to a machine learning model???
- apply distant supervision???

### Moral Machine
- We tried creating labeling functions based on MM results (as if regular people were the experts)
  + Provide sample label functions
- Here's how the label functions performed relative to real users, and here's how much less it cost
  + How well does it agree on random scenarios? on all scenarios?
- When does this method disagree with Kim, Noothigattu and why?
  + Highlight weaknesses of each method
    * Kim: the same as the limits of utility function morality (what if there aren't estimatable moral variables? similar to KE example)
    * Noothigattu: not very fast; probably super inaccurate, if we can manage to reproduce it
    * Both: rely on democratic voter data

Results to present
<!-- - Describe the method used to collect the data -->
<!-- - Describing the datasets -->
  <!-- + Number of votes -->
  <!-- + Number of voters -->
  <!-- + Frequency of each scenario (turns out to be about even, no fun) -->
  <!-- + (MM) Frequency of occurrence by character -->
<!-- - Describing the approach -->
  <!-- + Labeling functions -->
    <!-- * The functions themselves & their source -->
    <!-- * Labeling density -->
    <!-- * Labeling function agreement/disagrement plotted against coverage -->
    <!-- * (KE) code the user responses into heuristics ('expresses a preference for ___ heuristic') -->
  <!-- + Labeling model: rate of agreement (accuracy) with voters (if we assume voters are actually experts, then this is the accuracy of our method; otherwise, examine the differences) -->
    <!-- * Rate of agreement per labeling function -->
    <!-- * (MM) Rate of agreement per labeling function, per scenario type -->
    <!-- * Total rate of agreement -->
    <!-- * The final estimated weight vector -->
    <!-- * (MM) Disagreement by scenario type -->
    <!-- * Labeling model perturbations - how does dropping each LF affect accuracy? -->
    * Qualitative assessment of disagreement by labeling function - try developing an explanatory ML technique for tracing labeling errors (or even modeling errors) back to the heuristics
    <!-- * Trade off between label model, majority voter -->
    <!-- * (KE) Bonus experiment: try weighting by heuristic frequency in user responses -->
  + Discriminative model: rate of agreement
    <!-- ~ Accuracy as data size increases (compare both gold label model and heuristic model - if data is low, does heuristic over-perform?) -->
    <!-- ~ (MM) Match Kim experimental conditions - try to train on first 8 respondents for 128 different voters, then test on last 5 responses -->
    <!-- ~ (KE) Match Kim experimental conditions - try to train on first 8 respondents for 128 different voters, then test on last 5 responses -->
    <!-- * By number of voters -->
    * (Bonus) Accuracy with probabilistic labels instead of threshold (keras cross-entropy loss)
    * (Bonus) (MM) Random scenarios vs. special scenarios
    * (Bonus) Accuracy with the addition of invented data (Cite Snorkel paper section 4.1.4)
    * (Bonus) (MM) Compare to reported statistics for baseline models (Kim, Noothigattu, Freedman)

## Discussion
- Discuss benefits
  + Cost - as demonstrated by comparability
  + Zero-shot applications - theoretical argument about info gain from heuristics
  + For highly complex scenarios when gathering training data is literally not feasible
  + See other benefits in Heilmeier's catechism
- Discuss drawbacks
  + Barriers to entry (education)
  + Demographic problem (smaller sample, less representative demographically) - experts must be proxies for larger populations
  + Inherently problematic case studies
    * e.g. still limited by choice of representation of ethical dilemmas (critical race theory is an example)
    * implicit choice of moral status (what gets moral status?) by selection of features
    * not practically relevant (marginal)
    * many professionals say that these types of features shouldn't even be considered; just choose based on likelihood of survival, or randomly if necessary
  + Succintly, moral machine is deliberately simplified
  + De-democratize moral decision-making - experts may be missing something valuable
  + SME expertise may not compensate for lower sample size
  + Labeling function may have less coverage than direct surveying - maybe people's heuristics differ from their actual behavior (do we trust experts to not have this quirk?)
  + May be impossible to prove if this is working - how to prove labeling functions are honored?
  + The requirements for being an SME labeler exclude certain groups from being able to provide input: The profile of the best performing user by F1 score was a MS or Ph.D. degree in any field, strong Python coding skills, and intermediate to advanced experience with machine learning (Snorkel). How to make this accessible to lower-educated, non Python coders?
- Mirror weak supervision trade-offs section of Snorkel paper
- Future work
  + Actually collect from experts (both ground-truth and heuristics, compare) and test in a real-world scenario
  + Suggest intelligent active learning approach during labeling process (an interface that shows datapoints not covered, or datapoints with high conflict)
  + Human-in-the-loop system, at least for training
  + MOST IMPORTANT: INCLUDE ETHICAL AND "TECHNICAL" HEURISTICS IN SAME LABEL MODEL
  + Eventually generalize to some more universal principles?
  + Hierarchical feature represenations - go granular for some experts, but stay abstract for others - how to represent this to a machine learning model?

## Conclusion
Restate Heilmeier's catechism - call for heuristic approaches
