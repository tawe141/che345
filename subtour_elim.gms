$include tsp_model

Sets
	n subtour id /n1*n1000/
	S1(i) /i4*i5/
        S2(i) /i1*i2/;

Alias (S1, S1comp);
Alias (S2, S2comp);

Equations
	subtour1 eliminate subtour around i4 and i5
        subtour2 eliminate subtour around i1 and i2;

subtour1 .. sum((S1,S1comp), x(S1,S1comp)) =l= 1;
subtour2 .. sum((S2,S2comp), x(S2,S2comp)) =l= 1;

Model tsp /all/;

Solve tsp using mip minimizing z;