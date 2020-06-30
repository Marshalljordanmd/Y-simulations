# Y-simulations
python program simulating mutation accumulation on the human Y-chromosome

Based on the historical record of Genesis, the program begins with 3 male lineages
and assigns mutations for each generation. Mutations are numbered sequentially and 
followed to the end of the run (usually 180 generations), when AC frequencies are 
computed and ploted as common AC bins in the minor form (with major variants folded into minor).

Functions of the program included Growth, Mutation, Famine, Mortality, Bottleneck, and Genghis Khan.
Parameters of these functions can be adjusted internally or from prompts at the beginning of the run.
Promps request settings for subpopulation growth rates, mutation rates, annual death rates, 
number of generations for the run, and maximal subpopulation levels. Internally, the bottleneck
numbers and locations (which generation), and the bottleneck mortalities and number of sons per
Genghis Khan event can be set. Also the number of patriarch profile mutations in the 3 lineages
can be set internally. 
