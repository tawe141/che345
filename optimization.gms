Sets
	i /i1*i7/;

Alias (i,j);

Table d(i,j) distance matrix
$ondelim
$include distances.csv
$offdelim
;

d(i,j) = max(d(i,j), d(j,i));

Binary Variable x(i,j)	decision variable: whether edge is taken;
Variable z		objective: minimize distance;

x(i,i) = 0;

Equations
	obj 		minimize distance
        rowsum(i)	each city can only be visited once -- only two edges per city;

        obj .. z =e= sum((i,j), d(i,j)*x(i,j));
        rowsum(i) .. sum(j, x(i,j)) =e= 2;

Model tsp /all/;

Solve tsp using mip minimizing z;

