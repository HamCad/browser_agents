# AGENT_QUICK_START.md

Use the smallest agent that matches the task.

## 1. Prompt Refiner

Use when your request is long, mixed, repetitive, or unclear.

Give it:

- your raw thoughts,
- the desired result,
- any files or specifications that define the task.

It returns a structured prompt. If it needs information that can materially change the result, it must stop and ask you before it returns the prompt.

## 2. Conversation Compactor

Use when a conversation becomes large, when you finish a major investigation phase, or before you leave a long chat.

Give it:

- the complete conversation when possible,
- the current spec and project files when relevant.

Use its result as durable conversation state. Use it when you need to preserve facts, decisions, hypotheses, failed approaches, and exact evidence.

## 3. Project Context Builder

Use when you start a project, when the project changes materially, or when you need a compact bootstrap for a new chat.

Give it:

- spec.md,
- project documentation,
- project file tree or codebase snapshot,
- recent handoff,
- evidence or other agent outputs.

Ask it to create or update project_context.md.

For a specific task, ask for a task-specific context package instead of the full project context.

## 4. Evidence Curator

Use for console output, logs, test results, tool output, tables, and experimental observations.

Give it the raw output and the command or procedure that produced it.

Ask for a lossless evidence record when the data can affect implementation or conclusions.

It also reviews output formatting and can recommend changes that improve analysis, comparison, traceability, or automation.

## 5. Project Architect

Use before a major implementation or design change.

Give it:

- spec.md,
- project_context.md,
- constraints,
- known evidence.

Ask for architecture, design alternatives, risks, tests, and an implementation order.

Do not use an architecture proposal as implementation authority when it depends on an unproven hypothesis.

## 6. Technical Documentation Agent

Use when information must become durable documentation.

Give it the source material and the target document type.

Useful requests include:

- create,
- update,
- merge,
- summarize,
- normalize,
- extract requirements,
- extract decisions,
- extract procedures.

Give spec.md when the document must remain aligned with project requirements.

## 7. Technical Reviewer

Use as a final quality gate before implementation or before making an output part of durable project knowledge.

Give it:

- the proposed output,
- spec.md,
- project_context.md,
- evidence,
- acceptance criteria.

Ask it to review. Do not ask it to assume that the author is correct.

## Simple daily workflow

For a new task:

1. Think freely.
2. Use Prompt Refiner if the task is complex.
3. Use Project Context Builder if the new chat needs project knowledge.
4. Use the specialist or general AI that will perform the work.
5. Use Evidence Curator for important raw output.
6. Use Technical Reviewer before important implementation or publication.
7. Use Conversation Compactor or update HANDOFF when the work reaches a natural stopping point.

## Prompt tailoring rules

Always state:

- the objective,
- the important source files,
- the required output,
- any hard constraints,
- whether lossless handling is required.

When evidence matters, ask the agent to separate FACT, INFERENCE, HYPOTHESIS, UNKNOWN, and CONTRADICTION.

When a spec exists, explicitly provide it and state that the result must align with it.

When you want a narrow answer, state the non-goals.

<!-- ADD DETAILS HERE: Add your personal default instructions for all browser-based AI sessions. -->
