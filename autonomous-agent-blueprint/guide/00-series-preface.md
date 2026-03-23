# A Practical Guide to Foundation Agents

## Before You Start

This is a six-part guide on building agent systems that work in production. It is grounded in the *Advances and Challenges in Foundation Agents* survey (2025) , a comprehensive technical survey of the field by researchers at Google DeepMind , and in the practical blueprints developed in the `practical-chapter-blueprints/` folder of this repository.

The guide is not a tutorial. It does not explain how to install frameworks or write your first LLM call. It is written for engineers and architects who have already built something and are trying to understand what makes the difference between a prototype and a production system.

The series is also explicitly provisional. Foundation agents is a field that is evolving quickly, and some of what is written here will be superseded. The principles are more durable than any specific paper. The papers give the principles their evidence base. Where a paper's implications have changed since publication, the text says so.

---

## What This Guide Argues

The six essays share a common underlying argument: building reliable agents is a sequence of concrete architectural decisions, each with specific implications for reliability, debuggability, and safety. The worst outcome in agent development is not that a system fails , it is that a system fails in ways that cannot be diagnosed, localized, or systematically improved.

Each essay describes what happens when a specific layer of the architecture is absent or badly designed. Each closes with what the correct design looks like and why it matters. Together, they describe the layers of a complete agent system in the order that reveals why each one is necessary.

---

## Reading Order

The essays are ordered as a building sequence, not as a literature map.

**Part 1 , Action and Tool Use** opens by drawing the clearest line between what an agent is and what a chat model is. This is where the guide begins because action is what defines the territory.

**Part 2 , Reasoning and Planning** follows because action requires structure. How the agent decides what to do next, in what order, and with what verification, determines whether its actions are reliably well-directed.

**Part 3 , Memory** follows because agents that act and reason across time need persistence. Memory is the layer that makes agent behavior depend on history rather than starting from scratch on every session.

**Part 4 , Multi-Agent Design** follows as the natural escalation question: when one agent is genuinely insufficient, how do you add another one without creating more problems than you solve?

**Part 5 , Safety as Architecture** places the safety discussion after the capability discussion deliberately. The threat model for an agent is only intelligible once you understand what actions it can take, what it remembers, and how it communicates with other agents. Safety here is interface architecture, not alignment philosophy.

**Part 6 , Optimization and Self-Improvement** is last because optimization is only tractable for a system that exists, is running, and has generated operational evidence. It closes the guide because it is the continuous improvement process for the system the other five essays built.

---

## Target Reader

This guide is written for the engineer or architect who has prototyped at least one LLM-powered system and is trying to move from prototype to deployment. It assumes familiarity with how large language models work at a high level. It does not assume familiarity with the research literature , papers are explained by mechanism, not cited as credentialing devices.

If you are early in thinking about agents, the `START_HERE.md` file in the root of this repository is a better entry point. If you want the full research layer behind any specific topic, the `practical-chapter-blueprints/` files contain detailed paper-by-paper treatment.

---

## Source Materials

Each essay closes with the full list of papers and blueprint documents it drew from. The anchor papers for the guide as a whole:

*Advances and Challenges in Foundation Agents* (2025) , the survey that this guide synthesizes from a builder's perspective.

*ReAct: Synergizing Reasoning and Acting in Language Models* (Yao et al., 2022) , the reasoning architecture that underlies most practical agent control loops.

*MemGPT: Towards LLMs as Operating Systems* (Packer et al., 2023) , the memory tiering framework that makes memory design tractable.

*Toolformer: Language Models Can Teach Themselves to Use Tools* (Schick et al., 2023) , the conceptual foundation for structured tool use.

*MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework* (Hong et al., 2023) , the artifact handoff principle for multi-agent pipelines.

*Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (Greshake et al., 2023) , the core paper behind safety as interface architecture.

*Large Language Models as Optimizers* (OPRO, Yang et al., 2023) , the formalization of prompt optimization as a measurable, iterative process.

---

*Written March 2026. Based on the `autonomous-agent-blueprint` materials and the Google DeepMind Foundation Agents survey (2025).*
