# The New Era of Meal Delivery (Grade)

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

Adding more pickup locations is considered a relatively easy way to grow the customer base. Locations at or near BART stations would be good choices because BART riders could easily pick up meals at the stations they travel through on the way to or from work. Additionally, setting up pickup locations in BART stations would be a low-overhead way to reach new customer bases.

Meals will continue to be made within the existing Berkeley store. Carriers will bring meals to 4 new satellite pickup locations located within BART stations twice daily on weekdays, once in the morning and once in the late afternoon. Drones will deliver meals within a 1.5 mile radius of a given satellite pickup location for an additional fee. Alternatively, customers will have the option to pick the meals up in person within the BART station, without having to leave the turnstiles.

Satellite pickup locations are chosen based on the following criteria:

* The BART station must have a higher measure of betweenness centrality than the Ashby station. This is a measurement of how many BART paths pass through that given station.
* Travel time from the Ashby station (closest BART station to the existing store location) to satellite locations is considered using shortest path (Dijkstra)
* Delivery radii for drones must not overlap

Under the criteria above, preference is given to stations that serve the highest population.

## Implementation

Opening of satellite pickup locations should be phased so as to avoid the risk of overly ambitious outlay of capital in real estate and to allow the business to gauge the success of the initiative and modify as necessary.

### Phase One - Establish 4 bellwether BART pick-up locations

* Glen Park
* Civic Center
* Lake Merritt
* Fruitvale

### Phase Two - Implement additional locations using lessons learned from phase one

We will compare the total sales value attributable to drone deliveries against that of in-person pickups at the new locations and recommend a best course of action using this data.

### Phase Three - Expand beyond the East Bay and San Francisco Peninsula

After Phase Two, we will examine how best to scale this new delivery operation.

## Cost Benefit Analysis

While we expect significant benefits from AGM expansion in the Bay Area, there are also costs that need to be taken into account. Much of the expansion has centered around using BART stations for delivery and pickup locations, however each BART ride has a cost and the more extensive use of the BART system, the higher the costs will be. In order to determine how many BART trips are required to fulfill the pickup requests, we decided to extrapolate the number of delivery orders took place in the Peak Deliveries proof-of-concept. In the one-day trial, Peak delivered 540 meals to customers from the Berkeley store. It is difficult to forecast future demand, but we project to double the number of meals delivered by Peak because there are several times more customers in our delivery range, but there may be some uncetainty in our customers using these new options. Our projection is to deliver 1080 meals per day across the different locations with our new delivery options. The final piece of the puzzle is the number of meals that can be transported in a single trip using BART. Based on our industry knowledge, we are projecting a carrier can transport 30 meals in each trip, which would require 9 round-trip BART rides for each location.

### Transportation Costs by Station (Roundtrip from Ashby)

Glen Park transportation costs: $81.90
Civic Center transportation costs: $74.70
Lake Merritt transportation costs: $37.80
Fruitvale transportation costs: $41.40
Total daily transportation costs: $235.80

### Drone Price

Based on preliminary research, we have found the retail price for a delivery drone is $4,000. In Phase 1 of the new delivery options, we recommend starting with one drone per pickup location which would total at $16,000.

### Projected Profit

Based on our projections of 1080 meals sold in a day, that would amount to $12,960 in new daily sales based on the fixed price of $12 per meal. The projected overall profit is $4602884.60 annually.
