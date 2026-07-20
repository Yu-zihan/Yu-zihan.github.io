---
title: Does the "Neuron-Wave" Tactic Work?
date: 2026-07-20
type: note
tags: Deep learning
summary: "Part 2: From many neurons to layered networks"
---

In the last note, we mentioned wanting to design the model itself so that it can learn hidden representations on its own to handle problems. Let's not rush to solve that yet. First, let's think briefly, within the framework we've been discussing, about the representational limits of linear threshold neurons.

## The Representational Power of "Many Neurons"

Consider a simple question: does adding more neurons increase a model's expressive power? And if so, is there an intuitive way to understand why?

The answer is of course yes. Intuitively, adding neurons can at worst be reduced back to the fewer-neuron case by some means (for example, setting the extra neurons' weights to zero) — things won't get worse as you add more.

But then the question becomes: how should we add neurons for a given problem? The way neurons are connected also matters a great deal; how the extra neurons are arranged is itself a question.

From simple intuition, there are roughly these options:
- Infinite series: one neuron per layer, stacked one after another indefinitely;
- Infinite parallel: add many neurons side by side, hoping unlimited parallelism brings unlimited representational power;
- Series-parallel combination: multiple stacked layers, with several neurons per layer;
- Fully connected as a complete graph: every neuron connected to every other, forming a neural network in the shape of a complete graph.

Below we discuss the characteristics of each of these structures in turn.

## Neurons in Infinite Series

Linear threshold neurons in infinite series — think about it for a moment. Each neuron takes the single-valued output of the previous one as its input. In the linear case this is essentially still a linear equation, which makes it a rather silly scheme.

First consider the case where we drop the threshold and keep only the linear part. Let the first neuron output $s_1=w_1^\top x+b_1$, and let the second neuron take $s_1$ as input and output $s_2=w_2s_1+b_2$. Substituting and expanding: $s_2=w_2(w_1^\top x+b_1)+b_2=(w_2w_1)^\top x+(w_2b_1+b_2)$. This is still a linear function of $x$. Setting $w'=w_2w_1$ and $b'=w_2b_1+b_2$, we are right back to a single linear neuron $s=w'^\top x+b'$. No matter how many layers you chain, it's equivalent to one.

Now consider the case with the threshold kept — things get even worse. The first neuron outputs $h_1(x)=\mathbf 1[w_1^\top x+b_1>0]\in\{0,1\}$, and every subsequent neuron $h_2=\mathbf 1[wh_1+b>0]$ is just a function from $\{0,1\}$ to $\{0,1\}$. Count them: there are only four possibilities — constant $0$, constant $1$, identity, and negation. In other words, the input information gets compressed down to a single bit at the very first layer, and no amount of further chaining can recover it. Expressive power goes down, not up.

## Partitioning with Parallel Neurons

Adding neurons in parallel, as discussed in the previous note, is geometrically simple for linear threshold neurons: it amounts to partitioning the space. We use multiple neurons to carve up the space sensibly, and in a well-behaved space we can in principle carve out representations of arbitrary shape.

Concretely, $k$ parallel neurons $h_i(x)=\mathbf 1[w_i^\top x+b_i>0]$ each make one cut through the plane. For example, three lines can enclose a triangular region; in general, $k$ lines can divide the two-dimensional plane into at most $1+k+\binom{k}{2}$ cells. Which cell an input point $x$ falls into is exactly encoded by this group of neurons' outputs as a binary vector $(h_1(x),h_2(x),\dots,h_k(x))$.

Once the space has been partitioned and subdivided, a lookup table over these codes is enough to classify spatial features. This feels like a workable scheme.

You can try the following code, which shows how three neurons cut the plane into multiple regions:

```wolfram
ClearAll["Global`*"];

h[x1_, x2_, w1_, w2_, b_] := Boole[w1*x1 + w2*x2 + b > 0];

(* three neurons, three lines *)
code[x1_, x2_] := {h[x1, x2, 1, 0, 0.5], h[x1, x2, 0, 1, 0.5], h[x1, x2, -1, -1, 1.5]};

Show[
 RegionPlot[
  Evaluate[Table[code[x1, x2] == c,
    {c, Tuples[{0, 1}, 3]}]],
  {x1, -3, 3}, {x2, -3, 3},
  PlotPoints -> 80,
  FrameLabel -> {"x1", "x2"},
  BoundaryStyle -> None
 ],
 ContourPlot[{x1 + 0.5 == 0, x2 + 0.5 == 0, -x1 - x2 + 1.5 == 0},
  {x1, -3, 3}, {x2, -3, 3},
  ContourStyle -> {Red, Thick}],
 ImageSize -> Large,
 PlotLabel -> "Three neurons cut the plane into cells, each cell has a binary code"
]
```

Each colored patch corresponds to a distinct code $(h_1,h_2,h_3)$. The more neurons, the finer the cuts, and the closer the enclosed shapes get to arbitrary regions.

## Series Meets Parallel: The Emergence of Layered Networks

Based on the discussion in the previous section, parallel neurons can encode regions of the space, splitting it into distinct pieces.

Given such a split, intuitively speaking, we can apply conditional filtering to specific regions, thereby achieving a selection effect.

From the previous note we know that neurons can implement AND and OR. So with OR and AND, we can express the membership conditions for each of the partitioned regions.

Let's take an example — XOR, the very thing the previous note couldn't do. In the first layer, place two parallel neurons: $h_1(x)=\mathbf 1[x_1+x_2-0.5>0]$ implements OR, and $h_2(x)=\mathbf 1[x_1+x_2-1.5>0]$ implements AND. In the second layer, place one more neuron taking $(h_1,h_2)$ as input: $\hat y=\mathbf 1[h_1-h_2-0.5>0]$. Let's verify point by point:

|$x_1$|$x_2$|$h_1$ (OR)|$h_2$ (AND)|$\hat y=\mathbf 1[h_1-h_2-0.5>0]$|XOR|
|--:|--:|--:|--:|--:|--:|
|$0$|$0$|$0$|$0$|$0$|$0$|
|$1$|$0$|$1$|$0$|$1$|$1$|
|$0$|$1$|$1$|$0$|$1$|$1$|
|$1$|$1$|$1$|$1$|$0$|$0$|

XOR is exactly "OR holds and AND does not." The first layer does the encoding, the second layer does the filtering — two layers suffice. The feature $x_3=x_1x_2$ that required a sage to hand-craft in the previous note is here played "automatically" by the first-layer neurons.

Following this line of thought, one layer of neurons is clearly not enough; we need extra neurons to filter the initial encoding results, and this is how the layered network structure arises. Drawn as a diagram, it looks roughly like this:

```
x1 ──┬──> [h1 : OR ] ──┐
     │                 ├──> [ y : 1[h1 - h2 - 0.5 > 0] ] ──> XOR
x2 ──┴──> [h2 : AND] ──┘
```

You can try the following code to see what this two-layer network actually carves out in the plane:

```wolfram
ClearAll["Global`*"];

(* first layer: two parallel neurons *)
h1[x1_, x2_] := Boole[x1 + x2 - 0.5 > 0];  (* OR *)
h2[x1_, x2_] := Boole[x1 + x2 - 1.5 > 0];  (* AND *)

(* second layer: a filtering neuron taking (h1, h2) as input *)
xorNet[x1_, x2_] := Boole[h1[x1, x2] - h2[x1, x2] - 0.5 > 0];

Show[
 RegionPlot[
  xorNet[x1, x2] == 1,
  {x1, -0.5, 1.5}, {x2, -0.5, 1.5},
  PlotPoints -> 100,
  PlotStyle -> LightBlue,
  BoundaryStyle -> None,
  FrameLabel -> {"x1", "x2"}
 ],
 ContourPlot[
  {x1 + x2 - 0.5 == 0, x1 + x2 - 1.5 == 0},
  {x1, -0.5, 1.5}, {x2, -0.5, 1.5},
  ContourStyle -> {{Red, Thick, Dashed}, {Darker[Green], Thick, Dashed}}
 ],
 Graphics[{
   PointSize[Large],
   Blue, Point[{{1, 0}, {0, 1}}],
   Black, Point[{{0, 0}, {1, 1}}],
   Text[Style["1", Blue, 16], {1.08, 0.08}],
   Text[Style["1", Blue, 16], {0.08, 1.08}],
   Text[Style["0", Black, 16], {0.08, 0.08}],
   Text[Style["0", Black, 16], {1.08, 1.08}]
 }],
 ImageSize -> Large,
 PlotLabel -> "Two layers carve out the strip between the OR line and the AND line"
]
```

The red dashed line is the OR boundary $x_1+x_2-0.5=0$, and the green dashed line is the AND boundary $x_1+x_2-1.5=0$. The blue region is where the network outputs $1$ — precisely the strip sandwiched between the two lines: $(1,0)$ and $(0,1)$ fall inside the strip, while $(0,0)$ and $(1,1)$ fall outside. The four points that no single line could separate are separated by the strip between two lines. This is the geometric meaning of the second layer's "filtering."

But then: how do we construct such a network automatically? How many neurons should each layer have, exactly? How can this relationship be realized through automatic iteration? These remain open questions.

## How to Obtain a Usable Network Automatically

This brings us to the evaluation criterion. Generally speaking, an algorithm needs a clear criterion for judging what counts as good. Reusing the notation from the first note, that criterion is the loss function $L(\theta)=\sum_i L(f_\theta(x_i),y_i)$. But knowing what's good is not enough by itself —

we also need to iterate against the current standard and revise the current parameters.

I've thought about it back and forth, and I honestly can't derive such an algorithm from scratch on my own. So here let's stand on the shoulders of giants: the algorithms that have proven successful are gradient descent and backpropagation.

The loss $L(\theta)$ is a function of the parameters $\theta$, so we need a corresponding way to correct this function. The basic idea is to keep taking derivatives and keep adjusting the parameters in the direction that decreases the loss: $\theta_{t+1}=\theta_t-\eta\nabla_\theta L(\theta_t)$, where $\eta$ is the step size (learning rate) and $\nabla_\theta L$ is the gradient of the loss with respect to the parameters. For a layered network, the gradient is passed back layer by layer via the chain rule; for example, the gradient of some layer's parameters $\theta^{(l)}$ takes the form $\frac{\partial L}{\partial\theta^{(l)}}=\frac{\partial L}{\partial h^{(L)}}\cdot\frac{\partial h^{(L)}}{\partial h^{(L-1)}}\cdots\frac{\partial h^{(l)}}{\partial\theta^{(l)}}$. This is backpropagation; the details are left to the next note.

## Summary

First, let's take stock of the elements we now have:
- A representable input $x$, and the minimal computable model — the linear threshold neuron $h(x)=\mathbf 1[w^\top x+b>0]$;
- Pure series stacking is meaningless, while parallel neurons can partition and encode the space;
- Adding a filtering layer on top of the encoding gives us layered networks; two layers already solve XOR;
- The evaluation criterion (the loss function $L$) tells us what "good" means, and gradient descent gives us the direction to iterate;
- But the hard threshold is non-differentiable, so gradient descent can't be applied just yet.

In the next note, we will discuss backpropagation and gradient descent.

## Appendix: Fully Connected as a Complete Graph

Of the four options, full connectivity is the one we haven't discussed head-on, so let me briefly address it here. From the perspective of graph theory (graph theory being the study of abstract nodes and edges), each neuron is a node, and the communication pathways between neurons are the edges. Series and parallel are then arguably the simplest possible graph structures, so it's natural to want to level up the structure — for instance, by connecting all neurons (or some subset of them) pairwise, forming a complete graph.

This kind of structure is quite interesting, and it corresponds to Hopfield networks and Boltzmann machines: the network is no longer a feedforward "input in, output out" pipeline; rather, the network itself carries information, with states iterating back and forth among the neurons until they stabilize. These lie on a different path from the feedforward main line of this series, so we set them aside for now and will develop them separately as extension material later.
