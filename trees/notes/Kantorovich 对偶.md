
在最优化中，对偶问题一直是一个有效的解决思路，在计算最优传输这本书中有提到，但是这本书对于对偶过程写得实在太简洁了，对于优化知识的研究者来说太不友好了，我学习了一下相关知识，然后对这部分进行注释性的笔记，也加深自己的理解。

## 1. 离散最优传输问题

设有两个离散概率分布：
$a=(a_1,\dots,a_n)\in \mathbb R_+^n, \, b=(b_1,\dots,b_m)\in \mathbb R_+^m,$
满足
$\sum_{i=1}^n a_i=\sum_{j=1}^m b_j.$
设运输代价矩阵为$C=(C_{ij})\in \mathbb R^{n\times m}.$
其中 $C_{ij}$ 表示从源点 $i$ 向目标点 $j$ 运输单位质量的代价。
运输计划记为
$P=(P_{ij})\in \mathbb R_+^{n\times m},$

其中 $P_{ij}\ge 0$ 表示从 $i$ 运到 $j$ 的质量。
Kantorovich 最优传输问题为
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
矩阵形式为
$$
P\mathbf 1_m=a,
\qquad
P^T\mathbf 1_n=b,
\qquad
P\ge 0.
$$
记 primal 最优值为
$$
p^\star
=
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\langle C,P\rangle.
$$
## 2. 引入拉格朗日量

约束优化的基本想法是：把等式约束乘上拉格朗日乘子后加进目标函数。
在可行域上，约束项等于 0，所以这样做不会改变原目标函数。
对约束
$$
\sum_j P_{ij}=a_i
$$
引入乘子 $f_i$，对约束
$$
\sum_i P_{ij}=b_j
$$
引入乘子 $g_j$。
由于这些都是等式约束，$f_i$ 和 $g_j$ 没有正负限制。
定义拉格朗日量：
$$
\mathcal L(P,f,g)
=
\sum_{i,j}C_{ij}P_{ij}
+
\sum_i f_i\left(a_i-\sum_jP_{ij}\right)
+
\sum_j g_j\left(b_j-\sum_iP_{ij}\right).
$$
如果 $P$ 是 primal 可行的，那么
$$
a_i-\sum_jP_{ij}=0,
\qquad
b_j-\sum_iP_{ij}=0.
$$
因此对任意 $f,g$，都有
$$
\mathcal L(P,f,g)=\langle C,P\rangle.
$$
这说明：**拉格朗日量在原可行域上与原目标函数相等。**
## 3. 整理拉格朗日量

展开并整理 $P_{ij}$ 的系数：
$$
\mathcal L(P,f,g)
=
\sum_{i,j}C_{ij}P_{ij}
+\sum_i f_i a_i
-\sum_{i,j}f_iP_{ij}
+\sum_j g_j b_j
-\sum_{i,j}g_jP_{ij}.
$$
所以
$$
\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle
+\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij}.
$$
记
$$
s_{ij}=C_{ij}-f_i-g_j.
$$
则
$$
\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle
+\sum_{i,j}s_{ij}P_{ij}.
$$
这里的 $s_{ij}$ 是 dual 约束的松弛量，也叫 slack。
## 4. 为什么拉格朗日量会给出下界

虽然 $\mathcal L(P,f,g)$ 在 primal 可行域上等于 $\langle C,P\rangle$，但对偶推导并不是只在可行域上看它。
定义对偶函数：
$$
d(f,g)=\inf_{P\ge0}\mathcal L(P,f,g).
$$
注意这里已经放松了边缘约束，只保留了
$$
P\ge0.
$$
因为
$$
\{P\ge0,\ P\mathbf 1=a,\ P^T\mathbf 1=b\}
\subseteq
\{P\ge0\},
$$
所以在更大的集合上取 inf，只会更小或相等：
$$
\inf_{P\ge0}\mathcal L(P,f,g)
\le
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\mathcal L(P,f,g).
$$
而在 primal 可行域上，
$$
\mathcal L(P,f,g)=\langle C,P\rangle.
$$
因此
$$
d(f,g)\le p^\star.
$$
所以 $d(f,g)$ 是 primal 最优值的一个下界。
对偶问题就是寻找最紧的下界：
$$
\max_{f,g}d(f,g).
$$
## 5. 计算对偶函数

由
$$
\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle
+\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij}
$$
可知，对 $P\ge0$ 取 inf 时，每个 $P_{ij}$ 的行为由系数
$$
C_{ij}-f_i-g_j
$$
决定。
### 情况一：存在负系数

如果存在某个 $(i,j)$，使得
$$
C_{ij}-f_i-g_j<0,
$$
那么令
$$
P_{ij}\to +\infty,
$$
就有
$$
(C_{ij}-f_i-g_j)P_{ij}\to -\infty.
$$
因此
$$
d(f,g)=-\infty.
$$
这种 $(f,g)$ 给不出有意义的下界。
### 情况二：所有系数非负

如果对所有 $(i,j)$ 都有
$$
C_{ij}-f_i-g_j\ge0,
$$
也就是
$$
f_i+g_j\le C_{ij},
$$
那么
$$
\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij}\ge0.
$$
因此
$$
\inf_{P\ge0}\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle.
$$
这里的 inf 在 $P=0$ 处达到。注意 $P=0$ 一般不是 primal 可行解，但它属于放松后的集合 $P\ge0$。
## 6. 得到 Kantorovich 对偶问题

由上一节可得：为了使对偶函数有限，必须要求
$$
f_i+g_j\le C_{ij},\qquad \forall i,j.
$$
在此条件下，
$$
d(f,g)=\langle f,a\rangle+
\langle g,b\rangle.
$$
因此 Kantorovich 对偶问题为
$$
\max_{f,g}\ \langle f,a\rangle+
\langle g,b\rangle
$$
subject to
$$
f_i+g_j\le C_{ij},\qquad \forall i,j.
$$
也可以写成
$$
L_C(a,b)
=
\max_{(f,g)\in \mathcal R(C)}
\langle f,a\rangle+
\langle g,b\rangle,
$$
其中
$$
\mathcal R(C)
=
\left\{(f,g)\in\mathbb R^n\times\mathbb R^m:
f_i+g_j\le C_{ij},\ \forall i,j\right\}.
$$
这里的 $f,g$ 称为 **Kantorovich potentials**，即 Kantorovich 势函数。
## 7. 弱对偶的直接理解

如果 $(f,g)$ 满足
$$
f_i+g_j\le C_{ij},
$$
那么对任意 primal 可行的 $P$，都有
$$
\sum_{i,j}C_{ij}P_{ij}
\ge
\sum_{i,j}(f_i+g_j)P_{ij}.
$$
右边利用边缘约束展开：
$$
\sum_{i,j}(f_i+g_j)P_{ij}
=
\sum_{i,j}f_iP_{ij}+
\sum_{i,j}g_jP_{ij}.
$$
因为
$$
\sum_jP_{ij}=a_i,
\qquad
\sum_iP_{ij}=b_j,
$$
所以
$$
\sum_{i,j}f_iP_{ij}
=
\sum_i f_i a_i
=\langle f,a\rangle,
$$
$$
\sum_{i,j}g_jP_{ij}
=
\sum_j g_j b_j
=\langle g,b\rangle.
$$
因此
$$
\langle C,P\rangle
\ge
\langle f,a\rangle+
\langle g,b\rangle.
$$
这说明任意 dual feasible 的 $(f,g)$ 都给出 primal 运输成本的下界。
所以
$$
\max_{f_i+g_j\le C_{ij}}
\langle f,a\rangle+
\langle g,b\rangle
\le
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\langle C,P\rangle.
$$
这就是弱对偶。
## 8. 强对偶

由于离散 OT 是有限维线性规划，在可行且最优值有限的条件下，线性规划强对偶成立。因此
$$
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\langle C,P\rangle
=
\max_{f_i+g_j\le C_{ij}}
\langle f,a\rangle+
\langle g,b\rangle.
$$
也就是说，最好的下界正好等于 primal 的最小运输成本。
#### 用 Farkas 引理证明线性规划强对偶
考虑一个一般形式的线性规划 primal：
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
它的 weak dual 是：
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
由弱对偶可知：
$$
d^\star \le z^\star.
$$
现在要证明反向不等式：
$$
d^\star \ge z^\star.
$$
### Farkas 引理
对于矩阵 $A\in \mathbb R^{m\times n}$ 和向量 $b\in \mathbb R^m$，下面两个命题有且只有一个成立：
1. 存在 $x\in\mathbb R^n$，使得
$$
Ax=b,\qquad x\ge 0.
$$
2. 存在 $y\in\mathbb R^m$，使得
$$
A^T y\le 0,
\qquad
b^T y>0.
$$
几何上，第一种情况表示 $b$ 在 $A$ 的列向量张成的非负锥内；第二种情况表示存在一个超平面把 $b$ 和这个锥分开。
### 从 Farkas 引理到强对偶
设 primal 的最优解为 $x^\star$，最优值为
$$
z^\star=c^T x^\star.
$$
取任意 $\varepsilon>0$。

由于 $z^\star$ 已经是最小值，所以不存在 $x\ge0$ 同时满足
$$
Ax=b,
\qquad
c^T x=z^\star-\varepsilon.
$$
等价地，不存在 $x\ge0$ 满足
$$
\widehat A x=\widehat b_\varepsilon,
$$
其中
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
也就是说，系统
$$
\widehat A x=\widehat b_\varepsilon,
\qquad
x\ge0
$$
无解。

由 Farkas 引理，存在
$$
\widehat y
=
\begin{pmatrix}
y\\
\alpha
\end{pmatrix}
$$
使得
$$
\widehat A^T\widehat y\le0,
\qquad
\widehat b_\varepsilon^T\widehat y>0.
$$
展开第一条：
$$
\widehat A^T\widehat y
=
A^T y-\alpha c
\le0.
$$
因此
$$
A^T y\le \alpha c.
$$
展开第二条：
$$
\widehat b_\varepsilon^T\widehat y
=
b^T y+\alpha(-z^\star+\varepsilon)
>0.
$$
所以
$$
b^T y>\alpha(z^\star-\varepsilon).
$$
### 说明 $\alpha>0$

当 $\varepsilon=0$ 时，有
$$
\widehat A x^\star
=
\widehat b_0.
$$
因此系统
$$
\widehat A x=\widehat b_0,
\qquad
x\ge0
$$
有解。

由 Farkas 引理，此时不可能存在 $\widehat y$ 使得
$$
\widehat A^T\widehat y\le0,
\qquad
\widehat b_0^T\widehat y>0.
$$
也就是说，只要
$$
\widehat A^T\widehat y\le0,
$$
就必须有
$$
\widehat b_0^T\widehat y\le0.
$$
而前面已经有
$$
\widehat b_\varepsilon^T\widehat y
=
\widehat b_0^T\widehat y+\alpha\varepsilon
>0.
$$
由于
$$
\widehat b_0^T\widehat y\le0,
$$
要让上式大于 $0$，必须有
$$
\alpha>0.
$$
### 得到 dual 可行解

因为 $\alpha>0$，所以可以令
$$
\tilde y=\frac{y}{\alpha}.
$$
由
$$
A^T y\le \alpha c
$$
得到
$$
A^T \tilde y\le c.
$$
所以 $\tilde y$ 是 dual feasible。

又由
$$
b^T y>\alpha(z^\star-\varepsilon)
$$
两边除以 $\alpha>0$，得到
$$
b^T\tilde y>z^\star-\varepsilon.
$$
因此
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
由于 $\varepsilon>0$ 任意，所以
$$
d^\star\ge z^\star.
$$
结合弱对偶
$$
d^\star\le z^\star,
$$
得到
$$
d^\star=z^\star.
$$
即
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
这就是线性规划的强对偶。

## 9. 互补松弛条件

设 $P^\star$ 是 primal 最优解，$(f^\star,g^\star)$ 是 dual 最优解。

强对偶给出
$$
\langle C,P^\star\rangle
=
\langle f^\star,a\rangle+
\langle g^\star,b\rangle.
$$
另一方面，由 primal-dual gap 的恒等式：
$$
\langle C,P\rangle
-\bigl(\langle f,a\rangle+
\langle g,b\rangle\bigr)
=
\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij}.
$$
代入最优解，得到
$$
\sum_{i,j}(C_{ij}-f_i^\star-g_j^\star)P_{ij}^\star=0.
$$
由于
$$
C_{ij}-f_i^\star-g_j^\star\ge0,
\qquad
P_{ij}^\star\ge0,
$$
每一项都是非负数。非负数之和等于 0，只能每一项都等于 0：
$$
(C_{ij}-f_i^\star-g_j^\star)P_{ij}^\star=0,
\qquad \forall i,j.
$$
这就是互补松弛条件。
等价地，
$$
P_{ij}^\star>0
\quad\Longrightarrow\quad
f_i^\star+g_j^\star=C_{ij}.
$$
也就是说，最优运输只会发生在 dual 约束取等号的边上。
## 10. 互补松弛的含义

定义 slack：
$$
s_{ij}=C_{ij}-f_i^\star-g_j^\star.
$$
互补松弛为
$$
P_{ij}^\star s_{ij}=0.
$$
它的含义是：
- 如果 $P_{ij}^\star>0$，那么 $s_{ij}=0$，即
$$
f_i^\star+g_j^\star=C_{ij}.
$$
- 如果 $s_{ij}>0$，那么 $P_{ij}^\star=0$。
也就是说：
$$
\text{运输正质量的边，一定是等号边。}
$$
但反过来不一定成立：
$$
f_i^\star+g_j^\star=C_{ij}
$$
只说明这条边有可能被使用，不保证
$$
P_{ij}^\star>0.
$$
因此
$$
\operatorname{supp}(P^\star)
\subseteq
\{(i,j):f_i^\star+g_j^\star=C_{ij}\}.
$$
## 11. 势函数的作用

Kantorovich potentials $f,g$ 的作用主要有三点。
### 11.1 证明最优性

如果找到一个 primal feasible 的 $P$，以及一个 dual feasible 的 $(f,g)$，满足
$$
\langle C,P\rangle
=
\langle f,a\rangle+
\langle g,b\rangle,
$$
那么 $P$ 和 $(f,g)$ 都是最优的。
原因是：dual objective 是 primal objective 的下界。若某个 primal 可行解刚好达到这个下界，它不可能再被改进。
### 11.2 定位最优运输的 support

由互补松弛，
$$
P_{ij}^\star>0
\Rightarrow
f_i^\star+g_j^\star=C_{ij}.
$$
因此势函数可以帮助排除不可能使用的边：
$$
f_i^\star+g_j^\star<C_{ij}
\Rightarrow
P_{ij}^\star=0.
$$
### 11.3 解释为价格或势能

可以把 $f_i$ 理解为源点 $i$ 的价格，把 $g_j$ 理解为目标点 $j$ 的价格。
约束
$$
f_i+g_j\le C_{ij}
$$
表示：从 $i$ 到 $j$ 的总势能不能超过真实运输成本。
最优时真正运输的边满足
$$
f_i^\star+g_j^\star=C_{ij}.
$$
即被使用的边上，势能与成本刚好匹配。

## 12. 总结

离散 Kantorovich 最优传输的 primal 是
$$
\min_{\substack{P\ge0\\P\mathbf 1=a,\ P^T\mathbf 1=b}}
\langle C,P\rangle.
$$
通过拉格朗日量
$$
\mathcal L(P,f,g)
=
\langle f,a\rangle+
\langle g,b\rangle
+\sum_{i,j}(C_{ij}-f_i-g_j)P_{ij},
$$
对 $P\ge0$ 取 inf，可以得到 dual feasible condition
$$
f_i+g_j\le C_{ij}.
$$
因此 Kantorovich 对偶为
$$
\max_{f_i+g_j\le C_{ij}}
\langle f,a\rangle+
\langle g,b\rangle.
$$
强对偶保证
$$
\min_{P}\langle C,P\rangle
=
\max_{f,g}\langle f,a\rangle+
\langle g,b\rangle.
$$
最优解满足互补松弛：
$$
(C_{ij}-f_i^\star-g_j^\star)P_{ij}^\star=0.
$$
因此
$$
P_{ij}^\star>0
\Rightarrow
f_i^\star+g_j^\star=C_{ij}.
$$
这说明最优运输只会发生在势函数与代价矩阵相切的位置上。

## 参考资料

- 苏剑林. 《从 Wasserstein 距离、对偶理论到 WGAN》. 科学空间, 2019-01. https://spaces.ac.cn/archives/6280