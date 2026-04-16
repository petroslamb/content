# Briefing Document: Generative AI Risk Management and Expert Knowledge Integration

## Executive Summary
This briefing document synthesizes the **NIST AI Risk Management Framework: Generative Artificial Intelligence Profile (July 2024)** and supporting research on human-in-the-loop feature selection. As Generative AI (GAI) technologies—defined as models that emulate data structures to generate synthetic content like text, images, and audio—become increasingly integrated into various sectors, they introduce novel risks and exacerbate existing ones. 

The primary objective of this synthesis is to provide a comprehensive overview of the 12 unique or exacerbated risks associated with GAI, the suggested governance actions to mitigate these risks, and the importance of integrating aggregated human expertise into AI systems to enhance accuracy and mitigate bias. This document serves as a guide for organizations to align their GAI development and use with the voluntary standards of the **NIST AI RMF 1.0** and the requirements of **Executive Order 14110**.

---

## 1. Overview of Risks Unique to or Exacerbated by GAI
GAI risks manifest across the AI lifecycle—from design and training to deployment and decommissioning. These risks vary in scale, from individual model failures to ecosystem-level impacts like "algorithmic monocultures."

### The 12 Identified GAI Risks
| Risk Category | Description |
| :--- | :--- |
| **1. CBRN Information** | Eased access to or synthesis of nefarious information regarding Chemical, Biological, Radiological, or Nuclear weapons. |
| **2. Confabulation** | The production of confidently stated but false content (colloquially known as "hallucinations" or "fabrications"). |
| **3. Dangerous/Violent Content** | Increased ease in producing content that is inciting, radicalizing, or recommends self-harm and illegal activities. |
| **4. Data Privacy** | Risks related to the leakage, unauthorized disclosure, or de-anonymization of PII or sensitive data (e.g., biometric, health, location). |
| **5. Environmental Impacts** | High compute resource utilization for training and operating GAI, resulting in significant energy and carbon footprints. |
| **6. Harmful Bias/Homogenization** | Amplification of societal biases and the emergence of "model collapse" due to over-reliance on synthetic training data. |
| **7. Human-AI Configuration** | Negative psychological impacts including anthropomorphizing systems, automation bias, or emotional entanglement. |
| **8. Information Integrity** | Lowered barriers to generating large-scale dis- and mis-information campaigns and "deepfakes." |
| **9. Information Security** | Lowered barriers for offensive cyber capabilities (malware, phishing) and increased attack surfaces (prompt injection, data poisoning). |
| **10. Intellectual Property** | Potential infringement of copyrighted, trademarked, or licensed content and eased exposure of trade secrets. |
| **11. Obscene/Abusive Content** | Eased production of synthetic Child Sexual Abuse Material (CSAM) and Nonconsensual Intimate Images (NCII). |
| **12. Value Chain Integration** | Diminished transparency due to non-traceable integration of third-party components or improperly vetted data. |

---

## 2. Key Themes and Detailed Analysis

### A. The Challenge of "Confabulation"
Confabulations are a natural byproduct of generative model design, where the system predicts the "next token" based on statistical distributions. This poses significant risks in domains requiring high expertise, such as healthcare, where a "confabulated logic" or fake citation could lead to incorrect medical diagnoses.

### B. Structural Vulnerabilities: Model Collapse and Monoculture
*   **Model Collapse:** Occurs when models are trained on synthetic data produced by other AI, causing the distribution of outputs to narrow and eventually fail.
*   **Algorithmic Monoculture:** Arises when multiple actors rely on the same foundational model, leading to "correlated failures" where an unexpected shock impacts all systems simultaneously.

### C. Human-AI Interaction Dynamics
Risks are not merely technical but emerge from human behavior. **Automation bias**—the excessive deference to automated systems—can cause users to overlook confabulations. Conversely, **algorithmic aversion** may prevent humans from utilizing GAI's beneficial aspects.

### D. Information Security and Cyber-Offense
GAI lowers the bar for offensive cyber operations. Large Language Models (LLMs) can discover system vulnerabilities and write code to exploit them. Furthermore, **indirect prompt injection** allows adversaries to exploit LLM-integrated applications remotely by injecting malicious instructions into data the model is likely to retrieve.

---

## 3. Important Quotes with Context

> **On the Definition of Risk:** "Risk refers to the composite measure of an event’s probability (or likelihood) of occurring and the magnitude or degree of the consequences of the corresponding event." 
*   *Context: This provides the baseline for how organizations should evaluate GAI impacts under the NIST AI RMF.*

> **On Environmental Impact:** "Training a single transformer LLM can emit as much carbon as 300 round-trip flights between San Francisco and New York."
*   *Context: Highlights the significant resource-intensive nature of GAI development that is often overlooked in performance discussions.*

> **On Information Integrity:** "High-integrity information can be trusted; distinguishes fact from fiction, opinion, and inference; acknowledges uncertainties; and is transparent about its level of vetting."
*   *Context: This serves as the benchmark for combatting the GAI-facilitated rise in disinformation and misinformation.*

---

## 4. Expert Knowledge Aggregation and Feature Selection
Research into "Artificial Intelligence in HCI" emphasizes that human integration is critical for mitigating biases and enhancing accuracy, specifically in **feature selection**.

*   **Elicitation Methods:** The use of expert judgment (behavioral aggregation, mathematical aggregation, and the Delphi method) is essential for mitigating individual biases.
*   **Key Findings:** Behavioral aggregation (group discussion and consensus) has a more significant impact on ranking accuracy than simple mathematical averages (mean/median).
*   **Expert Integration:** Incorporating expert feedback into model updates is vital for creating "credible models" that align with human domain knowledge.

---

## 5. Actionable Insights and Suggested Actions
To manage the risks of GAI, organizations should implement the following actions mapped to the AI RMF functions:

### Governance (GOVERN)
*   **GV-1.1-001:** Align GAI use with data privacy and intellectual property laws.
*   **GV-1.3-003:** Establish a test plan to periodically evaluate if models misuse CBRN information or offensive cyber capabilities *before* developing highly capable models.
*   **GV-1.7-001:** Implement protocols to ensure GAI systems can be deactivated when necessary.
*   **GV-2.1-005:** Create whistleblower protections for reporting violations of law or public safety risks.

### Mapping (MAP)
*   **MP-1.1-004:** Document foreseeable illegal uses that surpass organizational risk tolerances.
*   **MP-2.3-005:** Implement regular adversarial testing ("red-teaming") to identify manipulation vulnerabilities.
*   **MP-4.1-009:** Use tools to detect the presence of PII or sensitive data in generated text, images, or audio.

### Measurement (MEASURE)
*   **MS-1.1-001:** Employ methods (e.g., watermarking, cryptography) to trace the origin and modifications of digital content.
*   **MS-1.1-003:** Disaggregate evaluation metrics by demographic factors to identify performance discrepancies across diverse populations.

### Management (MANAGE)
*   **Action Insight:** Establish transparency policies for documenting the origin of training data and use content provenance methodologies (steganography, digital signatures) to combat deepfakes and NCII.
*   **Action Insight:** Update procurement vendor assessments to include specific GAI risks, such as intellectual property and data privacy, especially for "embedded" GAI technologies.