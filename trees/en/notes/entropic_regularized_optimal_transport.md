---
title: Entropic Regularized Optimal Transport
date: 2026-05-22
type: note
tags: Optimal transport
summary: Personal notes on entropic regularized optimal transport
---

## 1. Definition of Discrete Optimal Transport

Optimal transport ultimately concerns a concrete computational problem. In practical computation, it is usually discretized and can be formulated as follows.

Let $a \in \mathbb{R}^n$ and $b \in \mathbb{R}^m$ denote the source and target distributions, respectively, satisfying $a_i \ge 0$, $b_j \ge 0$, and $\sum_i a_i = \sum_j b_j = 1$.

Define:
- The **transport matrix** $P \in \mathbb{R}^{n\times m}$, where $P_{ij}$ denotes the amount of mass transported from the $i$-th point to the $j$-th point.
- The **cost matrix** $C \in \mathbb{R}^{n\times m}$, where $C_{ij}=c(x_i,y_j)$.

The discrete optimal transport problem is to solve
$$\min_{P}\sum_{i,j} C_{ij}P_{ij}$$
subject to $P\mathbf{1}_m = a$ (row constraint: conservation of mass in the source distribution), $P^T\mathbf{1}_n = b$ (column constraint: conservation of mass in the target distribution), and $P_{ij}\ge0$.

## 2. Why Do We Need Entropic Regularization?

Standard OT has several computational difficulties: the number of variables is large ($n\times m$), the number of constraints is $(n+m)$, linear programming is expensive, and the resulting solution may be sparse or unstable.

Therefore, we introduce the entropic regularization term
$$H(P)=-\sum_{i,j}P_{ij}\log P_{ij},$$
which changes the objective function into
$$\min_P \sum_{i,j} C_{ij}P_{ij} - \varepsilon H(P) = \min_P \sum_{i,j} C_{ij}P_{ij} + \varepsilon\sum_{i,j}P_{ij}\log P_{ij}.$$
Here, $\varepsilon>0$ is the regularization strength. A larger entropy encourages a smoother transport plan.

The meaning of this regularization can be understood as follows. When $\varepsilon\rightarrow\infty$, the regularization term dominates and pushes the solution toward the maximum-entropy transport plan satisfying the marginal constraints; from an information-theoretic perspective, this distribution is the outer product of the two marginal distributions. When $\varepsilon\rightarrow 0$, the problem gradually approaches the standard optimal transport problem.

## 3. Lagrangian Form of Entropic Regularized OT

Using basic optimization theory, we can derive an analytic expression for $P$ through the method of Lagrange multipliers. Introduce the Lagrange multipliers $f_i$ for the row constraints and $g_j$ for the column constraints. The Lagrangian can be written as
$$\mathcal{L}(P,f,g) = \sum_{i,j}\left(C_{ij}P_{ij}+\varepsilon P_{ij}\log P_{ij}\right) - \sum_i f_i\left(a_i-\sum_j P_{ij}\right) - \sum_j g_j\left(b_j-\sum_i P_{ij}\right).$$
Taking the partial derivative with respect to each $P_{ij}$ and setting it to zero gives
$$\frac{\partial \mathcal{L}}{\partial P_{ij}} = C_{ij}+\varepsilon(\log P_{ij}+1)-f_i-g_j = 0.$$
Rearranging yields
$$\log P_{ij} = \dfrac{f_i+g_j-C_{ij}}{\varepsilon}-1,$$
and therefore
$$P_{ij} = \exp\!\left(\frac{f_i}{\varepsilon}\right)\exp\!\left(-\frac{C_{ij}}{\varepsilon}\right)\exp\!\left(\frac{g_j}{\varepsilon}\right)e^{-1}.$$
Absorbing the constant into the variables, define
$$u_i = \exp\!\left(\dfrac{f_i}{\varepsilon}\right), \qquad
v_j = \exp\!\left(\dfrac{g_j}{\varepsilon}\right), \qquad
K_{ij}=\exp\!\left(-\dfrac{C_{ij}}{\varepsilon}\right).$$
Then
$$P_{ij}=u_i K_{ij} v_j.$$

## 4. Matrix Form

The expression derived in the previous section can be written in matrix form, which is more convenient for GPU-based computation.

Define $u \in \mathbb{R}^n$, $v\in\mathbb{R}^m$, and $K=\exp(-C/\varepsilon)$. Then
$$P = \mathrm{diag}(u)\,K\,\mathrm{diag}(v).$$
The equation above is only a structural analytic form. In principle, the marginal constraints still need to be imposed in order to determine the scaling vectors $u$ and $v$. The most classical method for doing this is the Sinkhorn algorithm, which is introduced below.

## 5. Deriving the Sinkhorn Iteration from Marginal Constraints

From $P\mathbf{1}_m=a$, substituting the matrix expression gives
$$\mathrm{diag}(u)K\mathrm{diag}(v)\mathbf{1}_m=a.$$
This is equivalent to
$$u \odot (Kv)=a,$$
so $u$ should satisfy
$$u = \frac{a}{Kv}.$$
Similarly, from $P^T\mathbf{1}_n=b$, we obtain
$$v=\frac{b}{K^Tu}.$$

The vectors $u$ and $v$ depend on each other. If one of them were known explicitly, the other could be computed immediately. However, since neither is known in advance, we introduce the Sinkhorn-Knopp iterative algorithm. The idea is to take an initial step and then gradually correct the two scaling vectors until convergence.

Initialize $v^{(0)}=\mathbf{1}$, and iterate:
$$u^{(t+1)} = \frac{a}{Kv^{(t)}}, \qquad v^{(t+1)} = \frac{b}{K^Tu^{(t+1)}}.$$
Finally,
$$P^\star = \mathrm{diag}(u)K\mathrm{diag}(v).$$

This algorithm is very simple. However, why does it converge to a particular value? Mathematicians have already established its convergence rigorously, but as learners, we still need some intuitive explanations. The following sections provide two such perspectives.

## 6. Why Sinkhorn Converges: The Matrix Scaling Perspective

The optimal solution of entropic regularized optimal transport has the form
$$
P^\star = \operatorname{diag}(u) K \operatorname{diag}(v),
$$
where
$$
K_{ij} = e^{-C_{ij}/\varepsilon}.
$$
Since $\varepsilon > 0$, and since $C_{ij}$ is usually assumed to be finite, we have
$$
K_{ij} > 0.
$$

In other words, entropic regularization transforms the original optimal transport problem into a **positive matrix scaling problem**.

Given a positive matrix $K$, we seek two positive vectors $u$ and $v$ such that the row sums of
$$\operatorname{diag}(u) K \operatorname{diag}(v)$$
equal $a$, and the column sums equal $b$.

The row marginal constraint requires
$$\operatorname{diag}(u)Kv = a.$$
Written elementwise, this becomes
$$u_i (Kv)_i = a_i.$$

Therefore, when $v$ is fixed, the only update that makes the row sums equal to $a$ is
$$
u_i = \frac{a_i}{(Kv)_i}.
$$
Similarly, the column marginal constraint requires
$$\operatorname{diag}(v)K^\top u = b.$$
Written elementwise, this becomes
$$v_j (K^\top u)_j = b_j.$$

Therefore, when $u$ is fixed, the only update that makes the column sums equal to $b$ is
$$
v_j = \frac{b_j}{(K^\top u)_j}.
$$
Thus, the Sinkhorn iteration is
$$u^{(t+1)} = \frac{a}{K v^{(t)}},$$
$$v^{(t+1)} = \frac{b}{K^\top u^{(t+1)}}.$$

Intuitively, the Sinkhorn iteration repeatedly performs two operations:
1. Fix the column scaling $v$ and correct the row scaling $u$ so that the row sums equal $a$.
2. Fix the row scaling $u$ and correct the column scaling $v$ so that the column sums equal $b$.

That is,
$$\text{correct rows} \rightarrow \text{correct columns} \rightarrow \text{correct rows} \rightarrow \text{correct columns} \rightarrow \cdots$$

Why does this repeated row-column scaling not oscillate indefinitely, but instead converge? A simple way to understand this is that the mapping corresponding to the Sinkhorn iteration is a contraction mapping.

Write the Sinkhorn update only in terms of $v$:
$$v^{(t+1)} = F(v^{(t)}) = \frac{b}{K^\top\left(\frac{a}{Kv^{(t)}}\right)}.$$
That is, each iteration applies the same mapping $F$ to the current $v$.

Since $K$ is a strictly positive matrix, multiplication by $K$ or $K^\top$ averages out extreme ratio differences in a vector. Therefore, after one Sinkhorn update, the difference between two different initial values becomes smaller.

Equivalently, there exists an appropriate distance $d$ and a constant $0<\gamma<1$ such that
$$
d(F(v),F(w))
\leq
\gamma d(v,w).
$$
This is precisely the contraction property.

A contraction mapping has an important property: repeated iteration does not produce genuine periodic oscillations, but converges to a unique fixed point.

Thus, the Sinkhorn iteration eventually converges to some $v^\star$ satisfying
$$
F(v^\star)=v^\star.
$$
Then
$$
u^\star=\frac{a}{Kv^\star}
$$
gives the corresponding $u^\star$.

Therefore,
$$P^\star = \operatorname{diag}(u^\star)K\operatorname{diag}(v^\star)$$
satisfies both the row and column marginal constraints. Since this form was obtained from the Lagrange multiplier derivation, it is the optimal transport plan for entropic regularized optimal transport. It should be noted that “unique” here refers to the final transport matrix $P^\star$; the scaling factors $u^\star$ and $v^\star$ themselves may differ by a common multiplicative factor.

## 7. Sinkhorn as Alternating KL Projection

The Sinkhorn iteration can also be understood from the perspective of projection onto constraint sets.

Define two constraint sets:
$$\mathcal C_a = \{\pi : \pi \mathbf 1 = a\}, \qquad
\mathcal C_b = \{\pi : \pi^\top \mathbf 1 = b\}.$$

Here:
- $\mathcal C_a$ denotes the set of all transport matrices whose row marginal is $a$.
- $\mathcal C_b$ denotes the set of all transport matrices whose column marginal is $b$.

Entropic regularized optimal transport can be understood as finding, among all transport plans satisfying the marginal constraints, the matrix closest to the Gibbs kernel $K$. Here, the notion of “distance” is not Euclidean distance, but KL divergence.

Specifically, the objective of entropic regularized optimal transport can be written as
$$\min_{\pi \in \mathcal C_a \cap \mathcal C_b} \sum_{i,j} C_{ij}\pi_{ij} + \varepsilon \sum_{i,j}\pi_{ij}\log \pi_{ij}.$$

Let
$$K_{ij}=e^{-C_{ij}/\varepsilon}.$$

Then
$$C_{ij}=-\varepsilon \log K_{ij}.$$

Substituting this into the objective gives
$$\sum_{i,j} C_{ij}\pi_{ij} + \varepsilon \sum_{i,j}\pi_{ij}\log \pi_{ij} = \sum_{i,j}(-\varepsilon \log K_{ij})\pi_{ij} + \varepsilon \sum_{i,j}\pi_{ij}\log \pi_{ij}.$$

Further simplification yields
$$= \varepsilon \sum_{i,j}\pi_{ij}\left(\log \pi_{ij} - \log K_{ij}\right) = \varepsilon \sum_{i,j}\pi_{ij}\log \frac{\pi_{ij}}{K_{ij}}.$$

Therefore, over the constraint set $\mathcal C_a \cap \mathcal C_b$, the original problem is equivalent to
$$\min_{\pi \in \mathcal C_a \cap \mathcal C_b} \sum_{i,j}\pi_{ij}\log \frac{\pi_{ij}}{K_{ij}}.$$

This quantity can be interpreted as a KL-type distance from $\pi$ to the unnormalized kernel $K$.

Thus, from the perspective of projection onto constraint sets, entropic regularized OT seeks the transport matrix that is closest to the Gibbs kernel $K$ among all matrices satisfying the marginal constraints:
$$\pi^\star = \arg\min_{\pi \in \mathcal C_a \cap \mathcal C_b} \sum_{i,j}\pi_{ij}\log \frac{\pi_{ij}}{K_{ij}}.$$

The Sinkhorn iteration alternately projects the current matrix onto the two constraint sets:
$$\mathcal C_a \rightarrow \mathcal C_b \rightarrow \mathcal C_a \rightarrow \mathcal C_b \rightarrow \cdots$$

That is:
1. First project the current matrix onto the set $\mathcal C_a$ satisfying the row marginal constraint.
2. Then project it onto the set $\mathcal C_b$ satisfying the column marginal constraint.
3. Repeat this process.

Under KL geometry, the projection onto $\mathcal C_a$ corresponds exactly to “row scaling”:
$$
u_i = \frac{a_i}{(Kv)_i}.
$$
The projection onto $\mathcal C_b$ corresponds exactly to “column scaling”:
$$
v_j = \frac{b_j}{(K^\top u)_j}.
$$

Therefore, the Sinkhorn iteration can also be viewed as

> alternating KL projection between the two convex sets $\mathcal C_a$ and $\mathcal C_b$.

This is analogous to alternating projection in Euclidean space: if there are two convex sets, repeatedly projecting onto the first set and then onto the second usually brings the point closer to their intersection.

Here, the intersection of the two sets is
$$\mathcal C_a \cap \mathcal C_b = \{\pi : \pi \mathbf 1 = a,\ \pi^\top \mathbf 1 = b\}.$$

This is precisely the set of all couplings satisfying the two marginal distribution constraints.

Since both $\mathcal C_a$ and $\mathcal C_b$ are convex sets, and since KL divergence corresponds to Bregman projection with favorable convergence properties, alternating KL projection converges to the optimal point in the intersection.

Therefore, from the set-projection perspective, Sinkhorn converges because

> it does not update the matrix arbitrarily; instead, under KL geometry, it repeatedly projects the matrix back onto the two convex sets corresponding to the “correct row marginal” and the “correct column marginal.” Convexity and the KL projection structure guarantee the convergence of this process.

---

## Summary

The main line of this note is as follows: standard OT is computationally expensive $\to$ entropic regularization is introduced $\to$ Lagrangian differentiation yields the analytic structure $P_{ij}=u_iK_{ij}v_j$ $\to$ this is written in matrix form as $P=\operatorname{diag}(u)K\operatorname{diag}(v)$ $\to$ substituting the marginal constraints gives the Sinkhorn iteration.

The convergence of Sinkhorn iteration can be understood from two perspectives. From the **matrix scaling** perspective, the iterative mapping $F$ is a contraction mapping with a unique fixed point. From the **KL projection** perspective, each step is an alternating Bregman projection between the two convex sets $\mathcal{C}_a$ and $\mathcal{C}_b$, and convexity guarantees convergence.

The two perspectives are complementary: the former explains why the iteration does not oscillate, while the latter explains why the limit is exactly the desired optimal solution.
