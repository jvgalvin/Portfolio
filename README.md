# The New Era of Meal Delivery

## Context

Executives at a fictitious meal preparation company have expressed a desire to expand operations beyond just a single store (in North Berkeley). They would like data-driven recommendations on how the company can capitalize on market opportunities in the greater Bay Area.

## Options Under Consideration

The following options are under consideration to expand operations:

* Adding meal pickup locations
* Using drones to deliver meals
* Using public transit (BART) to deliver meals
* Note that we will not consider using delivery robots as we see no additional or unique benefit afforded by this option which is not captured within one or a combination of the above

## Data and Tools Used

The data used for this analysis is fictitious and synthetic, save for the BART data. This entire project was completed within a virtual machine on AWS  running inside of an Anaconda, PostgreSQL, and Neo4j Docker cluster. Given the nature of the problem, graph centrality and community detection algorithms naturally lent themselves to appropriate solution paths.

## Methodology

This analysis follows a logical series of steps:

* Create and load the BART stations, lines, and travel times tables within PostgreSQL
* Use the tables within PostgreSQL to create a graph within Neo4j
* Verify that the graph database was built correctly
* Perform preliminary analytics on each option delineated above, independent of all other options
* Use findings from preliminary analysis to recommend a hybrid approach to solving the problem
  * Devise a list of candidate satellite stations (criteria below)
  * Refine this list based on travel time from the existing store location
  * Further refine this list in light of the density of the surrounding population

## Decision Criteria

Adding more pickup locations is considered a relatively easy way to grow the customer base. Creating pickup locations requires renting (or purchasing) property, renovating (or building) space in a way that is suitable for the business.

Locations at or near BART stations would be good choices because BART riders could easily pick up meals at the stations they travel through on the way to or from work.

Meals will continue to be made within the existing Berkeley store. Carriers will bring meals to 4 new satellite pickup locations located within BART stations twice daily on weekdays, once in the morning and once in the late afternoon. Drones will deliver meals within a 1.5 mile radius of a given satellite pickup location for an additional fee. Alternatively, customers will have the option to pick the meals up in person within the BART station, without having to leave the turnstiles.

Satellite pickup locations are chosen based on the following criteria:

* The BART station must have a higher measure of betweenness centrality than the North Berkeley store. This is a measurement of how many BART paths pass through that given station.
* The BART station must have a denser population than the North Berkeley store within a 1.5 mile radius.
* Travel time from the Ashby station (closest BART station to the existing store location) to satellite locations is considered using shortest path (Dijkstra)
* Delivery radii for drones must not overlap

## Implementation

Opening of satellite pickup locations should be phased so as to avoid the risk of overly ambitious outlay of capital in real estate and to allow the business to gauge the success of the initiative and modify as necessary.

### Phase One - Establish 4 bellwether BART pick-up locations

[put which ones here...2 drone, 2 non-drone]

### Phase Two - Implement additional locations using lessons learned from phase one

[If current drone-delivery service locations show significantly higher customer traffic, then expand drone-delivery service to additional locations from the data frame (list these out) of candidatesl...probably should keep relatively close to Berkeley to limit cost of transporting meals] 

### Phase Three - Expand beyond the East Bay and San Francisco Peninsula

[Consider establishing more BART pick-up location in areas outside current drone/pickup-delivery service.]

## Cost Benefit Analysis

[insert here]
