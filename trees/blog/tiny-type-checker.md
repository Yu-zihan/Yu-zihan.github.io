---
title: Implementing a Tiny Type Checker
date: 2026-05-02
type: blog
tags: programming, types, rust
summary: A small dependently-typed lambda calculus in Rust.
draft: false
---

A small dependently-typed lambda calculus in Rust.

## Core idea

We separate syntax, typing context, and normalization, then define typing rules by structural recursion.
