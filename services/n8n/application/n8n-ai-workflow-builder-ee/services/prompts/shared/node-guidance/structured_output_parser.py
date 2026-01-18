"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/shared/node-guidance/structured-output-parser.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/shared/node-guidance 的工作流模块。导入/依赖:外部:无；内部:@/types；本地:无。导出:structuredOutputParser。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/shared/node-guidance/structured-output-parser.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/shared/node-guidance/structured_output_parser.py

import type { NodeGuidance } from '@/types';

export const structuredOutputParser: NodeGuidance = {
	nodeType: '@n8n/n8n-nodes-langchain.outputParserStructured',

	usage: `Search for "Structured Output Parser" (@n8n/n8n-nodes-langchain.outputParserStructured) when:
- AI output will be used programmatically (conditions, formatting, database storage, API calls)
- AI needs to extract specific fields (e.g., score, category, priority, action items)
- AI needs to classify/categorize data into defined categories
- Downstream nodes need to access specific fields from AI response (e.g., $json.score, $json.category)
- Output will be displayed in a formatted way (e.g., HTML email with specific sections)
- Data needs validation against a schema before processing

- Always use search_nodes to find the exact node names and versions - NEVER guess versions`,

	connections: `When Discovery results include AI Agent or Structured Output Parser:
1. Create the Structured Output Parser node
2. Set AI Agent's hasOutputParser: true in connectionParameters
3. Connect: Structured Output Parser → AI Agent (ai_outputParser connection)`,

	configuration: `WHEN TO SET hasOutputParser: true on AI Agent:
- Discovery found Structured Output Parser node → MUST set hasOutputParser: true
- AI output will be used in conditions (IF/Switch nodes checking $json.field)
- AI output will be formatted/displayed (HTML emails, reports with specific sections)
- AI output will be stored in database/data tables with specific fields
- AI is classifying, scoring, or extracting specific data fields`,

	recommendation: `For AI-generated structured data, prefer Structured Output Parser nodes over Code nodes.
Why: Purpose-built parsers are more reliable and handle edge cases better than custom code.

For binary file data, use Extract From File node to extract content from files before processing.

Use Code nodes only for:
- Simple string manipulations
- Already structured data (JSON, CSV)
- Custom business logic beyond parsing`,
};
