---
title: Conformal Prediction from the Perspective of the Probability Integral Transform (PIT)
date: 2026-05-16
type: note
tags: Conformal prediction
summary: Understanding CP from the PIT perspective
---

This note records my preliminary understanding of the relationship between Conformal Prediction (CP) and Optimal Transport (OT) in the paper (arXiv:2502.03609). The goal is not to reproduce all the proofs, but to connect the key intuitions.

## 1. Why Start from “Distributional Transformation”?

Many traditional explanations of CP begin with the algorithmic procedure: defining scores, computing quantiles, and constructing prediction sets. The paper takes a different entry point: it first asks how to transform a random variable into a uniform distribution, and then returns to CP.

The significance of this step is that:

- CP is essentially comparing the relative position of a new sample score among historical scores;
- mapping to a uniform distribution expresses this relative position in a more geometric and unified form.

## 2. What the Probability Integral Transform (PIT) Says

Let the random variable $Z$ have CDF $F$. The classical result is:

$$
F(Z) \sim \mathrm{Unif}(0,1).
$$

That is, $F(Z)$ is uniformly distributed on $(0,1)$. Therefore,

$$
\mathbb{P}(F(Z) \in [a,b]) = b-a.
$$

Define the set

$$
R_\alpha = \{z \in \mathbb{R}: F(z) \in [a,b]\}.
$$

Then $Z \in R_\alpha$ is equivalent to saying that $F(Z)$ falls within the interval $[a,b]$.

Intuitively, this rewrites a regional event in the original space as an interval event for a uniform random variable. As a result, coverage control can be converted into control over interval length, or equivalently over a threshold.

## 3. Returning to CP: Score Functions and Set-Valued Prediction

In CP, we usually have a score function

$$
Z = S(X,Y),
$$

where $X$ is the input and $Y$ is a candidate output. After fixing $x$, the prediction set can be written as

$$
R_\alpha(x) = \{y: F\!\circ\! S(x,y) \in [a,b]\}.
$$

This is essentially a **set-valued function**: different values of $x$ correspond to different acceptable regions of $y$. This is precisely the core form of CP prediction sets.

## 4. The True $F$ Is Unavailable in Practice: Using the Empirical Distribution $F_n$

The true distribution function is usually unknown, so we use the empirical distribution function

$$
F_n(z)=\frac{1}{n}\sum_{i=1}^n \mathbf{1}\{Z_i \le z\}.
$$

For a new score $Z$, $F_n(Z)$ can be interpreted as the proportion of samples whose scores are no larger than it; in other words, it gives a rank or quantile perspective.

This step is essentially consistent with the standard explanation of CP: it relies on exchangeability to guarantee finite-sample coverage.

## 5. My Current Intuition About the Paper’s Contribution

My understanding is that the paper generalizes, or replaces, the PIT-based step of mapping through $F$ with the geometric perspective of an OT map $T$.

In one sentence:

- Traditional formulation: use $F$ to push a random variable into uniform coordinates, then perform threshold comparison;
- Paper’s formulation: use an OT map $T$ to push a distribution to a target reference distribution, which can be understood as a more general “uniformized” or “standardized” space, and then perform comparison in that space.

This makes it easier to connect CP coverage control with geometric structure, transport costs, and the “shape” of high-dimensional spaces.

## 6. Remarks

This is a conceptual-level note. Its main focus is to connect the intuition among PIT $\leftrightarrow$ empirical distributions $\leftrightarrow$ the ranking mechanism in CP $\leftrightarrow$ the OT perspective.

If I continue reading, I will add two parts:

1. the precise construction conditions and computability of the OT map $T$ in the paper;
2. a one-to-one correspondence with classical split conformal prediction in terms of implementation and sources of error.
