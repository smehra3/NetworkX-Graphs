# NetworkX-Graphs

Eight employees at a small company were asked to choose 3 movies that they would most enjoy watching for the upcoming company movie night. These choices are stored in the file `Employee_Movie_Choices.txt`.
A second file, `Employee_Relationships.txt`, has data on the relationships between different coworkers. 
The relationship score has value of `-100` (Enemies) to `+100` (Best Friends). A value of zero means the two employees haven't interacted or are indifferent.
Both files are tab delimited.

Using NetworkX, loaded and plotted:
* Bipartite graph from `Employee_Movie_Choices.txt`
* Weighted Projected graph and saw how many movies different pairs of employees have in common

Found the Pearson correlation ( using `DataFrame.corr()` ) between employee relationship scores and the number of movies they have in common. If two employees have no movies in common it was treated as a 0.
