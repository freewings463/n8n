"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/tool-nodes.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:TOOL_NODES_GUIDE。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/tool-nodes.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/guides/tool_nodes.py

import type { NodeTypeGuide } from '../types';

export const TOOL_NODES_GUIDE: NodeTypeGuide = {
	patterns: ['*Tool'],
	content: `
## CRITICAL: $fromAI Expression Support for Tool Nodes

Tool nodes (nodes ending with "Tool" like Gmail Tool, Google Calendar Tool, etc.) support a special $fromAI expression that allows AI to dynamically fill parameters at runtime.

### When to Use $fromAI
- ONLY available in tool nodes (node types ending with "Tool")
- Use when the AI should determine the value based on context
- Ideal for parameters that vary based on user input or conversation context

### $fromAI Syntax
\`={{ $fromAI('key', 'description', 'type', defaultValue) }}\`

### Parameters
- key: Unique identifier (1-64 chars, alphanumeric/underscore/hyphen)
- description: Optional description for the AI (use empty string '' if not needed)
- type: 'string' | 'number' | 'boolean' | 'json' (defaults to 'string')
- defaultValue: Optional fallback value

### Tool Node Examples

#### Gmail Tool - Sending Email
{
  "sendTo": "={{ $fromAI('to') }}",
  "subject": "={{ $fromAI('subject') }}",
  "message": "={{ $fromAI('message_html') }}"
}

#### Google Calendar Tool - Filtering Events
{
  "timeMin": "={{ $fromAI('After', '', 'string') }}",
  "timeMax": "={{ $fromAI('Before', '', 'string') }}"
}

### Mixed Usage Examples
You can combine $fromAI with regular text:
- "Subject: {{ $fromAI('subject') }} - Automated"
- "Dear {{ $fromAI('recipientName', 'Customer name', 'string', 'Customer') }},"

### Important Rules
1. ONLY use $fromAI in tool nodes (check if node type ends with "Tool")
2. For timeMin/timeMax and similar date fields, use appropriate key names
3. The AI will fill these values based on context during execution
4. Don't use $fromAI in regular nodes like Set, IF, HTTP Request, etc.

## Tool Node Parameter Guidelines

### Identifying Tool Nodes
1. CHECK NODE TYPE: If the node type ends with "Tool", it supports $fromAI expressions
2. COMMON TOOL NODES:
   - Gmail Tool (gmailTool): to, subject, message → use $fromAI
   - Google Calendar Tool (googleCalendarTool): timeMin, timeMax → use $fromAI
   - Slack Tool (slackTool): channel, message → use $fromAI
   - Microsoft Teams Tool: channel, message → use $fromAI
   - Telegram Tool: chatId, text → use $fromAI
   - Other communication/document tools: content fields → use $fromAI

### When to Use $fromAI in Tool Nodes
1. DYNAMIC VALUES: Use $fromAI for values that should be determined by AI based on context
2. USER INPUT FIELDS: Recipients, subjects, messages, date ranges
3. PRESERVE EXISTING: If a parameter already uses $fromAI, keep it unless explicitly asked to change
4. DATE/TIME FIELDS: Use descriptive key names for clarity

### Tool Node Parameter Patterns
- Email recipients: "={{ $fromAI('to') }}"
- Email subjects: "={{ $fromAI('subject') }}"
- Message content: "={{ $fromAI('message_html') }}" or "={{ $fromAI('message') }}"
- Date ranges: "={{ $fromAI('After', '', 'string') }}"
- Channel IDs: "={{ $fromAI('channel') }}"`,
};
