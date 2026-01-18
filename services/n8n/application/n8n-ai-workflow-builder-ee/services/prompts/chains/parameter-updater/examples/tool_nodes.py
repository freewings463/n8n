"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/tool-nodes.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:TOOL_NODE_EXAMPLES。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/tool-nodes.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/examples/tool_nodes.py

import type { NodeTypeExamples } from '../types';

export const TOOL_NODE_EXAMPLES: NodeTypeExamples = {
	patterns: ['*Tool'],
	content: `
### Tool Node Examples

#### Example 1: Gmail Tool - Send Email with AI
Current Parameters: {}
Requested Changes: Let AI determine recipient, subject, and message
Expected Output:
{
  "sendTo": "={{ $fromAI('to') }}",
  "subject": "={{ $fromAI('subject') }}",
  "message": "={{ $fromAI('message_html') }}",
  "options": {}
}

#### Example 2: Google Calendar Tool - Filter by Date
Current Parameters:
{
  "operation": "getAll",
  "calendar": {
    "__rl": true,
    "value": "primary",
    "mode": "list"
  }
}

Requested Changes: Let AI determine date range for filtering

Expected Output:
{
  "operation": "getAll",
  "calendar": {
    "__rl": true,
    "value": "primary",
    "mode": "list"
  },
  "timeMin": "={{ $fromAI('After', '', 'string') }}",
  "timeMax": "={{ $fromAI('Before', '', 'string') }}"
}

#### Example 3: Slack Tool - Send Message
Current Parameters:
{
  "resource": "message"
}

Requested Changes: Let AI determine channel and message content

Expected Output:
{
  "resource": "message",
  "channelId": "={{ $fromAI('channel') }}",
  "messageText": "={{ $fromAI('message') }}"
}

#### Example 4: Tool Node with Mixed Content
Current Parameters:
{
  "sendTo": "admin@company.com"
}

Requested Changes: Keep admin email but let AI add additional recipients and determine subject

Expected Output:
{
  "sendTo": "=admin@company.com, {{ $fromAI('additional_recipients') }}",
  "subject": "={{ $fromAI('subject') }} - Automated Report"
}`,
};
