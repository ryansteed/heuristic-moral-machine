# Heuristic Moral Machine Project

Attempting to train moral algorithms with ethical/legal heuristic functions to build more ethical systems.


## Data
Using [published data](https://osf.io/3hvt2/?view_only=4bb49492edee4a8eb1758552a362a2cf) from [Moral Machine](http://moralmachine.mit.edu/) experiment.

Recommended: convert data into a SQLite db locally by doing the following:
```
sqlite> .mode csv
sqlite> .import path/to/db path/to/SharedResponses.csv sharedresponses
```
