/*********************************************
 * OPL 12.6.0.0 Model
 * Author: frant
 * Creation Date: 21/10/2016 at 08:53:22
 *********************************************/

/********/
/* DATA */
/********/
int bigM=...;

int startLocation=...;
int nLocations=...;

range N=1..nLocations;
 
int task[n in N]=...;
int minW[n in N]=...;
int maxW[n in N]=...;

int distances[n in N, n2 in N]=...;
 
 
/******************/
/* DECISSION VARS */
/******************/

// The number of vehicles needed in order to do
// the optimal routes.
dvar int nVehicles;

// Whether the path from n to n2 has been taked.
dvar boolean tracked[n in N, n2 in N];

// Hour in minutes in which the last vehicle has
// done the work.
dvar int lastDone;

// Arriving times for every location
dvar int arrivingTime[n in N];


/*****************/
/* OBJ. FUNCTION */
/*****************/

// We are multiplying the nVehicles by a bigM because it is 
// more important to optimize the number of nVehicles that the lastDone.
// In fact, that we want is that if there are more than two solutions
// with the same nVehicles, then, the solution, should be this one
// that end before, i.e. this one that has smallest lastDone.
minimize nVehicles*bigM + lastDone;


/***************/
/* CONSTRAINTS */
/***************/

subject to {
	/* GRAPH CONSTRAINTS */
	
	// All locations have to be visited exactly one time except 
	// startLocation. i.e. to have only one entry edge.
	forall (n1 in N) {
		if (n1 == startLocation) sum(n2 in N) tracked[n1, n2] >=1;		
		else sum(n2 in N) tracked[n1, n2] == 1;		
	}
	
	// The number of entry edges in a node will be equal as the
	// out edges.
	forall (n in N) {
		sum(n2 in N) tracked[n, n2] == sum(n3 in N) tracked[n3, n];	
	}
	
	// If the truck is in a city it can not get track to the same city (loop).
	forall(n in N) {
		tracked[n,n] == 0;	
	}

	// TODO: We have to ensure that all cycles in the graph must involve
	// the startLocation node.
	// NOTE: Check out the TSP.

	/* TIME CONSTRAINTS */
	
	// We need this constraints in order to calculate the arrivingTime of the
	// other locations.
	arrivingTime[startLocation] == 0;
	
	// The arriving time at a location will be the time spent in order
	// to arrive to this location or the minW
	forall(n in N, n2 in N) {
		if (n!=startLocation)
			arrivingTime[n] >= (arrivingTime[n2] + task[n2] + distances[n2, n])-(bigM*(1-tracked[n2, n]));	
	}
	
	// But in fact, if the arriving time is before minW, then we have to wait until
	// minW, then another constraint must be imposed.
	forall(n in N) {
		if (n != startLocation)
			arrivingTime[n] >= minW[n];		
	}
	
	// (*) One of the two above constraints will impose the arrivingTime.
	// CPLEX will want to minimize the arrivingTime, therefore the constraint
	// is >=. 
	
	// Arriving time should be before maxW
	forall(n in N) {
		if (n != startLocation)
			arrivingTime[n] <= maxW[n];	
	}
	
	// Good value for nVehicles. Is the number of cycles, that is in fact the
	// number of edges that go out from startLocation
	nVehicles == sum(n in N) tracked[startLocation, n];
	
	// Good value for lastDone. We only have to check the paths from
	// whereever to startLocation, and get the most big one.
	forall (n in N) {
		lastDone >= (arrivingTime[n] + task[n] + distances[n, startLocation])-(bigM*(1-tracked[n, startLocation]));
	}
	
	// All work should be done from 8 a.m. to 8 p.m., i.e. in 12 hours
	lastDone <= 12*60;
	
	// Los arriving time del siguiente nodo ha de ser mayot que el del anterior
	// excepto para el camino de vuelta a ls. No sé si hace falta.
}


