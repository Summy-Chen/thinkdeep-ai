import { DigestData } from "./types";

export const MOCK_DATA: DigestData = {
  date: "2025-12-31",
  analysis: {
    overview: "今日AI领域呈现出多元化发展态势，涵盖从基础研究到应用实践的多个层面，特别是在空间推理、公平性、责任治理和生产力提升方面取得新进展。",
    highlights: [
      "新颖的空间推理评估工具GamiBench，推动多模态大模型在复杂空间任务中的能力提升。",
      "关于AI治理与责任的框架提出，强调自主智能系统的风险管理与责任划定。",
      "关于AI生产力的讨论揭示了实际应用中存在的认知偏差与提升空间，强调模型辅助下的编码与决策优化。"
    ],
    trends: [
      "多模态与空间推理能力的持续突破，推动MLLMs向更复杂的任务扩展。",
      "AI伦理、责任与公平性成为研究重点，推动行业规范和治理框架的建立。"
    ],
    recommendation: "最值得关注的是《With Great Capabilities Come Great Responsibilities》，因其提出的责任与风险治理框架对未来自主智能系统的安全发展具有重要指导意义。"
  },
  articles: [
    {
      id: "1",
      title: "GamiBench: Evaluating Spatial Reasoning and 2D-to-3D Planning Capabilities of MLLMs",
      link: "https://arxiv.org/abs/2512.22207",
      summary: "Multimodal large language models (MLLMs) are proficient in perception and instruction-following, but they still struggle with spatial reasoning...",
      chinese_summary: "GamiBench是一个新的评估工具，用于测试多模态大模型在折纸任务中的空间推理和2D到3D规划能力，揭示了当前模型在复杂空间任务中的局限性。",
      source_name: "arXiv CS.AI",
      published: "2025-12-31T05:00:00",
      category: "research",
      priority: 1
    },
    {
      id: "2",
      title: "With Great Capabilities Come Great Responsibilities: Introducing the Agentic Risk & Capability Framework",
      link: "https://arxiv.org/abs/2512.22211",
      summary: "Agentic AI systems present both significant opportunities and novel risks due to their capacity for autonomous action...",
      chinese_summary: "本文提出了代理风险与能力框架（ARCF），旨在治理具有自主行动能力的AI系统，平衡其带来的机遇与潜在风险。",
      source_name: "arXiv CS.AI",
      published: "2025-12-31T05:00:00",
      category: "research",
      priority: 1
    },
    {
      id: "3",
      title: "The 70% AI productivity myth: why most companies aren't seeing the gains",
      link: "https://sderosiaux.substack.com/p/the-70-ai-productivity-myth-why-most",
      summary: "这篇文章指出，许多公司声称通过使用AI工具实现了70%的生产力提升，但实际上大多数企业并未真正达到这样的效果...",
      chinese_summary: "文章揭示了AI生产力提升的迷思，指出大多数公司因技术应用不当和管理难题，未能实现预期的效率增长。",
      source_name: "Hacker News AI",
      published: "2025-12-30T14:29:00",
      category: "community",
      priority: 2
    },
    {
      id: "4",
      title: "OpenAI Releases GPT-5 with Enhanced Reasoning",
      link: "#",
      summary: "OpenAI has announced the release of GPT-5, featuring significantly improved reasoning capabilities...",
      chinese_summary: "OpenAI发布了GPT-5，具有更强的推理能力和减少的幻觉，在复杂问题解决任务上表现出色。",
      source_name: "OpenAI Blog",
      published: "2025-12-30T10:00:00",
      category: "company",
      priority: 1
    },
    {
      id: "5",
      title: "Google Announces Gemini 2.0",
      link: "#",
      summary: "Google推出Gemini 2.0，在多模态任务上表现出色。",
      chinese_summary: "Google推出Gemini 2.0，在多模态任务上表现出色，特别是在视频理解和生成方面。",
      source_name: "Google AI Blog",
      published: "2025-12-30T09:00:00",
      category: "company",
      priority: 1
    }
  ]
};
