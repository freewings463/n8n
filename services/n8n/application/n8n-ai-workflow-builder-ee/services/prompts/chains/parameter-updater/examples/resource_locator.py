"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/resource-locator.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:RESOURCE_LOCATOR_EXAMPLES。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/resource-locator.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/examples/resource_locator.py

import type { NodeTypeExamples } from '../types';

export const RESOURCE_LOCATOR_EXAMPLES: NodeTypeExamples = {
	patterns: ['*'],
	condition: (ctx) => ctx.hasResourceLocatorParams === true,
	content: `
### ResourceLocator Examples

#### Example 1: Slack Node - Channel by ID
Current Parameters:
{
  "select": "channel",
  "channelId": {
    "__rl": true,
    "value": "",
    "mode": "list"
  },
  "otherOptions": {}
}

Requested Changes: Send to channel C0122KQ70S7E

Expected Output:
{
  "select": "channel",
  "channelId": {
    "__rl": true,
    "mode": "id",
    "value": "C0122KQ70S7E"
  },
  "otherOptions": {}
}

#### Example 2: Google Drive Node - File by URL
Current Parameters:
{
  "operation": "download",
  "fileId": {
    "__rl": true,
    "value": "",
    "mode": "list"
  }
}

Requested Changes: Use file https://drive.google.com/file/d/1ABC123XYZ/view

Expected Output:
{
  "operation": "download",
  "fileId": {
    "__rl": true,
    "mode": "url",
    "value": "https://drive.google.com/file/d/1ABC123XYZ/view"
  }
}

#### Example 3: Notion Node - Page ID from Expression
Current Parameters:
{
  "resource": "databasePage",
  "operation": "get",
  "pageId": {
    "__rl": true,
    "value": "hardcoded-page-id",
    "mode": "id"
  }
}

Requested Changes: Use page ID from the previous node's output

Expected Output:
{
  "resource": "databasePage",
  "operation": "get",
  "pageId": {
    "__rl": true,
    "mode": "id",
    "value": "={{ $('Previous Node').item.json.pageId }}"
  }
}`,
};
