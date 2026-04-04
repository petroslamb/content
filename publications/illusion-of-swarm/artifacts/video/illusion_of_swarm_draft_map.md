{
  "captions": "publications/illusion-of-swarm/artifacts/video/illusion_of_swarm_auto_captions.srt",
  "slides_dir": "publications/illusion-of-swarm/assets/Beyond_Multi-Agent_Swarms",
  "support_slides_dirs": [],
  "segments": [
    {
      "image": "slide-01.png",
      "start": "00:01:18.960",
      "caption_start_index": 41,
      "caption_end_index": 45,
      "match_score": 0.48,
      "ocr_excerpt": "Multi-agent systems are a phase transition, not a destination. Rooted Layers: AI insights grounded on research. A) NotebookLM",
      "ocr_source_count": 1,
      "matched_captions": [
        "AI systems are being designed, funded",
        "and deployed at scale.",
        "Yeah. So our insights today, they come",
        "from a brilliant post by Rooted Layers",
        "AI insights grounded on research. We're"
      ]
    },
    {
      "image": "slide-02.png",
      "start": "00:06:43.919",
      "caption_start_index": 207,
      "caption_end_index": 213,
      "match_score": 0.2613,
      "ocr_excerpt": "Most multi-agent systems are a workaround for routing and state limits. For many same-model production systems, explicit multi-agent structure is the operational price of unresolved coordination problems. The frontier is not adding more personas, but organizing decomposition unde",
      "ocr_source_count": 1,
      "matched_captions": [
        "significant portion of production",
        "applications right now, the explicit",
        "multi- aent structure is just the",
        "operational tax we are paying because",
        "our single models struggle with routing,",
        "state management, and internal",
        "coordination."
      ]
    },
    {
      "image": "slide-03.png",
      "start": "00:11:30.640",
      "caption_start_index": 358,
      "caption_end_index": 358,
      "match_score": 0.2914,
      "ocr_excerpt": "Compiling swarms into single agents reduces both latency and cost. Coder Reviewer -53.7% || -49.5% Token Reduction Latency Reduction Agent + Skills Library Source: University of British Columbia compilation experiments (Li, 2026). The compiled single-agent matches the original mu",
      "ocr_source_count": 1,
      "matched_captions": [
        "to the single agents compiled library to"
      ]
    },
    {
      "image": "slide-04.png",
      "start": "00:42:40.800",
      "caption_start_index": 1301,
      "caption_end_index": 1301,
      "match_score": 0.217,
      "ocr_excerpt": "We build personas to compensate for single-model brittleness. Outcomes depend on tool-coordination tradeoffs and topology- specific error amplification across 180 configurations (Kim et al., 2025). Brittleness stems from three distinct limits: Routing Overloaded context windows f",
      "ocr_source_count": 1,
      "matched_captions": [
        "state."
      ]
    },
    {
      "image": "slide-05.png",
      "start": "00:47:45.520",
      "caption_start_index": 1456,
      "caption_end_index": 1456,
      "match_score": 0.114,
      "ocr_excerpt": "Tool selection breaks down in the semantic collapse zone. Skill selection does not degrade gracefully. Around 80 to 90 skills, nearby tool descriptions occupy the same action space. Adding even one semantically similar competitor reduces selection accuracy materially due to seman",
      "ocr_source_count": 1,
      "matched_captions": [
        "skill-aware routing. implement something"
      ]
    },
    {
      "image": "slide-06.png",
      "start": "00:48:02.480",
      "caption_start_index": 1465,
      "caption_end_index": 1465,
      "match_score": 0.1475,
      "ocr_excerpt": "The boundary keeps similar actions from interfering with each other. We do not create a database agent because querying a database requires a mystical new cognitive faculty. We create it to group tools into namespaces, replacing one overloaded routing decision with several manage",
      "ocr_source_count": 1,
      "matched_captions": [
        "talk to each other."
      ]
    },
    {
      "image": "slide-07.png",
      "start": "00:52:34.160",
      "caption_start_index": 1603,
      "caption_end_index": 1603,
      "match_score": 0.1667,
      "ocr_excerpt": "Structured decomposition beats louder prompting. Once the action space crosses the disambiguation threshold, vague personas fail. Systems must adopt recursive routing (ROMA, Alzu'bi et al., 2026) or route based on explicit performance-cost handbooks (SkillOrchestra, Wang et al., ",
      "ocr_source_count": 1,
      "matched_captions": [
        "the disambiguation threshold around 80"
      ]
    },
    {
      "image": "slide-08.png",
      "start": "00:53:31.119",
      "caption_start_index": 1629,
      "caption_end_index": 1629,
      "match_score": 0.2267,
      "ocr_excerpt": "Multi-agent architectures are strictly necessary in four specific conditions Heterogeneity Trust Different underlying Hard governance and oe O substrates and models Safety boundaries Environment Exploration Distributed, embodied ; | ea Widening coverage coordination a \u201c over poss",
      "ocr_source_count": 1,
      "matched_captions": [
        "models."
      ]
    },
    {
      "image": "slide-09.png",
      "start": "00:53:51.839",
      "caption_start_index": 1640,
      "caption_end_index": 1640,
      "match_score": 0.081,
      "ocr_excerpt": "Capability differences and governance require hard system boundaries. Substrates A code model, vision model, and verifier are not workarounds; they are irreducible capability differences. Authority Safety monitors and delegates must be structurally isolated. Folding them into a s",
      "ocr_source_count": 1,
      "matched_captions": [
        "is meant to be compressed into a single"
      ]
    },
    {
      "image": "slide-10.png",
      "start": "00:55:09.359",
      "caption_start_index": 1676,
      "caption_end_index": 1676,
      "match_score": 0.0667,
      "ocr_excerpt": "Distributed environments and solution search justify distinct actors. Space & Time Embodied agents can interrupt, replan, and block each other. System-level interaction is genuinely irreducible. (EmCoop & MultiAgentBench) Shared Coverage Multiple actors generate wider coverage ov",
      "ocr_source_count": 1,
      "matched_captions": [
        "for dedicating the time to think through"
      ]
    },
    {
      "image": "slide-11.png",
      "start": "00:55:14.960",
      "caption_start_index": 1679,
      "caption_end_index": 1679,
      "match_score": 0.0556,
      "ocr_excerpt": "Natural language is an expensive, lossy abstraction for inter-agent handoffs. When one model converts rich internal state into text, and another reconstructs meaning from that text, the handoff is slow, bandwidth-limited, and lossy. Text is a transih penalty, not an unquestioned ",
      "ocr_source_count": 1,
      "matched_captions": [
        "back next time to unpack another massive"
      ]
    },
    {
      "image": "slide-12.png",
      "start": "00:55:17.040",
      "caption_start_index": 1680,
      "caption_end_index": 1680,
      "match_score": 0.0,
      "ocr_excerpt": "Direct hidden-state transfer bypasses the text translation penalty. The Vision Wormhole: Repurposing visual pathways for coordination yields a +6.3% accuracy gain and 1.87x faster execution (X. Liu et al., 2026). Latent Collaboration: Moving hidden-state information directly with",
      "ocr_source_count": 1,
      "matched_captions": [
        "paradigm shift."
      ]
    },
    {
      "image": "slide-13.png",
      "start": "00:00:00.000",
      "caption_start_index": 1681,
      "caption_end_index": 1681,
      "match_score": -1.0,
      "ocr_excerpt": "Bounded schemas and typed fields outperform unstructured debate. Process-level evidence from EmCoop (H. Yang et al., 2026) shows that more communication is not automatically better. High-volume, unstructured chat destroys plan coherence. Prefer exchanging the smallest useful stat",
      "ocr_source_count": 1,
      "matched_captions": []
    },
    {
      "image": "slide-14.png",
      "start": "00:00:00.000",
      "caption_start_index": 1682,
      "caption_end_index": 1682,
      "match_score": -1.0,
      "ocr_excerpt": "The permanent value of a multi-agent swarm is the trajectory data it generates. Multi-agent systems aren't disappearing; their value is shifting from runtime execution to training-time data generation. Scaffolds, debates, and memory managers are complex training wheels designed t",
      "ocr_source_count": 1,
      "matched_captions": []
    },
    {
      "image": "slide-15.png",
      "start": "00:00:00.000",
      "caption_start_index": 1683,
      "caption_end_index": 1683,
      "match_score": -1.0,
      "ocr_excerpt": "External scaffolding and multi-agent debates eventually become policy updates External Memory Off-Policy Updates iN Core Multi-Agent Policy \\7r Search EMPO2: External memory tips improve exploration during training; the base policy absorbs the behavior during off-policy updates w",
      "ocr_source_count": 1,
      "matched_captions": []
    },
    {
      "image": "slide-16.png",
      "start": "00:00:00.000",
      "caption_start_index": 1684,
      "caption_end_index": 1684,
      "match_score": -1.0,
      "ocr_excerpt": "Engineering directives for system builders starting on Monday. O1 Q2 03 04 05 Start Single: Deploy one model plus tools. Do not add personas until the specific failure mode is named. Think in Namespaces: When routing fails, use bounded action spaces instead of theatrical promptin",
      "ocr_source_count": 1,
      "matched_captions": []
    },
    {
      "image": "slide-17.png",
      "start": "00:00:00.000",
      "caption_start_index": 1685,
      "caption_end_index": 1685,
      "match_score": -1.0,
      "ocr_excerpt": "Two clear architectural shifts expected by Q1 2027. Prediction 1: First-Class Graph Simplification. Major agent frameworks will ship built-in evaluator tooling that actively recommends collapsing multi-agent workflows into single-agent-plus-tools configurations. Q1 2027 JetBrains",
      "ocr_source_count": 1,
      "matched_captions": []
    },
    {
      "image": "slide-18.png",
      "start": "00:00:00.000",
      "caption_start_index": 1686,
      "caption_end_index": 1686,
      "match_score": -1.0,
      "ocr_excerpt": "Empirical foundations and peer-reviewed anchors. Li (2026) Wang et al. (2026) Zhu et al. (2025) Compilation thresholds SkillOrchestra handbooks MultiAgentBench evaluations X. Yang et al. (2026) X. Liu et al. (2026) Z. Liu et al. (2026) Efficient agent survey The Vision Wormhole E",
      "ocr_source_count": 1,
      "matched_captions": []
    }
  ]
}
