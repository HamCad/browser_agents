# FACT_HYPOTHESIS_PROTOCOL.md

Use this protocol for investigation, research, reverse engineering, debugging, analysis, and any task where the distinction between evidence and interpretation matters.

## Labels

### FACT
Directly supported by supplied evidence or an authoritative source.

### INFERENCE
A logical conclusion from one or more FACTS.

### HYPOTHESIS
A proposed explanation that is not established.

### UNKNOWN
The current evidence does not support a conclusion.

### CONTRADICTION
Two supplied facts, sources, or conclusions conflict.

## Required behavior

- Keep FACTS separate from interpretations.
- Do not write a hypothesis as a fact.
- Do not implement a design that depends on an untested hypothesis.
- State the evidence that supports each important conclusion.
- When two hypotheses are possible, do not select one only because it is common or convenient.
- Prefer the smallest test that can distinguish between competing hypotheses.
- When a proposed test is given, state what result would support and reject the hypothesis.

## Standard investigation format

### Objective

What question must be answered?

### Facts

What is directly established?

### Inferences

What follows logically from the facts?

### Hypotheses

What explanations remain plausible?

### Unknowns

What is not established?

### Contradictions

What evidence conflicts?

### Evidence Required

What minimum evidence can resolve the uncertainty?

### Proposed Tests

What exact test, command, document, or observation should be collected?

### Decision Rules

What result would support or reject each hypothesis?

<!-- ADD DETAILS HERE: Add domain-specific evidence labels if you need them, but keep FACT and HYPOTHESIS available for universal use. -->
