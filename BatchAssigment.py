
"""Problem 1 (Batch assignment). Consider a set of requests R ,  a set of vehicles V at their current state including passengers ,
and a function to compute travel times on the road network.
Compute the OPTIMAL assignment S of request to vehicles that minimizes a cost function C and that satisfies a set of constraints Z , including maximum capacity V of passengers per vehicle.

We will consider the following set of constraints Z:

1) For each request r , its maximum wating time Request.actual_pick_up_time <= Request.latest_time_to_pick_up

2) For each request or passenger r , its maximum travel delay

 """