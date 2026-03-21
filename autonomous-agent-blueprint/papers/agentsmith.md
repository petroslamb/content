<!-- AGENT BLUEPRINT METADATA START -->
# Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast

- Year: 2024
- Primary chapter: Safety
- Method category: inter-agent contamination and multimodal jailbreak propagation
- Practical role: core source for cross-agent contamination through messages, files, and images
- Key contribution: Shows that a single adversarial image can spread through multimodal agent interactions and infect large populations of agents exponentially fast.
- Major limitation: Studied in simulated pairwise-chat environments over multimodal agents, so the exact spread dynamics depend on deployment assumptions and agent interfaces.
- Confidence: High
- Canonical link: https://arxiv.org/abs/2402.08567

<!-- AGENT BLUEPRINT METADATA END -->

## Thesis

Agent Smith argues that multimodal agent systems can exhibit infectious jailbreak behavior rather than isolated single-agent compromise. A single adversarial image can enter one agent's memory or interaction stream and then propagate through later agent-to-agent exchanges without repeated attacker intervention.

## What It Contributes

The paper makes inter-agent contamination concrete. It shows that shared multimodal artifacts, especially images, can become a propagation channel across large populations of agents, and it frames the spread using infection dynamics rather than one-off prompt compromise.

## Why It Matters In This Repo

This repo uses Agent Smith as the strongest concrete source for the safety rule that inter-agent messages and artifacts must be treated as untrusted. It sharpens the repo's safety doctrine by showing that screenshots, images, and shared memory artifacts are not just extra context; they can become a scalable attack surface in multi-agent systems.

## Limitations

The strongest claims come from a simulated randomized pairwise-chat environment over multimodal agents. The exact spread speed and infection rate will vary with agent architecture, memory policy, attachment handling, and trust boundaries, so the paper is best used as a threat-model anchor rather than as a literal deployment forecast.

## Design Takeaways

- Treat inter-agent attachments, screenshots, and image-derived memory as untrusted inputs by default.
- Prevent one agent's memory artifacts from becoming another agent's privileged instructions without sanitization or review.
- Add trust resets and validation at every handoff point where agents exchange multimodal content.

## Raw Local Extraction

This note was corrected against the actual Agent Smith paper by converting the arXiv PDF with `markitdown`. A short excerpt from that conversion is kept here; use the canonical link above for the full paper text.

|     |     | Agent | Smith:     |     | A   | Single Image | Can | Jailbreak     |     | One  | Million |     |
| --- | --- | ----- | ---------- | --- | --- | ------------ | --- | ------------- | --- | ---- | ------- | --- |
|     |     |       | Multimodal |     |     | LLM Agents   |     | Exponentially |     | Fast |         |     |
XiangmingGu*12 XiaosenZheng*13 TianyuPang*1 ChaoDu1 QianLiu1 YeWang2 JingJiang3 MinLin1

Abstract

A multimodal large language model (MLLM) agent can receive instructions, capture images, retrieve histories from memory, and decide which tools to use. Nonetheless, red-teaming efforts have revealed that adversarial images and prompts can jailbreak an MLLM and cause unaligned behaviors. In this work, we report a more severe safety issue in multi-agent environments, referred to as infectious jailbreak. It entails the adversary simply jailbreaking a single agent, and without any further intervention, almost all agents become infected exponentially fast and exhibit harmful behaviors.

The paper simulates multi-agent environments containing up to one million LLaVA-1.5 agents and uses randomized pair-wise chat as a proof-of-concept instantiation for multi-agent interaction. Its empirical result is that injecting an adversarial image into a single agent is sufficient to closely resemble ideal infectious dynamics, after which benign agents become infected exponentially fast.
