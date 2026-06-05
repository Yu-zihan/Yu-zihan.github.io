---
title: Kantorovich Duality
date: 2026-06-05
type: note
tags: Optimal transport
summary: Annotated notes on the derivation and meaning of Kantorovich duality
---

In optimization, duality is a consistently useful way of solving problems. It is mentioned in *Computational Optimal Transport*, but the derivation of the dual problem in that book is quite concise, which can be unfriendly to readers who are still building their optimization background. I therefore studied the relevant material and wrote these annotated notes to clarify this part and strengthen my own understanding.

## 1. The Discrete Optimal Transport Problem

Consider two discrete probability distributions:
$a=(a_1,\dots,a_n)\in \mathbb R_+^n, \, b=(b_1,\dots,b_m)\in \mathbb R_+^m,$
satisfying
$\sum_{i=1}^n a_i=\sum_{j=1}^m b_j.$
Let the transport cost matrix be $C=(C_{ij})\in \mathbb R^{n\times m}.$
Here, $C_{ij}$ denotes the cost of transporting one unit of mass from source point $i$ to target point $j$.
The transport plan is denoted by
$P=(P_{ij})\in \mathbb R_+^{n\times m},$

where $P_{ij}\ge 0$ represents the amount of mass transported from $i$ to $j$.
The Kantorovich optimal transport problem is
$$
\min_{P\ge 0}\ \langle C,P\rangle
=
\min_{P\ge 0}\sum_{i,j} C_{ij}P_{ij}
$$
subject to
$$
\sum_j P_{ij}=a_i,\qquad i=1,\dots,n,
$$
$$
\sum_i P_{ij}=b_j,\qquad j=1,\dots,m.
$$
In matrix form, this is
$$
P\mathbf 1_m=a,
\qquad
P^T\mathbf 1_n=b,
\qquad
P\ge 0.
$$
Denote the primal optimal value by
$$
p^\star
=
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\langle C,P\rangle.
$$

## 2. Introducing the Lagrangian

The basic idea of constrained optimization is to multiply equality constraints by Lagrange multipliers and add them to the objective function.
On the feasible set, the constraint terms are equal to zero, so this operation does not change the original objective.
For the constraint
$$
\sum_j P_{ij}=a_i,
$$
introduce a multiplier $f_i$. For the constraint
$$
\sum_i P_{ij}=b_j,
$$
introduce a multiplier $g_j$.
Since these are equality constraints, $f_i$ and $g_j$ are unrestricted in sign.
Define the Lagrangian as
$$
\mathcal L(P,f,g)
=
\sum_{i,j}C_{ij}P_{ij}
+
\sum_i f_i\left(a_i-\sum_jP_{ij}\right)
+
\sum_j g_j\left(b_j-\sum_iP_{ij}\right).
$$
If $P$ is primal feasible, then
$$
a_i-\sum_jP_{ij}=0,
\qquad
b_j-\sum_iP_{ij}=0.
$$
Therefore, for any $f,g$, we have
$$
\mathcal L(P,f,g)=\langle C,P\rangle.
$$
This shows that **the Lagrangian coincides with the original objective on the primal feasible set.**

## 3. Rearranging the Lagrangian

Expanding the Lagrangian and collecting the coefficients of $P_{ij}$, we obtain
$$
\mathcal L(P,f,g)
=
\sum_{i,j}C_{ij}P_{ij}
+\sum_i f_i a_i
-\sum_{i,j}f_iP_{ij}
+\sum_j g_j b_j
-\sum_{i,j}g_jP_{ij}.
$$
Hence,
$$
\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle
+\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij}.
$$
Let
$$
s_{ij}=C_{ij}-f_i-g_j.
$$
Then
$$
\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle
+\sum_{i,j}s_{ij}P_{ij}.
$$
Here, $s_{ij}$ is the slack variable associated with the dual constraint.

## 4. Why the Lagrangian Gives a Lower Bound

Although $\mathcal L(P,f,g)$ equals $\langle C,P\rangle$ on the primal feasible set, the derivation of the dual problem does not restrict attention only to that feasible set.
Define the dual function:
$$
d(f,g)=\inf_{P\ge0}\mathcal L(P,f,g).
$$
Note that the marginal constraints have now been relaxed; only
$$
P\ge0
$$
is retained.
Since
$$
\{P\ge0,\ P\mathbf 1=a,\ P^T\mathbf 1=b\}
\subseteq
\{P\ge0\},
$$
taking the infimum over the larger set can only decrease the value, or leave it unchanged:
$$
\inf_{P\ge0}\mathcal L(P,f,g)
\le
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\mathcal L(P,f,g).
$$
On the primal feasible set,
$$
\mathcal L(P,f,g)=\langle C,P\rangle.
$$
Therefore,
$$
d(f,g)\le p^\star.
$$
Thus, $d(f,g)$ is a lower bound on the primal optimal value.
The dual problem is to find the tightest such lower bound:
$$
\max_{f,g}d(f,g).
$$

## 5. Computing the Dual Function

From
$$
\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle
+\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij},
$$
we see that when taking the infimum over $P\ge0$, the behavior of each $P_{ij}$ is determined by the coefficient
$$
C_{ij}-f_i-g_j.
$$

### Case 1: A Negative Coefficient Exists

If there exists some $(i,j)$ such that
$$
C_{ij}-f_i-g_j<0,
$$
then by letting
$$
P_{ij}\to +\infty,
$$
we obtain
$$
(C_{ij}-f_i-g_j)P_{ij}\to -\infty.
$$
Therefore,
$$
d(f,g)=-\infty.
$$
Such a pair $(f,g)$ cannot provide a meaningful lower bound.

### Case 2: All Coefficients Are Nonnegative

If, for all $(i,j)$,
$$
C_{ij}-f_i-g_j\ge0,
$$
that is,
$$
f_i+g_j\le C_{ij},
$$
then
$$
\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij}\ge0.
$$
Therefore,
$$
\inf_{P\ge0}\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle.
$$
The infimum is attained at $P=0$. Note that $P=0$ is generally not primal feasible, but it belongs to the relaxed set $P\ge0$.

## 6. Deriving the Kantorovich Dual Problem

From the previous section, to make the dual function finite, it is necessary to require
$$
f_i+g_j\le C_{ij},\qquad \forall i,j.
$$
Under this condition,
$$
d(f,g)=\langle f,a\rangle+
\langle g,b\rangle.
$$
Therefore, the Kantorovich dual problem is
$$
\max_{f,g}\ \langle f,a\rangle+
\langle g,b\rangle
$$
subject to
$$
f_i+g_j\le C_{ij},\qquad \forall i,j.
$$
It can also be written as
$$
L_C(a,b)
=
\max_{(f,g)\in \mathcal R(C)}
\langle f,a\rangle+
\langle g,b\rangle,
$$
where
$$
\mathcal R(C)
=
\left\{(f,g)\in\mathbb R^n\times\mathbb R^m:
f_i+g_j\le C_{ij},\ \forall i,j\right\}.
$$
Here, $f,g$ are called **Kantorovich potentials**.

## 7. A Direct Understanding of Weak Duality

If $(f,g)$ satisfies
$$
f_i+g_j\le C_{ij},
$$
then for any primal feasible $P$,
$$
\sum_{i,j}C_{ij}P_{ij}
\ge
\sum_{i,j}(f_i+g_j)P_{ij}.
$$
Using the marginal constraints, the right-hand side expands as
$$
\sum_{i,j}(f_i+g_j)P_{ij}
=
\sum_{i,j}f_iP_{ij}+
\sum_{i,j}g_jP_{ij}.
$$
Since
$$
\sum_jP_{ij}=a_i,
\qquad
\sum_iP_{ij}=b_j,
$$
we have
$$
\sum_{i,j}f_iP_{ij}
=
\sum_i f_i a_i
=\langle f,a\rangle,
$$
and
$$
\sum_{i,j}g_jP_{ij}
=
\sum_j g_j b_j
=\langle g,b\rangle.
$$
Therefore,
$$
\langle C,P\rangle
\ge
\langle f,a\rangle+
\langle g,b\rangle.
$$
This shows that any dual feasible pair $(f,g)$ gives a lower bound on the primal transport cost.
Hence,
$$
\max_{f_i+g_j\le C_{ij}}
\langle f,a\rangle+
\langle g,b\rangle
\le
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\langle C,P\rangle.
$$
This is weak duality.

## 8. Strong Duality

Since discrete OT is a finite-dimensional linear program, strong duality for linear programming holds whenever the problem is feasible and has a finite optimal value. Therefore,
$$
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\langle C,P\rangle
=
\max_{f_i+g_j\le C_{ij}}
\langle f,a\rangle+
\langle g,b\rangle.
$$
In other words, the best lower bound is exactly equal to the minimum primal transport cost.

#### Proving Strong Duality for Linear Programming via Farkas' Lemma

Consider a linear program in the following standard primal form:
$$
z^\star
=
\min_x
\left\{
c^T x
\mid
Ax=b,\ x\ge 0
\right\}.
$$
Its weak dual is
$$
d^\star
=
\max_y
\left\{
b^T y
\mid
A^T y\le c
\right\}.
$$
By weak duality,
$$
d^\star \le z^\star.
$$
We now need to prove the reverse inequality:
$$
d^\star \ge z^\star.
$$

### Farkas' Lemma

For a matrix $A\in \mathbb R^{m\times n}$ and a vector $b\in \mathbb R^m$, exactly one of the following two statements is true:

1. There exists $x\in\mathbb R^n$ such that
$$
Ax=b,\qquad x\ge 0.
$$

2. There exists $y\in\mathbb R^m$ such that
$$
A^T y\le 0,
\qquad
b^T y>0.
$$

Geometrically, the first case says that $b$ lies in the nonnegative cone generated by the columns of $A$; the second case says that there exists a hyperplane separating $b$ from this cone.

### From Farkas' Lemma to Strong Duality

Suppose the primal optimal solution is $x^\star$, with optimal value
$$
z^\star=c^T x^\star.
$$
Take any $\varepsilon>0$.

Since $z^\star$ is already the minimum value, there does not exist $x\ge0$ such that
$$
Ax=b,
\qquad
c^T x=z^\star-\varepsilon.
$$
Equivalently, there does not exist $x\ge0$ satisfying
$$
\widehat A x=\widehat b_\varepsilon,
$$
where
$$
\widehat A
=
\begin{pmatrix}
A\\
-c^T
\end{pmatrix},
\qquad
\widehat b_\varepsilon
=
\begin{pmatrix}
b\\
-z^\star+\varepsilon
\end{pmatrix}.
$$
That is, the system
$$
\widehat A x=\widehat b_\varepsilon,
\qquad
x\ge0
$$
has no solution.

By Farkas' lemma, there exists
$$
\widehat y
=
\begin{pmatrix}
y\\
\alpha
\end{pmatrix}
$$
such that
$$
\widehat A^T\widehat y\le0,
\qquad
\widehat b_\varepsilon^T\widehat y>0.
$$
Expanding the first condition gives
$$
\widehat A^T\widehat y
=
A^T y-\alpha c
\le0.
$$
Therefore,
$$
A^T y\le \alpha c.
$$
Expanding the second condition gives
$$
\widehat b_\varepsilon^T\widehat y
=
b^T y+\alpha(-z^\star+\varepsilon)
>0.
$$
Thus,
$$
b^T y>\alpha(z^\star-\varepsilon).
$$

### Showing That $\alpha>0$

When $\varepsilon=0$, we have
$$
\widehat A x^\star
=
\widehat b_0.
$$
Thus, the system
$$
\widehat A x=\widehat b_0,
\qquad
x\ge0
$$
has a solution.

By Farkas' lemma, in this case there cannot exist $\widehat y$ such that
$$
\widehat A^T\widehat y\le0,
\qquad
\widehat b_0^T\widehat y>0.
$$
In other words, whenever
$$
\widehat A^T\widehat y\le0,
$$
we must have
$$
\widehat b_0^T\widehat y\le0.
$$
But we already have
$$
\widehat b_\varepsilon^T\widehat y
=
\widehat b_0^T\widehat y+\alpha\varepsilon
>0.
$$
Since
$$
\widehat b_0^T\widehat y\le0,
$$
the above inequality can be positive only if
$$
\alpha>0.
$$

### Obtaining a Dual Feasible Solution

Since $\alpha>0$, define
$$
\tilde y=\frac{y}{\alpha}.
$$
From
$$
A^T y\le \alpha c,
$$
we obtain
$$
A^T \tilde y\le c.
$$
Thus, $\tilde y$ is dual feasible.

Moreover, from
$$
b^T y>\alpha(z^\star-\varepsilon),
$$
dividing both sides by $\alpha>0$ gives
$$
b^T\tilde y>z^\star-\varepsilon.
$$
Therefore,
$$
d^\star
=
\max_y
\left\{
b^T y
\mid
A^T y\le c
\right\}
>
z^\star-\varepsilon.
$$
Since $\varepsilon>0$ is arbitrary,
$$
d^\star\ge z^\star.
$$
Together with weak duality,
$$
d^\star\le z^\star,
$$
we conclude that
$$
d^\star=z^\star.
$$
That is,
$$
\max_y
\left\{
b^T y
\mid
A^T y\le c
\right\}
=
\min_x
\left\{
c^T x
\mid
Ax=b,\ x\ge0
\right\}.
$$
This is strong duality for linear programming.

## 9. Complementary Slackness

Let $P^\star$ be a primal optimal solution, and let $(f^\star,g^\star)$ be a dual optimal solution.

Strong duality gives
$$
\langle C,P^\star\rangle
=
\langle f^\star,a\rangle+
\langle g^\star,b\rangle.
$$
On the other hand, by the primal-dual gap identity,
$$
\langle C,P\rangle
-\bigl(\langle f,a\rangle+
\langle g,b\rangle\bigr)
=
\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij}.
$$
Substituting the optimal solutions gives
$$
\sum_{i,j}(C_{ij}-f_i^\star-g_j^\star)P_{ij}^\star=0.
$$
Since
$$
C_{ij}-f_i^\star-g_j^\star\ge0,
\qquad
P_{ij}^\star\ge0,
$$
every term is nonnegative. A sum of nonnegative terms can equal zero only when each term is zero:
$$
(C_{ij}-f_i^\star-g_j^\star)P_{ij}^\star=0,
\qquad \forall i,j.
$$
This is the complementary slackness condition.
Equivalently,
$$
P_{ij}^\star>0
\quad\Longrightarrow\quad
f_i^\star+g_j^\star=C_{ij}.
$$
In other words, optimal transport occurs only along edges where the dual constraint is tight.

## 10. The Meaning of Complementary Slackness

Define the slack variable:
$$
s_{ij}=C_{ij}-f_i^\star-g_j^\star.
$$
Complementary slackness is
$$
P_{ij}^\star s_{ij}=0.
$$
Its meaning is as follows:

- If $P_{ij}^\star>0$, then $s_{ij}=0$, that is,
$$
f_i^\star+g_j^\star=C_{ij}.
$$

- If $s_{ij}>0$, then $P_{ij}^\star=0$.

That is,
$$
\text{Any edge that carries positive mass must be a tight edge.}
$$
However, the converse is not necessarily true:
$$
f_i^\star+g_j^\star=C_{ij}
$$
only indicates that the edge may be used; it does not guarantee
$$
P_{ij}^\star>0.
$$
Therefore,
$$
\operatorname{supp}(P^\star)
\subseteq
\{(i,j):f_i^\star+g_j^\star=C_{ij}\}.
$$

## 11. The Role of the Potentials

The Kantorovich potentials $f,g$ mainly serve three purposes.

### 11.1 Proving Optimality

If we find a primal feasible $P$ and a dual feasible pair $(f,g)$ such that
$$
\langle C,P\rangle
=
\langle f,a\rangle+
\langle g,b\rangle,
$$
then both $P$ and $(f,g)$ are optimal.
The reason is that the dual objective is a lower bound on the primal objective. If a primal feasible solution exactly attains this lower bound, it cannot be improved further.

### 11.2 Locating the Support of the Optimal Transport Plan

By complementary slackness,
$$
P_{ij}^\star>0
\Rightarrow
f_i^\star+g_j^\star=C_{ij}.
$$
Therefore, the potentials help rule out edges that cannot be used:
$$
f_i^\star+g_j^\star<C_{ij}
\Rightarrow
P_{ij}^\star=0.
$$

### 11.3 Interpreting Potentials as Prices or Potential Energy

One can interpret $f_i$ as the price of source point $i$ and $g_j$ as the price of target point $j$.
The constraint
$$
f_i+g_j\le C_{ij}
$$
means that the total potential from $i$ to $j$ cannot exceed the true transport cost.
At optimality, every edge that actually carries mass satisfies
$$
f_i^\star+g_j^\star=C_{ij}.
$$
That is, on the used edges, the potential exactly matches the transport cost.

## 12. Summary

The primal problem of discrete Kantorovich optimal transport is
$$
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\langle C,P\rangle.
$$
Using the Lagrangian
$$
\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle
+\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij},
$$
and taking the infimum over $P\ge0$, we obtain the dual feasibility condition
$$
f_i+g_j\le C_{ij}.
$$
Therefore, the Kantorovich dual problem is
$$
\max_{f_i+g_j\le C_{ij}}
\langle f,a\rangle+
\langle g,b\rangle.
$$
Strong duality guarantees that
$$
\min_{P}\langle C,P\rangle
=
\max_{f,g}\langle f,a\rangle+
\langle g,b\rangle.
$$
The optimal solutions satisfy complementary slackness:
$$
(C_{ij}-f_i^\star-g_j^\star)P_{ij}^\star=0.
$$
Thus,
$$
P_{ij}^\star>0
\Rightarrow
f_i^\star+g_j^\star=C_{ij}.
$$
This means that optimal transport occurs only where the potentials are tangent to the cost matrix.

## Reference

- Jianlin Su. "From Wasserstein Distance and Duality Theory to WGAN." *Scientific Spaces*, 2019-01. https://spaces.ac.cn/archives/6280
- Gabriel Peyré and Marco Cuturi. *Computational Optimal Transport*. *Foundations and Trends in Machine Learning*, 2019. https://optimaltransport.github.io/book/
