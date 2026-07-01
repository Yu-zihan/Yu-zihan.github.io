---
title: Starting with One Neuron
date: 2026-07-01
type: note
tags: Deep learning
summary: "Part 1: From the smallest computable model to XOR"
---

## Part 1: From the Smallest Computable Model to XOR

Deep learning algorithms come in many forms. I often feel that if I start directly from the many existing algorithms, I only learn fragments. So I want to think from the beginning: start with the simplest possible structure and see how far that structure can take us. I will refer to existing materials along the way, but I want the explanation to stay as understandable as possible.

This post studies one question:

> If we start from the smallest binary classification model, what can it express, and where does it fail?

---

## 0. A Few Basic Premises of Machine Learning

Before talking about neural networks, let us ask a more basic question:

> What does a machine learning model need in order to work at all?

In my view, at least the following ingredients are necessary.

### 0.1 Learning Requires Representable Input

A machine cannot learn the real world directly. It can only learn from experience after that experience has been encoded.

For example:

- an image is represented as a matrix of pixels;
- text is represented as a sequence of tokens;
- a tabular sample is represented as a feature vector.

These representations are usually obtained through some measurement or sampling process, and then stored approximately inside a computer for further processing.

In other words, a learning algorithm needs some form of input $x$:

$$
x = (x_1,x_2,\dots,x_d)
$$

Here, $x$ is not the phenomenon itself. It is a numerical representation obtained through measurement, encoding, or sampling.

---

### 0.2 Learning Happens Inside a Computable Model Space

Machine learning does not search freely through all possible rules. We must first specify what kind of model we are using. Otherwise, what exactly is the computer supposed to compute?

A model can be written as:

$$
\hat y = f_\theta(x)
$$

where:

- $x$ is the input;
- $\hat y$ is the model output;
- $\theta$ represents the model parameters;
- $f_\theta$ is some computable function.

Learning does not create rules from nothing. It searches for suitable parameters inside a given family of models, according to some criterion.

This also means that the model itself carries a prior assumption.

For example:

- if we choose a linear model, we assume that useful patterns can be captured, at least approximately, by linear relationships;
- if we choose a Gaussian model, we assume that the relevant distribution is approximately Gaussian;
- if we choose a neural network, we assume that complex relationships can be composed from many simple computable units.

---

### 0.3 Learning Requires an Evaluation Criterion

A model needs to know what counts as “good.” Only then can it be improved.

In supervised learning, this evaluation criterion is usually a loss function:

$$
L(\hat y,y)
$$

where $y$ is the true label and $\hat y$ is the model prediction.

The learning objective can be written as:

$$
\min_\theta \sum_i L(f_\theta(x_i),y_i)
$$

Without an evaluation criterion, there is no direction for improvement.

---

### 0.4 Models Manipulate Numbers; Meaning Comes From the Task

The immediate output of a computational model is a number. The meaning of that number is assigned by humans through the task definition.

For example:

$$
\hat y = 1
$$

or:

$$
\hat y = 0.83
$$

These numbers do not carry meaning by themselves. Their meaning comes from the task.

In a spam classification task:

$$
\hat y = 1
$$

may mean “this is spam.”

In a medical classification task:

$$
\hat y = 1
$$

may mean “there is a certain risk.”

So inside a machine learning model, what is processed is numerical structure. The semantic interpretation is supplied by the task, the labels, and the human context.

---

### 0.5 Every Model Carries a Prior

There is no completely neutral learning model.

Choosing a model means choosing a way of looking at the world.

For example:

- a linear model assumes that some relationships can be approximated by linear relationships;
- a decision tree assumes that data can be partitioned by a sequence of conditional tests;
- a convolutional neural network assumes that local structure and translation sharing matter;
- a Transformer assumes that relationships between tokens can be modeled through attention.

This point is also related to the famous No Free Lunch theorem: no learning method is universally best without assumptions about the data or the task.

---

## 1. Starting From the Smallest Nontrivial Computable Model

Now let us ask what the simplest model can do.

The phrase “what can it do” is still broad. For this post, I will interpret it as:

> What kinds of functions can this simple model fit or express?

This is useful because a function is an explicit mapping between variables. It gives us a concrete way to describe a relationship, and therefore a concrete way to discuss what the model is capable of representing.

Strictly speaking, the simplest computable model could be a constant model:

$$
\hat y = 0
$$

This is certainly computable, but it does not look at the input. It does not express how the input affects the output.

So we begin with a slightly more meaningful minimal model:

> a model that receives input, has parameters, and can change its output according to the input.

A linear expression is one of the simplest computable relationships:

$$
s=w^\top x+b
$$

If we output $s$ directly, the model looks more like a regression or scoring model.

But if we are studying binary classification, we also need to turn this score into either $0$ or $1$. The simplest way to do that is to apply a threshold:

$$
h(x)=\mathbf 1[s>0]
$$

This gives us the linear threshold neuron.

---

## 2. The Linear Threshold Neuron

### 2.1 Why Start With a Linear Threshold Neuron?

Before talking about neurons, we need to clarify what this model is supposed to do.

The basic form of a machine learning model is:

$$
x \longrightarrow \hat y
$$

That is: given an input $x$, the model produces a prediction $\hat y$.

But the output can take different forms.

If $\hat y$ is a continuous value, such as a house price, a temperature, or a risk score, then we are dealing with a regression or scoring problem.

If $\hat y$ is a category, such as “yes/no,” “positive/negative,” or “cat/dog,” then we are dealing with a classification problem.

This post starts with the smallest classification problem: binary classification.

That is:

$$
y\in\{0,1\}
$$

In this setting, the model has a very specific task:

> given an input $x$, decide whether it belongs to class $0$ or class $1$.

---

### 2.2 What Does a Binary Classification Model Need?

From the premises above, a simple model can be written as:

$$
\hat y = f_\theta(x)
$$

For a classification model, the final output is a category. But before producing a category, the model usually needs to compute something from the input.

The simplest kind of computation is a linear computation.

So a minimal binary classification model needs two steps:

1. compute a score from the input $x$;
2. convert that score into class $0$ or class $1$.

That is:

$$
x \longrightarrow s \longrightarrow \hat y
$$

Here, $s$ is an internal score computed by the model, and $\hat y$ is the final classification result.

---

### 2.3 Definition and Structure of a Linear Threshold Neuron

Combining the two steps gives the linear threshold neuron.

First, compute a linear score:

$$
s=w^\top x+b
$$

Second, apply a threshold:

$$
h(x)=\mathbf 1[s>0]
$$

Let us look more carefully at the second step. Once a score has been computed, a binary classifier needs to turn it into either $0$ or $1$. A natural way to do this is to use a piecewise rule.

More generally, we could write:

$$
h(x)=\mathbf 1[s>t]
$$

That is:

$$
h(x)=\mathbf 1[w^\top x+b>t]
$$

Move $t$ to the left-hand side:

$$
h(x)=\mathbf 1[w^\top x+(b-t)>0]
$$

Let:

$$
b'=b-t
$$

Then we are back to:

$$
h(x)=\mathbf 1[w^\top x+b'>0]
$$

So writing the threshold as $0$ does not lose generality. The threshold can always be absorbed into the bias term.

A linear threshold neuron can therefore be understood as:

> a minimal binary classification model that first computes a linear score and then applies a threshold.

It contains two assumptions.

The first assumption is that the input can be described by a linear score:

$$
s=w^\top x+b
$$

In other words, the model assumes that the input features can be combined by a weighted sum into a meaningful decision score.

The second assumption is that classification can be completed by thresholding this score:

$$
h(x)=\mathbf 1[s>0]
$$

In other words, once the score crosses a certain critical value, the input belongs to one class; otherwise, it belongs to the other class.

Putting the two steps together:

$$
x \longrightarrow s=w^\top x+b \longrightarrow h(x)=\mathbf 1[s>0]
$$

This is the complete logic of a linear threshold neuron.

The following Wolfram Language code visualizes how a single neuron divides a two-dimensional plane with a line.

```wolfram
ClearAll["Global`*"];

score2D[x1_, x2_, w1_, w2_, b_] := w1*x1 + w2*x2 + b;
neuron2D[x1_, x2_, w1_, w2_, b_] := Boole[score2D[x1, x2, w1, w2, b] > 0];

Manipulate[
 Show[
  RegionPlot[
   neuron2D[x1, x2, w1, w2, b] == 1,
   {x1, -3, 3},
   {x2, -3, 3},
   PlotPoints -> 60,
   FrameLabel -> {"x1", "x2"},
   PlotStyle -> LightBlue,
   BoundaryStyle -> None
  ],
  ContourPlot[
   score2D[x1, x2, w1, w2, b],
   {x1, -3, 3},
   {x2, -3, 3},
   Contours -> {0},
   ContourStyle -> {Red, Thick},
   ContourShading -> False
  ],
  PlotRange -> {{-3, 3}, {-3, 3}},
  ImageSize -> Large,
  PlotLabel -> "A linear threshold neuron cuts the plane into two half-spaces"
 ],
 {{w1, 1, "w1"}, -3, 3, 0.1, Appearance -> "Labeled"},
 {{w2, 1, "w2"}, -3, 3, 0.1, Appearance -> "Labeled"},
 {{b, 0, "b"}, -3, 3, 0.1, Appearance -> "Labeled"}
]
```

The red line is:

$$
w_1x_1+w_2x_2+b=0
$$

The blue region is:

$$
w_1x_1+w_2x_2+b>0
$$

This shows that a neuron is not “understanding” the points in the plane. It is using one linear condition to cut the plane into two sides.

---

## 3. The Expressive Limit of a Single Linear Threshold Neuron

Because a linear threshold neuron can only produce one linear boundary, it can only solve linearly separable binary classification problems.

If there exists some $w,b$ such that all positive samples lie on one side of the boundary and all negative samples lie on the other side, then the problem is linearly separable.

In that case, a linear threshold neuron may be able to classify the data.

But if the positive and negative samples cannot be separated by a single line, then a linear threshold neuron cannot solve the problem.

This is not a matter of training technique. It is a limitation of the model’s expressive power. No matter how we train it, the model cannot represent what is not inside its model space.

A classic way to see this limitation is to test the neuron on simple logical functions.

At first, this may feel counterintuitive. Why jump from a mathematical model to logical functions? After all, AND, OR, and XOR can be computed perfectly well by digital circuits.

The point is not to replace logic gates with neurons.

> The point is to check what this minimal model can and cannot express.

Now assume the input space is two-dimensional. AND, OR, and XOR all take two binary inputs:

$$
x_1,x_2\in\{0,1\}
$$

Their outputs are also binary:

$$
y\in\{0,1\}
$$

So they are minimal classification tasks.

Each task has only four possible input points:

$$
(0,0),(1,0),(0,1),(1,1)
$$

These four points are the corners of a square in the two-dimensional plane.

Thus, a logical problem becomes a classification problem:

> Can we draw a line that separates the points with output $1$ from the points with output $0$?

Now let us look at the truth tables. A truth table simply tells us which output corresponds to each input.

AND:

| $x_1$ | $x_2$ | AND |
|---:|---:|---:|
| $0$ | $0$ | $0$ |
| $1$ | $0$ | $0$ |
| $0$ | $1$ | $0$ |
| $1$ | $1$ | $1$ |

OR:

| $x_1$ | $x_2$ | OR |
|---:|---:|---:|
| $0$ | $0$ | $0$ |
| $1$ | $0$ | $1$ |
| $0$ | $1$ | $1$ |
| $1$ | $1$ | $1$ |

XOR:

| $x_1$ | $x_2$ | XOR |
|---:|---:|---:|
| $0$ | $0$ | $0$ |
| $1$ | $0$ | $1$ |
| $0$ | $1$ | $1$ |
| $1$ | $1$ | $0$ |

The result is simple. AND and OR can both be separated by a single line, so they are linearly separable.

But XOR places its outputs on opposite diagonals of the square. A single line cannot separate the positive and negative samples.

We can also prove this algebraically.

Assume that there exists a neuron:

$$
h(x)=\mathbf 1[w_1x_1+w_2x_2+b>0]
$$

that implements XOR.

Since:

$$
(0,0)\mapsto 0
$$

we must have:

$$
b\le 0
$$

Since:

$$
(1,0)\mapsto 1
$$

we must have:

$$
w_1+b>0
$$

Since:

$$
(0,1)\mapsto 1
$$

we must have:

$$
w_2+b>0
$$

Adding the last two inequalities gives:

$$
w_1+w_2+2b>0
$$

Since $b\le 0$, we have:

$$
w_1+w_2+b>0
$$

But XOR also requires:

$$
(1,1)\mapsto 0
$$

so we must have:

$$
w_1+w_2+b\le 0
$$

This is a contradiction.

Therefore, a single linear threshold neuron cannot implement XOR. This is the simplest example of its expressive limitation.

---

## 4. After the Linear Threshold Neuron Fails

After XOR fails, we could of course abandon the model. We could write a special XOR rule, use a decision tree, or even go back to logic gates.

But a clever logician might have a “Eureka” moment and directly write down a useful expression:

$$
s=x_1+x_2-2x_1x_2
$$

Let us check it:

| $x_1$ | $x_2$ | $x_1x_2$ | $s=x_1+x_2-2x_1x_2$ | XOR |
|---:|---:|---:|---:|---:|
| $0$ | $0$ | $0$ | $0$ | $0$ |
| $1$ | $0$ | $0$ | $1$ | $1$ |
| $0$ | $1$ | $0$ | $1$ | $1$ |
| $1$ | $1$ | $1$ | $0$ | $0$ |

This expression does distinguish XOR.

If we add a threshold:

$$
h(x)=\mathbf 1[x_1+x_2-2x_1x_2-0.5>0]
$$

then it fully implements XOR.

But there is a problem. This expression is not linear in the original inputs $x_1,x_2$, because it contains a product term:

$$
x_1x_2
$$

In other words, in the original two-dimensional space, we still did not find a line that separates XOR.

What the logician secretly did was introduce a new feature:

$$
x_3=x_1x_2
$$

The original input:

$$
(x_1,x_2)
$$

is transformed into a three-dimensional feature representation:

$$
\phi(x)=(x_1,x_2,x_1x_2)
$$

or equivalently:

$$
\phi(x)=(x_1,x_2,x_3)
$$

where:

$$
x_3=x_1x_2
$$

Now the expression that looked nonlinear:

$$
x_1+x_2-2x_1x_2-0.5
$$

can be rewritten as:

$$
x_1+x_2-2x_3-0.5
$$

This expression is linear in the new feature space $(x_1,x_2,x_3)$.

In other words:

> **We did not change the form of the linear model. We changed the input representation.**

The original model could not do this:

$$
h(x)=\mathbf 1[w_1x_1+w_2x_2+b>0]
$$

But after adding the new feature, the model becomes:

$$
h(x)=\mathbf 1[w_1x_1+w_2x_2+w_3x_3+b>0]
$$

Take:

$$
w_1=1,\quad w_2=1,\quad w_3=-2,\quad b=-0.5
$$

Then:

$$
h(x)=\mathbf 1[x_1+x_2-2x_3-0.5>0]
$$

Since:

$$
x_3=x_1x_2
$$

this is equivalent to:

$$
h(x)=\mathbf 1[x_1+x_2-2x_1x_2-0.5>0]
$$

This shows something important:

> XOR is not linearly separable in the original two-dimensional space, but after a feature transformation, it becomes linearly separable in a new three-dimensional feature space.

In the original space, we only have two coordinates:

$$
(x_1,x_2)
$$

The four points are:

$$
(0,0),(1,0),(0,1),(1,1)
$$

These four points cannot be separated by a single line.

But in the new feature space, they become:

| Original input | New feature $x_3=x_1x_2$ | 3D feature point | XOR |
|---|---:|---|---:|
| $(0,0)$ | $0$ | $(0,0,0)$ | $0$ |
| $(1,0)$ | $0$ | $(1,0,0)$ | $1$ |
| $(0,1)$ | $0$ | $(0,1,0)$ | $1$ |
| $(1,1)$ | $1$ | $(1,1,1)$ | $0$ |

In this three-dimensional space, a single plane separates the positive and negative samples:

$$
x_1+x_2-2x_3-0.5=0
$$

One side of the plane outputs $1$, and the other side outputs $0$.

So we can say:

> A nonlinear problem does not always require a nonlinear classifier.  
> Sometimes we can first apply a nonlinear feature transformation, and then continue using a linear classifier in the transformed feature space.

The following Wolfram Language code visualizes this three-dimensional feature space.

```wolfram
ClearAll["Global`*"];

(* Original XOR inputs *)
rawPoints = {{0, 0}, {1, 0}, {0, 1}, {1, 1}};
labels = {0, 1, 1, 0};

(* New feature: x3 = x1 x2 *)
featurePoint[{x1_, x2_}] := {x1, x2, x1*x2};

points3D = featurePoint /@ rawPoints;

pos = Pick[points3D, labels, 1];
neg = Pick[points3D, labels, 0];

plane =
 ContourPlot3D[
  x1 + x2 - 2*x3 - 0.5 == 0,
  {x1, -0.2, 1.2},
  {x2, -0.2, 1.2},
  {x3, -0.2, 1.2},
  ContourStyle -> Directive[Opacity[0.35], Red],
  Mesh -> None
 ];

points =
 Graphics3D[
  {
   Blue, PointSize[Large], Point[pos],
   Black, PointSize[Large], Point[neg],
   
   Text[Style["1", Blue, 16], # + {0.05, 0.05, 0.05}] & /@ pos,
   Text[Style["0", Black, 16], # + {0.05, 0.05, 0.05}] & /@ neg
  }
 ];

Show[
 plane,
 points,
 Axes -> True,
 AxesLabel -> {"x1", "x2", "x3 = x1 x2"},
 BoxRatios -> {1, 1, 1},
 PlotRange -> {{-0.2, 1.2}, {-0.2, 1.2}, {-0.2, 1.2}},
 ImageSize -> Large,
 PlotLabel -> "XOR becomes linearly separable after adding x3 = x1 x2"
]
```

But one problem remains. The new feature was designed by the logician.

We can ask why this feature works. A possible explanation is: XOR means that the two inputs are different, while $x_1x_2$ detects whether both inputs are $1$. Subtracting twice this term corrects the OR-like score.

But such insights are not always easy to find. For a complex problem, we may not know what feature we should construct by hand.

So the next question is:

> Can we design a model that learns new features by adjusting its parameters?

If the answer is yes, that would be powerful.

It would mean that we do not always need to wait for a clever hand-designed feature. Instead, we can build a model that starts from the raw input and gradually learns intermediate representations.

That is the question for the next post.
