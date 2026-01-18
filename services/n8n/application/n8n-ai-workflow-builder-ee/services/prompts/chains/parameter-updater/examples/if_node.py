"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/if-node.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:IF_NODE_EXAMPLES。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/if-node.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/examples/if_node.py

import type { NodeTypeExamples } from '../types';

export const IF_NODE_EXAMPLES: NodeTypeExamples = {
	patterns: ['n8n-nodes-base.if'],
	content: `
### IF Node Examples

#### Example 1: Simple String Condition
Current Parameters: {}
Requested Changes: Check if order status equals "pending"
Expected Output:
{
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "id-1",
        "leftValue": "={{ $('Previous Node').item.json.orderStatus }}",
        "rightValue": "pending",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      }
    ],
    "combinator": "and"
  }
}

#### Example 2: Check if Field Exists
Current Parameters: {}
Requested Changes: Check if email field exists in the data
Expected Output:
{
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "id-1",
        "leftValue": "={{ $('Previous Node').item.json.email }}",
        "operator": {
          "type": "string",
          "operation": "exists"
        }
      }
    ],
    "combinator": "and"
  }
}

#### Example 3: Multiple Conditions with AND
Current Parameters: {}
Requested Changes: Check if status is active AND score is 50 or higher
Expected Output:
{
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "id-1",
        "leftValue": "={{ $('Set').item.json.status }}",
        "rightValue": "active",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      },
      {
        "id": "id-2",
        "leftValue": "={{ $('Set').item.json.score }}",
        "rightValue": "50",
        "operator": {
          "type": "number",
          "operation": "gte"
        }
      }
    ],
    "combinator": "and"
  }
}

#### Example 3: IF Node - Complex Multi-Type Conditions
Current Parameters: {}

Requested Changes:
- Check if email is not empty AND verified is true AND permissions array contains "write"

Expected Output:
{
  "conditions": {
    "options": {
      "caseSensitive": true,
      "leftValue": "",
      "typeValidation": "strict"
    },
    "conditions": [
      {
        "id": "id-1",
        "leftValue": "={{ $('Set').item.json.email }}",
        "operator": {
          "type": "string",
          "operation": "notEmpty"
        }
      },
      {
        "id": "id-2",
        "leftValue": "={{ $('Set').item.json.verified }}",
        "operator": {
          "type": "boolean",
          "operation": "true"
        }
      },
      {
        "id": "id-3",
        "leftValue": "={{ $('Set').item.json.permissions }}",
        "rightValue": "write",
        "operator": {
          "type": "array",
          "operation": "contains"
        }
      }
    ],
    "combinator": "and"
  }
}
`,
};
