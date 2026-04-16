{
  "title": "AI Quiz",
  "questions": [
    {
      "question": "According to the NIST AI RMF GAI Profile, which phenomenon occurs when a generative model's training over-relies on synthetic data, causing data points to vanish from the output distribution?",
      "answerOptions": [
        {
          "text": "Algorithmic Monoculture",
          "isCorrect": false,
          "rationale": "This refers to systemic failures resulting from multiple actors relying on the same underlying algorithm or model."
        },
        {
          "text": "Model Collapse",
          "isCorrect": true,
          "rationale": "This specifically describes the degradation of a model's output distribution due to the recursive use of synthetic training data."
        },
        {
          "text": "Data Memorization",
          "isCorrect": false,
          "rationale": "This term refers to a model revealing sensitive training data samples during adversarial attacks rather than the loss of output diversity."
        },
        {
          "text": "Confabulation",
          "isCorrect": false,
          "rationale": "This refers to the generation of false or erroneous content presented confidently by the system."
        }
      ],
      "hint": "Consider the long-term impact on a model's robustness when it learns primarily from its own previous outputs."
    },
    {
      "question": "Regarding Chemical, Biological, Radiological, or Nuclear (CBRN) risks, what was a primary finding of recent research into state-of-the-art Large Language Models (LLMs)?",
      "answerOptions": [
        {
          "text": "LLMs provide significant operational assistance for attack planning that surpasses expert human knowledge.",
          "isCorrect": false,
          "rationale": "Research indicates that current models do not yet offer capabilities that exceed existing expert-level scientific design."
        },
        {
          "text": "LLM outputs provided minimal assistance beyond what can be found through traditional search engine queries.",
          "isCorrect": true,
          "rationale": "Studies found that for biological threat creation, LLMs did not substantially increase the likelihood of an attack compared to standard information retrieval."
        },
        {
          "text": "Biological Design Tools (BDTs) are less effective than text-based LLMs for specialized chemical design.",
          "isCorrect": false,
          "rationale": "BDTs are highly specialized AI systems trained on scientific data that actually aid design capabilities more than general text models."
        },
        {
          "text": "The primary barrier to CBRN misuse is currently the lack of access to general-purpose LLM weights.",
          "isCorrect": false,
          "rationale": "The document suggests expertise and infrastructure remain the key barriers rather than just model weight access."
        }
      ],
      "hint": "Think about how LLM outputs compare to the information available through standard internet searches."
    },
    {
      "question": "In the NIST AI RMF context, how is a 'Profile' defined for Generative AI (GAI)?",
      "answerOptions": [
        {
          "text": "A set of mandatory regulatory requirements for GAI developers.",
          "isCorrect": false,
          "rationale": "The AI RMF is intended for voluntary use and is not a set of mandatory regulations."
        },
        {
          "text": "An implementation of the AI RMF functions for a specific setting, application, or technology.",
          "isCorrect": true,
          "rationale": "Profiles assist organizations in managing AI risks aligned with their goals and specific technological contexts."
        },
        {
          "text": "A technical specification for the hardware used to train dual-use foundation models.",
          "isCorrect": false,
          "rationale": "Profiles focus on risk management frameworks and governance rather than hardware specifications."
        },
        {
          "text": "A database of known security vulnerabilities in open-source GAI modeling libraries.",
          "isCorrect": false,
          "rationale": "While it may reference such databases, a Profile is a higher-level implementation of risk management categories."
        }
      ],
      "hint": "Consider how the AI RMF functions are tailored to specific sectors or technologies."
    },
    {
      "question": "Which specific information security risk involves modifies inputs to a GAI system so it behaves in unintended ways, often through exploiting retrieved data?",
      "answerOptions": [
        {
          "text": "Direct Prompt Injection",
          "isCorrect": false,
          "rationale": "This involves crafting malicious prompts inputted directly into the system's interface by a user."
        },
        {
          "text": "Data Poisoning",
          "isCorrect": false,
          "rationale": "This refers to the compromise of the training dataset used by a model to manipulate its fundamental operations."
        },
        {
          "text": "Indirect Prompt Injection",
          "isCorrect": true,
          "rationale": "This occurs when adversaries exploit integrated applications by injecting prompts into data that the LLM is likely to retrieve remotely."
        },
        {
          "text": "Model Distillation",
          "isCorrect": false,
          "rationale": "This is a method for creating smaller versions of trained models to reduce environmental impact, not a security attack."
        }
      ],
      "hint": "Focus on the distinction between a user's direct input and data retrieved by the system from external sources."
    },
    {
      "question": "A study cited in the GAI Profile compared energy consumption for LLM inference. Which type of task was found to be more carbon-intensive?",
      "answerOptions": [
        {
          "text": "Discriminative tasks such as text classification.",
          "isCorrect": false,
          "rationale": "Non-generative tasks like classification require fewer resources during the inference phase compared to synthesis."
        },
        {
          "text": "Generative tasks such as text summarization.",
          "isCorrect": true,
          "rationale": "The document notes that generative tasks are more energy- and carbon-intensive than discriminative tasks during inference."
        },
        {
          "text": "Model compression tasks such as pruning.",
          "isCorrect": false,
          "rationale": "Compression is a refinement process, not a standard inference task compared in the cited study."
        },
        {
          "text": "Fine-tuning tasks using self-supervision.",
          "isCorrect": false,
          "rationale": "While resource-heavy, the study specifically compared different types of inference tasks rather than training phases."
        }
      ],
      "hint": "Consider the difference between a model categorizing existing data and a model creating new content."
    },
    {
      "question": "The conference paper 'Aggregating Human Domain Knowledge for Feature Ranking' examined different methods for eliciting opinions. What was the observed impact of the Delphi method compared to individual rankings?",
      "answerOptions": [
        {
          "text": "It significantly increased the accuracy of feature selection over mathematical aggregation.",
          "isCorrect": false,
          "rationale": "The results indicated that mathematical aggregation, specifically behavioral, had a more significant impact."
        },
        {
          "text": "It had a more significant impact on the final rankings than behavioral aggregation.",
          "isCorrect": false,
          "rationale": "The study found that behavioral aggregation actually had a more significant impact than other methods."
        },
        {
          "text": "It had minimal impact on the rankings compared to individual expert opinions.",
          "isCorrect": true,
          "rationale": "The online experiment showed that the Delphi method's impact was minimal relative to individual rankings."
        },
        {
          "text": "It completely eliminated cognitive biases in the participants' feature ranking process.",
          "isCorrect": false,
          "rationale": "While intended to mitigate bias, the study does not claim that it 'completely eliminated' all biases."
        }
      ],
      "hint": "Recall the study's findings on the effectiveness of consensus-building methods versus mathematical averages."
    },
    {
      "question": "According to the NIST GAI Profile, which human-AI interaction risk refers to 'excessive deference to automated systems' where users perceive AI content to be of higher quality than other sources?",
      "answerOptions": [
        {
          "text": "Algorithmic Aversion",
          "isCorrect": false,
          "rationale": "This refers to the opposite phenomenon, where experts are unnecessarily resistant to using beneficial GAI systems."
        },
        {
          "text": "Emotional Entanglement",
          "isCorrect": false,
          "rationale": "This involves psychological impacts from a human forming an inappropriate bond with a GAI system."
        },
        {
          "text": "Automation Bias",
          "isCorrect": true,
          "rationale": "This specifically describes the unjustified trust or deference humans give to automated systems over human or other data sources."
        },
        {
          "text": "Anthropomorphization",
          "isCorrect": false,
          "rationale": "This is the act of attributing human-like characteristics or traits to the AI system itself."
        }
      ],
      "hint": "Look for a term that implies a systematic leaning toward trusting machine-generated results."
    },
    {
      "question": "In the suggested actions for the GOVERN function (GV-6.1-009), what is recommended for organizations during the GAI acquisition and procurement process?",
      "answerOptions": [
        {
          "text": "Automatically terminate all contracts with vendors that use open-source GAI modeling libraries.",
          "isCorrect": false,
          "rationale": "The framework suggests managing risks through due diligence and assessment rather than blanket termination of open-source use."
        },
        {
          "text": "Rely solely on the GAI vendor's internal safety assessments to ensure legal compliance.",
          "isCorrect": false,
          "rationale": "The framework encourages independent evaluations and verifying vendors against external incident or vulnerability databases."
        },
        {
          "text": "Update due diligence processes to include assessments of third-party intellectual property, data privacy, and security risks.",
          "isCorrect": true,
          "rationale": "The action item specifically suggests integrating GAI-specific risks into procurement assessments and vendor vetting."
        },
        {
          "text": "Wait for the GAI space to mature before establishing any internal acceptable use policies for contractors.",
          "isCorrect": false,
          "rationale": "Action GV-6.1-010 recommends updating these policies to address proprietary and open-source GAI technologies immediately."
        }
      ],
      "hint": "Consider the 'due diligence' required when integrating external components into an organizational value chain."
    },
    {
      "question": "Regarding 'Information Integrity,' what is a key characteristic of 'high-integrity information' as defined in the Roadmap for Researchers derived within the NIST document?",
      "answerOptions": [
        {
          "text": "It is information generated solely by verified AI systems to eliminate human error.",
          "isCorrect": false,
          "rationale": "Integrity is not tied to AI generation; in fact, AI often presents a risk to this integrity."
        },
        {
          "text": "It acknowledges uncertainties and can be linked to the original source(s) with appropriate evidence.",
          "isCorrect": true,
          "rationale": "High-integrity information distinguishes fact from fiction, provides evidence for its sources, and is transparent about vetting."
        },
        {
          "text": "It is content that has been obfuscated via steganography to prevent unauthorized use.",
          "isCorrect": false,
          "rationale": "While steganography is a provenance tool, integrity refers to the transparency and verifiability of the content itself."
        },
        {
          "text": "It refers only to information that is impossible to replicate via synthetic media.",
          "isCorrect": false,
          "rationale": "Information integrity relates to the patterns of creation and exchange across all types of media."
        }
      ],
      "hint": "Think about transparency regarding evidence and the distinction between fact and opinion."
    },
    {
      "question": "Which Suggested Action (MAP 4.1-008) is advised when adapting GAI models to new domains where previous assumptions may no longer hold?",
      "answerOptions": [
        {
          "text": "Decommission the model immediately to avoid unanticipated performance disparities.",
          "isCorrect": false,
          "rationale": "The action suggests re-evaluation and establishment of warning systems rather than immediate decommissioning."
        },
        {
          "text": "Re-evaluate risks and establish warning systems to determine if the GAI system is being misused in the new context.",
          "isCorrect": true,
          "rationale": "The action specifically recommends establishing systems to detect when safety or security assumptions are no longer valid in a new domain."
        },
        {
          "text": "Permit users to decide the risk tolerance for the new domain without organizational oversight.",
          "isCorrect": false,
          "rationale": "Organizational governance is emphasized to ensure risks like harmful bias or security are managed centrally."
        },
        {
          "text": "Rely on the training data curation policies of the original base model without further testing.",
          "isCorrect": false,
          "rationale": "Fine-tuned models or those used in new domains require fresh evaluation of risks like data privacy and bias."
        }
      ],
      "hint": "Consider the importance of context-specific safety checks when a technology moves into a different field."
    }
  ]
}