---
title: "Notes on Imprecise Probability (II): Philosophy of Decision Making and Choice Functions"
date: 2026-09-30
type: note
tags: Imprecise probability
summary: "From partial preferences and desirable gambles to maximality, E-admissibility, and the geometry of choice functions"
---

This is the second note in my series of notes from the Imprecise Probability Summer School. This one is mainly about the philosophy of choice in decision making. The choice-function framework can be viewed as an extension of the idea of desirable gambles from binary comparisons to more general set-valued choice: desirable gambles more naturally describe “which of two options is better,” while a choice function directly asks “which options in a set should not be rejected.” There is a long list of axioms and properties later on. I am not particularly interested in those, and quite a few of them also have fairly intuitive geometric interpretations, so this note will mainly discuss the general idea and only include the minimum amount of necessary mathematics. (To keep my flag of updating once every month, I rushed this out today. I almost forgot that today is the last day of September. The mathematical details were written by GPT; the intuition is mine.)

## Logic in Imprecise Probability

A claim should always come with a corresponding chain of reasoning: where the concept comes from, why it is defined in this way, and how one can defend the claim. As long as the reasoning process is sufficiently rigorous and complete, that is enough. The development of imprecise probability itself has also always carried a strong flavour of the philosophy of probability and decision theory.

Some research starts from rational choice, axioms, or preference relations, and then derives representations in terms of probabilities or imprecise probabilities. Other work starts from uncertainty models such as sets of probability distributions or lower previsions, and then studies what kinds of decision rules they induce. There is no unique narrative order that one has to follow, so this note will still start from how I personally feel when making decisions.

Suppose there are several options in front of me. When I finally make a decision, what first appears in my head is often not a very specific numerical value, but some kind of preference relation. The problem is that this preference may not be complete enough, and may not even be able to rank all the options stably into a total order. For example, I may clearly think that A is better than C, and also clearly think that B is better than C, but between A and B, because there is not enough information, I may have no sufficient reason to believe that one must be better than the other.

This is actually closer to the idea of imprecise probability than saying that “comparisons eventually lead to contradictions.” The key point is not necessarily that a person’s preferences become cyclic, but that **when the evidence is insufficient, we may simply not be entitled to compare certain options at all**. Partial preference relations are therefore very natural, and there is no need to force everything into a single ranking.

Then it is natural to look for some mathematical objects that can represent both “comparisons that can already be made” and “comparisons that cannot yet be made.” Here, one intuition needs to be corrected slightly: introducing imprecise probability is not meant to make our belief more precise. Quite the opposite, it allows us to **avoid manufacturing additional precision when the available information is insufficient**.

For example, instead of forcing ourselves to specify a unique probability distribution p, we can simply assume that the true probability model belongs to some set P. This set is usually called a credal set. Different p represent different precise beliefs that have not yet been ruled out by the current information. Similarly, objects such as lower previsions and sets of desirable gambles can also be used to represent such incomplete beliefs. There are many representation relationships among these objects, so “imprecise probability” itself is more like a large bag containing many different kinds of mathematical models, rather than one unique mathematical model.

This is both an advantage and a disadvantage. The advantage is that it is very inclusive: many things can be described by saying, “Oh, this is an imprecise-probability method,” even though the researchers themselves may not say that they are working on IP. The disadvantage is that it is also too general, and people within the field can have very different tastes. So for me, applying IP to a specific domain seems like a more reliable direction.

## Choice Functions

Let me first talk about gambles. Strictly speaking, a gamble is not a “strategy” itself, but a function mapping possible states to rewards or utilities. A strategy or act will usually induce a gamble under a given model. Suppose the state space is X. A gamble f can simply be understood as follows: if the final state is x, then I receive f(x).

Now suppose I am given a finite set of candidates A. What a choice function does is not to find “all valid gambles,” but to return those options in A that **cannot be rejected** under the current decision rule. The simplest way to write this is:

$$\varnothing\neq C(A)\subseteq A.$$

Equivalently, one can define a rejection function:

$$R(A)=A\setminus C(A).$$

So essentially, a choice function answers the question: “Given this set A of candidate options, which options should I still keep?” It can naturally return multiple elements and does not require that only one option remain in the end.

Now consider a candidate set A. The gambles that are not strictly beaten by any other option can be retained:

$$C_D(A)=\{f\in A:(\forall g\in A)\;g-f\notin D\}.$$

So instead of saying that a choice function is a “more refined desirable function,” it is more accurate to say that **desirability gives us a very natural way to make binary comparisons, while a choice function generalises this idea to set-valued, non-binary choice problems.** A general coherent choice function can even be represented through combinations of choice rules associated with a collection of coherent desirable sets, rather than depending on only one D.

### From a Geometric Point of View

I personally prefer to think about this problem geometrically.

First, consider a precise probability distribution p, and for the moment interpret the values of gambles directly as utilities. To decide which of two options g and f is better, we can compare the expectation of their difference:

$$E_p[g-f]=\sum_{x\in X}p(x)(g(x)-f(x)).$$

If this quantity is greater than 0, then we regard g as better than f under p.

Once p is fixed, the expectation operator is essentially a linear functional. Therefore, all directions with strictly positive expectation form:

$$H_p=\{h:E_p[h]>0\}.$$

This is an open half-space in a linear space. So geometrically, many choice problems under precise probability really reduce to asking “on which side of a half-space does a certain vector lie?”

There is also a more basic requirement that does not even need probability. If g is strictly better than f in every possible state, then regardless of what the belief is, there is little reason to choose f while rejecting g. This is the simplest form of the dominance idea, and it is also one of the basic intuitions behind the coherence conditions for desirable gambles.

Then what happens if the probability itself is imprecise, and all we know is that p belongs to a credal set P?

In this case, we cannot simply describe the situation as “the intersection of two cases,” because different decision rules use P in different ways. Two typical examples are maximality and E-admissibility. Troffaes gives a fairly systematic treatment of different decision criteria under imprecise probability, while the later choice-function literature places these rules into a unified choice-function framework.

The idea of **maximality** is quite straightforward: we only have sufficient reason to reject f if there exists another option g such that every probability model in the credal set considers the expected value of g to be larger than that of f:

$$C_{\mathrm M}(A)=\{f\in A:\nexists g\in A\text{ such that }(\forall p\in P)\ E_p[g]>E_p[f]\}.$$

From a geometric point of view, if we let h=g-f, then saying that “g is better than f under every p” is equivalent to saying that h lies in all the corresponding positive-expectation half-spaces simultaneously:

$$h\in\bigcap_{p\in P}H_p.$$

So intersections of half-spaces, convex cones, and dominance relations naturally appear here. This is also why a lot of the theory of desirable gambles and choice functions looks so geometric.

Another very common rule is **E-admissibility**. Its criterion is different: as long as there exists at least one probability model p that is still considered possible, under which f maximises expected value, then f is retained:

$$C_{\mathrm E}(A)=\{f\in A:(\exists p\in P)\ f\in\operatorname*{arg\,max}_{g\in A}E_p[g]\}.$$

These two rules are not the same. Under maximality, rejecting f requires finding a g that beats f uniformly under every p. E-admissibility, on the other hand, requires only that f be optimal under at least one p. Therefore, the set retained by E-admissibility is usually contained in the set retained by maximality.

I think this distinction captures the flavour of imprecise probability quite well: **a set of probabilities does not automatically tell you how you should make a decision; you still need to specify a decision rule.** Choice functions provide a very general language in which these different rules can all be described as answering the question “given A, which options remain?” E-admissibility and maximality are simply special cases.

So my original intuition that “a choice function takes all possible strategies and, based on our current knowledge of the probability distribution, removes all the useless ones” was roughly correct. A more precise way to say it would be:

> A choice function uses the currently adopted preference model or decision criterion to eliminate options that can be judged unacceptable from a candidate set, and returns all options that have not yet been rejected.

Moreover, a choice function does not necessarily have to come from a probability model. In a more general theory, the direction can actually be reversed: choice behaviour or preference can be treated as the primitive object, and we can then study under what conditions it can be represented in terms of sets of desirable gambles, lower previsions, or probability models. The representation results of De Bock and de Cooman are doing exactly this.

Even after obtaining a choice function, we do not necessarily need to “choose one more time.” If C(A) contains multiple elements, this can simply mean that, under the current information and decision criterion, there is not yet sufficient reason to distinguish further among these options. Only if the real task forces us to execute exactly one option do we need to introduce additional information, a tie-breaking rule, or a stronger decision principle.

I will skip the other axioms involving coherence, Archimedeanity, mixing, and so on for now. Of course, these are not purely formal games: they determine what kinds of objects a choice function can ultimately be represented by, such as strict preference orders, lexicographic probabilities, coherent lower previsions, or linear previsions. But if the only goal is to understand where choice functions sit within IP, I think the geometric picture above is already enough.

## Summary

In the imprecise-probability literature I have encountered so far, quite a large proportion of the work does indeed have a taste for decision making: first put an option or gamble into a linear space, represent incomplete information using sets, and then use axioms such as coherence to study these sets and the corresponding choice rules.

Linear spaces are of course convenient, and efficient. Expectation is linear, probability constraints often produce half-spaces, and combining multiple models gives intersections of half-spaces. As a result, many problems naturally become problems involving convex sets, convex cones, and linear programming.

But using a linear structure in the mathematical representation does not mean that the mechanism of the real world itself is linear. Real-world problems are of course very often nonlinear. It is just that we often first simplify a complex real-world process, and then represent the final outcome as a gamble or a utility-valued option. Only at that level do we obtain a linear structure that we can exploit. In other words, in many cases we are not pretending that the real world is linear. Instead, we are looking for an appropriate representation that makes the part we actually need to deal with linear.

When I was studying communication theory, one of my lecturers once said that there is noise in the world, but noise also gives us our jobs, because if there were no noise, transmitting and receiving signals would not involve much technical content.

The world is complicated. Abstracting simple mathematical models from a complicated world, while still making them useful enough to guide practice, is a very interesting thing. Turning unknown problems into known ones, linearising the parts that can be linearised, admitting “I still don’t know” when a complete comparison cannot be made, while at the same time making as much use as possible of the information we already have.

I think being able to correctly identify the main issue in a complicated problem is where both the difficulty and the fun of science lie.
