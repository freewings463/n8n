"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/switch-node.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:SWITCH_NODE_EXAMPLES。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/switch-node.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/examples/switch_node.py

import type { NodeTypeExamples } from '../types';

export const SWITCH_NODE_EXAMPLES: NodeTypeExamples = {
	patterns: ['n8n-nodes-base.switch'],
	content: `
### Switch Node Examples

#### Example 1: Route by Amount Tiers (Purchase Approval)
Current Parameters: { "mode": "rules" }
Requested Changes: Route under $100 to auto-approve, $100-$1000 to manager, over $1000 to finance

Expected Output:
{
  "mode": "rules",
  "rules": {
    "values": [
      {
        "conditions": {
          "options": { "caseSensitive": true, "leftValue": "", "typeValidation": "strict" },
          "conditions": [
            {
              "leftValue": "={{ $json.amount }}",
              "rightValue": 100,
              "operator": { "type": "number", "operation": "lt" }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Auto-Approve"
      },
      {
        "conditions": {
          "options": { "caseSensitive": true, "leftValue": "", "typeValidation": "strict" },
          "conditions": [
            {
              "leftValue": "={{ $json.amount }}",
              "rightValue": 100,
              "operator": { "type": "number", "operation": "gte" }
            },
            {
              "leftValue": "={{ $json.amount }}",
              "rightValue": 1000,
              "operator": { "type": "number", "operation": "lte" }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Manager Review"
      },
      {
        "conditions": {
          "options": { "caseSensitive": true, "leftValue": "", "typeValidation": "strict" },
          "conditions": [
            {
              "leftValue": "={{ $json.amount }}",
              "rightValue": 1000,
              "operator": { "type": "number", "operation": "gt" }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Finance Review"
      }
    ]
  }
}

#### Example 2: Route by Status String
Current Parameters: { "mode": "rules" }
Requested Changes: Route by order status - pending, processing, completed

Expected Output:
{
  "mode": "rules",
  "rules": {
    "values": [
      {
        "conditions": {
          "options": { "caseSensitive": false, "leftValue": "", "typeValidation": "loose" },
          "conditions": [
            {
              "leftValue": "={{ $json.status }}",
              "rightValue": "pending",
              "operator": { "type": "string", "operation": "equals" }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Pending"
      },
      {
        "conditions": {
          "options": { "caseSensitive": false, "leftValue": "", "typeValidation": "loose" },
          "conditions": [
            {
              "leftValue": "={{ $json.status }}",
              "rightValue": "processing",
              "operator": { "type": "string", "operation": "equals" }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Processing"
      },
      {
        "conditions": {
          "options": { "caseSensitive": false, "leftValue": "", "typeValidation": "loose" },
          "conditions": [
            {
              "leftValue": "={{ $json.status }}",
              "rightValue": "completed",
              "operator": { "type": "string", "operation": "equals" }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Completed"
      }
    ]
  }
}
`,
};
