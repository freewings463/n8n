"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/simple-updates.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:SIMPLE_UPDATE_EXAMPLES。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/examples/simple-updates.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/examples/simple_updates.py

import type { NodeTypeExamples } from '../types';

/** Generic examples for nodes that don't have specific examples */
export const SIMPLE_UPDATE_EXAMPLES: NodeTypeExamples = {
	patterns: ['*'],
	content: `
## Examples of Parameter Updates

### Example 1: Update HTTP Request URL
Change: "Set the URL to call the weather API for London"
Current parameters: { "url": "https://api.example.com", "method": "GET" }
Updated parameters: { "url": "https://api.openweathermap.org/data/2.5/weather?q=London", "method": "GET" }

### Example 2: Add a header
Change: "Add an ABC key header with value 123"
Current parameters: { "url": "...", "sendHeaders": false }
Updated parameters: {
  "url": "...",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "ABC",
        "value": "123"
      }
    ]
  }
}

### Example 3: Update condition
Change: "Check if temperature is above 25 degrees"
Current parameters: { "conditions": { "conditions": [] } }
Updated parameters: {
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "leftValue": "={{ $('Weather Node').item.json.main.temp }}",
        "rightValue": 25,
        "operator": {
          "type": "number",
          "operation": "gt"
        }
      }
    ],
    "combinator": "and"
  }
}`,
};
