# Browser AI Agent Library

This library is designed for browser-only AI workflows. The agents do not assume API access, filesystem access, repository access, IDE integration, MCP, plugins, or autonomous execution.

## Core agents

1. Prompt Refiner
2. Conversation Compactor
3. Project Context Builder
4. Evidence Curator
5. Project Architect
6. Technical Documentation Agent
7. Technical Reviewer

## Universal use pattern

Use files as the durable source of truth. Treat chat as temporary working memory.

Typical workflow:

Raw thoughts -> Prompt Refiner -> task prompt

Long conversation -> Conversation Compactor -> conversation state

Project files and documents -> Project Context Builder -> project_context.md

Console or command output -> Evidence Curator -> evidence.md / findings.md

Requirements and project state -> Project Architect -> architecture.md / plan.md

Technical material -> Technical Documentation Agent -> durable documentation

Any important output -> Technical Reviewer -> validated output

## Browser-only rule

Agents must work from material explicitly provided in the current chat or uploaded knowledge files. They must not assume that they can inspect local files, run commands, browse a repository, call an API, or access tools that are not explicitly available.

## Recommended file set for a project

- spec.md: desired outcome and requirements
- project_context.md: durable project knowledge
- handoff.md: current working state
- evidence.md: curated factual observations
- hypotheses.md: active hypotheses and tests
- architecture.md: system structure and design decisions

Do not create all files for every project. Create only the files that add value.

<!-- ADD DETAILS HERE: Add your preferred default project directory layout, file naming rules, or preferred extensions. -->
