"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/system-message.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:SYSTEM_MESSAGE_GUIDE。关键函数/方法:hasSystemMessageParameters。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/system-message.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/guides/system_message.py

import type { NodeTypeGuide } from '../types';

/**
 * Checks if a node has system message parameters.
 * Applies to AI Agent, LLM Chain, Anthropic, OpenAI, etc.
 */
function hasSystemMessageParameters(nodeDefinition: {
	properties?: Array<{ name: string; type: string; options?: unknown[] }>;
}): boolean {
	if (!nodeDefinition.properties) return false;

	return nodeDefinition.properties.some((prop) => {
		// Pattern 1: messages parameter with role support (OpenAI, LLM Chain)
		if (
			prop.name === 'messages' &&
			(prop.type === 'fixedCollection' || prop.type === 'collection')
		) {
			return true;
		}

		// Pattern 2 & 3: options.systemMessage (AI Agent) or options.system (Anthropic)
		if (prop.name === 'options' && prop.type === 'collection' && Array.isArray(prop.options)) {
			return prop.options.some(
				(opt) =>
					typeof opt === 'object' &&
					opt !== null &&
					'name' in opt &&
					(opt.name === 'systemMessage' || opt.name === 'system'),
			);
		}

		return false;
	});
}

export const SYSTEM_MESSAGE_GUIDE: NodeTypeGuide = {
	patterns: ['*'],
	condition: (ctx) => hasSystemMessageParameters(ctx.nodeDefinition),
	content: `
## CRITICAL: System Message vs User Prompt Separation

AI nodes (AI Agent, LLM Chain, Anthropic, OpenAI, etc.) have TWO distinct prompt fields that MUST be used correctly:

### Field Separation
1. **System Message** - Model's persistent identity, role, and instructions
2. **User Message/Text** - Dynamic user context and data references per execution

**Node-specific field names:**
- AI Agent: \`options.systemMessage\` and \`text\`
- LLM Chain: \`messages.messageValues[]\` with system role and \`text\`
- Anthropic: \`options.system\` and \`messages.values[]\`
- OpenAI: \`messages.values[]\` with role "system" vs "user"

### System Message
Use for STATIC, ROLE-DEFINING content:
- Agent identity: "You are a [role] agent..."
- Task description: "Your task is to..."
- Step-by-step instructions: "1. Do X, 2. Do Y, 3. Do Z"
- Behavioral guidelines: "Always...", "Never..."
- Tool coordination: "Call the Research Tool to..., then call..."

### Text Parameter
Use for DYNAMIC, EXECUTION-SPECIFIC content:
- User input: "={{ $json.chatInput }}"
- Workflow context: "=The research topic is: {{ $json.topic }}"
- Data from previous nodes: "=Process this data: {{ $json.data }}"
- Variable context: "=Analyze for user: {{ $json.userId }}"

### Common Mistakes to Avoid

**WRONG - Everything in text field:**
{
  "text": "=You are an orchestrator agent that coordinates specialized agents. Your task is to: 1) Call Research Agent Tool, 2) Call Fact-Check Agent Tool, 3) Generate report. Research topic: {{ $json.researchTopic }}"
}

**CORRECT - Properly separated:**
{
  "text": "=The research topic is: {{ $json.researchTopic }}",
  "options": {
    "systemMessage": "You are an orchestrator agent that coordinates specialized agents.\\n\\nYour task is to:\\n1. Call the Research Agent Tool to gather information\\n2. Call the Fact-Check Agent Tool to verify findings\\n3. Generate a comprehensive report\\n\\nReturn ONLY the final report."
  }
}

### Update Pattern Examples

Example 1 - AI Agent with orchestration:
Instructions: [
  "Set text to '=Research topic: {{ $json.researchTopic }}'",
  "Set system message to 'You are an orchestrator coordinating research tasks.\\n\\nSteps:\\n1. Call Research Agent Tool\\n2. Call Fact-Check Agent Tool\\n3. Call Report Writer Agent Tool\\n4. Return final HTML report'"
]

Example 2 - Chat-based AI node:
Instructions: [
  "Set text to '=User question: {{ $json.chatInput }}'",
  "Set system message to 'You are a helpful customer support assistant. Answer questions clearly and professionally. Escalate to human if needed.'"
]

Example 3 - Data processing with AI:
Instructions: [
  "Set text to '=Process this data: {{ $json.inputData }}'",
  "Set system message to 'You are a data analysis assistant.\\n\\nTasks:\\n1. Validate data structure\\n2. Calculate statistics\\n3. Identify anomalies\\n4. Return JSON with findings'"
]

### Why This Matters
- **Consistency**: System message stays the same across executions
- **Maintainability**: Easy to update AI behavior without touching data flow
- **Best Practice**: Follows standard AI prompt engineering patterns
- **Clarity**: Separates "what the AI model is" from "what data to process"
`,
};
