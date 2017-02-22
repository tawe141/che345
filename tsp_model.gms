Sets
        i /i1*i5/;

Alias (i,j);

Table d(i,j) distance matrix
$ondelim
$include distances.csv
$offdelim
;

d(i,j) = max(d(i,j), d(j,i));

Binary Variable x(i,j)  decision variable: whether edge is taken;
Variables
        z               objective: minimize distance;

Equations
        obj             minimize distance
        rowsum(i)
        colsum(j)
        zero_diag       zero diagonal;

        obj .. z =e= sum((i,j), d(i,j)*x(i,j));
        rowsum(i) .. sum(j, x(i,j)) =e= 1;
        colsum(j) .. sum(i, x(i,j)) =e= 1;
        zero_diag .. sum(i, x(i,i)) =e= 0;



