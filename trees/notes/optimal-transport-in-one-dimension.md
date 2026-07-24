---
title: Optimal Transport in One Dimension
date: 2026-07-24
type: note
tags: Optimal transport
summary: Why sorted matching and equal quantiles solve optimal transport on the real line
---

Optimal transport is traditionally introduced through the image of moving a pile of dirt: the source distribution is a heap of earth, the target distribution prescribes how that earth should end up arranged, and our job is to pick the transport plan that minimizes the total cost.

In a general space this is a genuinely hard optimization problem. On the real line, however, it becomes easy, and the answer fits into a single sentence:

> **Main result**　Positions on the real line come with a natural total order, from left to right. For the cost $c(x,y)=|x-y|^p$ (with $p\ge 1$), optimal transport obeys the principle that **mass of equal rank is matched to mass of equal rank**: in the equally weighted discrete case this means pairing up the points after sorting; in general it means matching equal quantiles.

The statement sounds reasonable enough at first glance, but there is a lot of detail hidden inside it. The thread running through this article is to make that sentence concrete, step by step, and to understand the result from both an intuitive and an analytic angle.

## 1. Notation: keep positions and masses apart

A discrete probability distribution on the real line is written
$$\alpha=\sum_{i=1}^n a_i\,\delta_{x_i}, \qquad a_i\ge 0, \qquad \sum_{i=1}^n a_i=1.$$
Here $\delta_{x_i}$ is the unit Dirac mass concentrated at $x_i$, so $a_i\delta_{x_i}$ reads "place mass $a_i$ at position $x_i$." **Positions live in the subscript of $\delta$, masses live in the coefficient**, and the two roles stay separate throughout: position tells us where, mass tells us how much.

Given $n$ sample points $x_1,\dots,x_n$, the corresponding empirical distribution is $\alpha=\frac1n\sum_{i=1}^n\delta_{x_i}$. This does not mean the points carry no mass; it means that by default every sample point carries the same mass $1/n$. If a position occurs more than once, the masses simply add up:
$$\frac14(\delta_{0.1}+\delta_{0.2}+\delta_{0.2}+\delta_{0.9}) = \frac14\delta_{0.1}+\frac12\delta_{0.2}+\frac14\delta_{0.9}.$$

## 2. The simplest case: equal weights, discrete

Take two equally weighted empirical distributions
$$\alpha=\frac1n\sum_{i=1}^n\delta_{x_i}, \qquad \beta=\frac1n\sum_{i=1}^n\delta_{y_i},$$
and sort each set of **positions**: $x_{(1)}\le\cdots\le x_{(n)}$ and $y_{(1)}\le\cdots\le y_{(n)}$.

What gets sorted here are the positions. With equal weights every point carries the same mass $\frac1n$ and is therefore equally heavy, so mass takes no part in the sorting and only reappears at the end as a coefficient. For the cost $c(x,y)=|x-y|^p$ (with $p\ge1$), one optimal plan is to pair points by rank, $x_{(i)}\to y_{(i)}$, which gives
$$W_p(\alpha,\beta) = \left( \frac1n\sum_{i=1}^n |x_{(i)}-y_{(i)}|^p \right)^{1/p}.$$
In other words, the Wasserstein distance between two equally weighted empirical distributions on the line is nothing but the normalized $\ell^p$ distance between the two **sorted coordinate vectors**:
$$W_p(\alpha,\beta) = n^{-1/p}\,\big\|(x_{(1)},\dots,x_{(n)})-(y_{(1)},\dots,y_{(n)})\big\|_p.$$

**Example.**　Let $x=(4,0,3)$ and $y=(6,2,1)$. After sorting, $x_{(\cdot)}=(0,3,4)$ and $y_{(\cdot)}=(1,2,6)$, so the optimal matching is $0\to1$, $3\to2$, $4\to6$. For $p=2$ we get $W_2^2 = \frac13(1^2+1^2+2^2)=2$, that is, $W_2=\sqrt2$.

The formula looks almost too good to be true: how can a $p$-norm between two sorted vectors possibly be enough?

The fundamental reason sorted matching is optimal is this: **for a cost that is a convex function of distance, crossing routes are never cheaper than ordered ones.** Start with just two points. Let $x_1\le x_2$ and $y_1\le y_2$, and compare the ordered matching ($x_1\to y_1$, $x_2\to y_2$) with the crossed one ($x_1\to y_2$, $x_2\to y_1$). For every $p\ge1$,
$$|x_1-y_1|^p+|x_2-y_2|^p \le |x_1-y_2|^p+|x_2-y_1|^p.$$
This is the **Monge inequality** for one-dimensional Wasserstein costs. It is intuitively easy to accept: crossing means the two routes retrace a common stretch of road twice, and uncrossing them saves exactly that duplicated stretch.

**Proof.**　Let $\varphi(t)=|t|^p$, which is convex for $p\ge1$. Write $a=x_2-x_1\ge0$, $b=y_2-y_1\ge0$ and $z=x_1-y_2$, so that the four differences are $x_1-y_2=z$, $x_1-y_1=z+b$, $x_2-y_2=z+a$ and $x_2-y_1=z+a+b$. The claimed inequality becomes
$$\varphi(z+b)+\varphi(z+a) \le \varphi(z)+\varphi(z+a+b).$$
For fixed $b\ge0$, define the increment $D_b(t)=\varphi(t+b)-\varphi(t)$. The slopes of a convex function are non-decreasing, so $D_b$ is non-decreasing; since $z+a\ge z$ we get $D_b(z+a)\ge D_b(z)$, and rearranging gives the result. $\blacksquare$

With this inequality in hand we can go further: in any plan that contains a pair matched out of order, we can isolate one such crossing (four points) and swap it by the inequality above without increasing the cost. Repeat until no crossings remain, and what is left is exactly the sorted matching. Hence no out-of-order matching can be strictly better.

Two remarks, to mark the boundaries of the result:

- **The cost must be convex** (for $c(x,y)=|x-y|^p$, the condition $p\ge1$ cannot be dropped). If $0<p<1$ then $|t|^p$ is concave and sorting may no longer be optimal. Take $x_1=0$, $x_2=1$, $y_1=1$, $y_2=2$: the ordered matching costs $1^p+1^p=2$, the crossed one costs $2^p+0$, and for $0<p<1$ we have $2^p<2$, so crossing is actually cheaper.
- **The optimal plan need not be unique.** When $p>1$, the positions are strictly increasing and the mass structure is non-degenerate, strict convexity usually yields a stronger uniqueness statement. When $p=1$ the sorted plan is still optimal, but it may be tied with others; repeated positions or intervals of zero distance can also destroy uniqueness. For instance, with $p=1$ and both source points on the same side of both target points (say $x=(2,3)$ and $y=(0,1)$), the ordered and the crossed matching both cost $4$, so the two plans are tied for optimal.

## 3. One step looser: unequal masses

Now allow arbitrary masses on both sides:
$$\alpha=\sum_{i=1}^n a_i\delta_{x_i}, \qquad \beta=\sum_{j=1}^m b_j\delta_{y_j}, \qquad x_1\le\cdots\le x_n,\quad y_1\le\cdots\le y_m.$$
At first sight the premise behind the equally weighted sorting argument is gone, and sorting no longer applies.

A moment's thought, though, reduces the problem to one we have already solved: **picture a heavy point as a large number of tiny, equally weighted points all stacked at the same position.** For example, $0.6\delta_0$ can be read as six little points of mass $0.1$ all standing at $0$. Once both sides are shattered this way we are back in the equally weighted case and sorted matching proceeds as usual. What people call "splitting one point across several targets" is nothing more than these co-located little points setting off for the same destination or for different ones.

As an algorithm this becomes the familiar "two-pointer" sweep: send a pointer along each side starting from the leftmost cell, ship $\min(\text{remaining mass on either side})$ each time, advance whichever pointer has just been emptied, and continue until the whole ruler has been traversed.

**Example.**　Let $\alpha=0.6\delta_0+0.4\delta_3$ and $\beta=0.3\delta_1+0.7\delta_2$. The sweep runs as follows. First ship $\min(0.6,0.3)=0.3$ of mass from $0$ to $1$; the first cell of $\beta$ empties and its pointer advances, while the first cell of $\alpha$ still holds $0.3$. Next ship $\min(0.3,0.7)=0.3$ from $0$ to $2$; now the first cell of $\alpha$ empties and its pointer advances, while the second cell of $\beta$ still holds $0.4$. Finally ship $\min(0.4,0.4)=0.4$ from $3$ to $2$; both sides empty simultaneously and we are done. For $p=1$ the total cost is $0.3\times1+0.3\times2+0.4\times1=1.3$. Notice that the mass at position $0$ was "split" between two targets, which is exactly what you get once you view it as a cluster of little points heading off separately.

## 4. A common language: the CDF and the quantile function

The sorted matching above is well suited to finite point sets, and the idea behind it is already the right one. But for continuous distributions, mixed distributions, or arbitrary weights, "shatter into equally weighted little points, then sort" cannot be carried over directly: a continuous distribution puts zero mass at every single point, so there are no individual "little points" to speak of, and there are infinitely many points anyway, so we cannot enumerate them one by one in order. The idea itself is fine — cut the mass into small pieces, then queue the pieces up by position — what is missing is a language general enough to state it precisely for every distribution. The tools for this section are the cumulative distribution function and its generalized inverse.

Two definitions first. Let $\alpha$ be a probability measure on the real line.

**Cumulative distribution function (CDF)**: $F_\alpha(x) = \alpha((-\infty,x])$, the mass of $\alpha$ accumulated to the left of $x$ (inclusive). For example, $\alpha=0.3\delta_0+0.7\delta_2$ gives
$$
F_\alpha(x)=
\begin{cases}
0, & x<0,\\
0.3, & 0\le x<2,\\
1, & x\ge 2.
\end{cases}
$$
Anyone who has taken a probability course will find this familiar. Its great virtue here is **universality**: discrete, continuous and mixed distributions may fail to have a density, but all of them have a CDF, which makes it a natural vehicle for a unified description.

**Quantile function** (generalized inverse):
$$
Q_{\alpha}(u)
\coloneqq
F_{\alpha}^{\leftarrow}(u)
\coloneqq
\inf\left\{
x\in\mathbb{R}
\,\middle|\,
F_{\alpha}(x)\ge u
\right\},
\qquad u\in(0,1).
$$
$Q_\alpha(u)$ is the $u$-th quantile of $\alpha$: $Q_\alpha(0.5)$ is the median, $Q_\alpha(0.25)$ the first quartile. For the example above, $Q_\alpha(u)=0$ for $0<u\le0.3$ and $Q_\alpha(u)=2$ for $0.3<u<1$. Read it intuitively as follows: feed in a cumulative probability $u$, and out comes the position at which the accumulated probability first reaches $u$ — a concrete real number.

With these two tools, let us go back and see how the "cut the mass up, then move it in order" operation of Sections 2 and 3 should be expressed.

The reason to start from the CDF, beyond the fact that every distribution has one, is a key property: it is **non-decreasing**. Walking in the positive direction along the line, accumulated mass can only grow (and if $F_\alpha$ is flat on some stretch, the distribution simply places no mass there). This means the left-to-right order of positions and the order in which mass gets accumulated agree automatically: the further left a piece of mass sits, the earlier it enters the running total.

That suggests cutting the mass along a different axis: instead of cutting by position, cut **by accumulated mass $u$**. Flatten the total mass onto the interval $(0,1)$ and slice it into infinitely many elements $\mathrm{d}u$; the quantile function $Q_\alpha(u)$ answers precisely the question "where on the line does the $u$-th element sit?" Every element has the same size, which makes this the continuum version of the equally weighted little points from Section 3 — only now the little points have become infinitesimal mass elements, and "being sorted" is guaranteed for free by the monotonicity of $F_\alpha$.

Matching then becomes easy: the $u$-th element of the source sits at $Q_\alpha(u)$, the $u$-th element of the target sits at $Q_\beta(u)$, and we simply move the former to the latter. The key reading is that **$u\in(0,1)$ is the "rank" of a piece of mass**. $F_\alpha$ translates positions into ranks, $Q_\alpha$ translates ranks back into positions; the two are a mutually inverse pair of lookup tables.

Let $\alpha,\beta\in\mathcal P_p(\mathbb R)$, i.e. both have finite $p$-th moments. For $p\ge1$,
$$W_p(\alpha,\beta)^p = \int_0^1 |Q_\alpha(u)-Q_\beta(u)|^p\,\mathrm{d}u.$$
The essence of one-dimensional optimal transport is now fully exposed: **send the $u$-th quantile of the source to the $u$-th quantile of the target**.

## 5. A bonus at $p=1$: the area between the CDFs

When $p=1$ the quantile formula can be evaluated along the other axis — instead of integrating the "horizontal" difference of quantiles, integrate the "vertical" difference of CDFs:
$$W_1(\alpha,\beta) = \int_{\mathbb R} |F_\alpha(x)-F_\beta(x)|\,\mathrm{d}x.$$
(The geometric reason the two agree: integrating $|Q_\alpha-Q_\beta|$ over $u$ and integrating $|F_\alpha-F_\beta|$ over $x$ both measure the area of the same region between two monotone curves; one slices it horizontally, the other vertically.)

There is a very physical way to read it. Fix a position $x$ and make a cut there on the line. Then $F_\alpha(x)-F_\beta(x)$ is the net discrepancy between source mass and target mass to the left of the cut. If the discrepancy is non-zero, at least $|F_\alpha(x)-F_\beta(x)|$ worth of mass has to pass through that cut. And a piece of mass travelling from $a$ to $b$ passes through exactly the cuts lying between $a$ and $b$, so integrating over all cuts adds up precisely "mass × distance travelled" — which is $W_1$.

## 6. Summary

One-dimensional optimal transport is easy because positions on the real line are totally ordered. For the convex cost $c(x,y)=|x-y|^p$ with $p\ge1$, the Monge inequality guarantees that crossings can be eliminated, so the optimal coupling must be monotone, and the whole theory collapses into a single sentence: **sort the discrete points, or equivalently, match equal quantiles**. The formula comes in three levels:

- discrete with equal weights: $W_p^p = \frac1n\sum_i|x_{(i)}-y_{(i)}|^p$;
- general distributions on the line: $W_p^p = \int_0^1|Q_\alpha(u)-Q_\beta(u)|^p\,\mathrm{d}u$;
- the special case $p=1$: $W_1 = \int_{\mathbb R}|F_\alpha(x)-F_\beta(x)|\,\mathrm{d}x$.

They are all saying the same thing. I think it finally clicks — cool!
