
|  Method 	| Local  	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|
|   REST add	| 2.904ms  |  3.5089ms 	|  282.7997ms	|
|   gRPC add	|  0.7009ms 	|   0.78635ms	|   166.5124ms 	|
|   REST rawimg	|  6.9997ms 	|  10.423ms 	|  1150.0498ms 	|
|   gRPC rawimg	|   21.3608ms  |  34.4589ms 	|  331.12198ms	|
|   REST dotproduct	|   3.1516ms	|   4.1096ms	|  282.0951ms	|
|   gRPC dotproduct	|   0.7885ms	|   0.8652ms	|  166.0331ms  	|
|   REST jsonimg	|   43,1303ms	|   50.0834ms	|  1287.6428ms 	|
|   gRPC jsonimg	|    7.5092ms   |  10.2226ms 	|  297.03521ms 	|
|   PING        |    0.050ms   |   0.324ms   |   137ms  |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.

**Answer**: 
1) We observed that data transfer using gRPC calls are way faster than REST calls because of TCP overheadi.e., REST makes a new TCP connection for each call there by resulting in 2n connections whereas gRPC just makes one TCP connection at the beginning and uses the same for subsequesnt calls thereby resulting in n+1 connections.
2) The latency is the time it takes for data or a request to go from the source to the destination. As the latency increases across the different regions, the time taken also increases. TCP expects round trip acknowledgement, therefore higher latency effects its performance.
