# AI Planning: Comparison of Metric-FF and HTN Planners

Given the wide variety and number of planning domains, it is necessary to consider how 
problems in these domains might be solved most efficiently. I compared a domain 
independent planner, specifically Metric-FF, with Hierarchical Task Network (HTN) planners for two 
established domains: Blocksworld and Satellite. 

I developed HTN methods in GTPyhop to solve randomly generated problems in the Satellite domain. I conducted 100 experiments per domain to 
compare planners’ performance in terms of CPU time and plan length, finding that the HTN planner performed up to 100x better in terms of CPU time.

The [Report](Report.pdf) goes into further detail on how I structured my HTN methods for the Satellite domain, how I decided on Metric-FF,
and the design and results of my comparative analyses.

Navigate to [GTPyhop>Examples](GTPyhop/Examples) to see the HTN methods, experiments, randomly generated problems by size, and results for each domain. 

The [Metric_FF_and_Satellite_problems](Metric_FF_and_Satellite_problems.ipynb) notebook includes Metric-FF related work and experiments, and the generation of Satellite 
problems.

The [satellite-generator folder](satellite-generator) includes the code provided to me to generate Satellite problems.

Metric-FF results includes the results of running Metric-FF on each domain.
