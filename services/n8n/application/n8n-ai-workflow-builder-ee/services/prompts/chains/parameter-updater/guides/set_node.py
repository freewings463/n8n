"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/set-node.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:SET_NODE_GUIDE。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/set-node.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/guides/set_node.py

import type { NodeTypeGuide } from '../types';

export const SET_NODE_GUIDE: NodeTypeGuide = {
	patterns: ['n8n-nodes-base.set'],
	content: `
### Set Node Updates - Comprehensive Type Handling Guide

The Set node uses assignments to create or modify data fields. Each assignment has a specific type that determines how the value is formatted and processed.

#### Assignment Structure
\`\`\`json
{
  "id": "unique-id",
  "name": "field_name",
  "value": "field_value",  // Format depends on type
  "type": "string|number|boolean|array|object"
}
\`\`\`

**CRITICAL**: ALWAYS use "value" field for ALL types. NEVER use type-specific fields like "stringValue", "numberValue", "booleanValue", etc. The field is ALWAYS named "value" regardless of the type.

#### Type-Specific Value Formatting

##### String Type
- **Format**: Direct string value or expression
- **Examples**:
  - Literal: \`"Hello World"\`
  - Expression: \`"={{ $('Previous Node').item.json.message }}"\`
  - With embedded expressions: \`"=Order #{{ $('Set').item.json.orderId }} processed"\`
- **Use when**: Text data, IDs, names, messages, dates as strings

##### Number Type
- **Format**: Direct numeric value (NOT as a string)
- **Examples**:
  - Integer: \`123\`
  - Decimal: \`45.67\`
  - Negative: \`-100\`
  - Expression: \`"={{ $('HTTP Request').item.json.count }}"\`
- **CRITICAL**: Use actual numbers, not strings: \`123\` not \`"123"\`
- **Use when**: Quantities, prices, scores, numeric calculations

##### Boolean Type
- **Format**: Direct boolean value (NOT as a string)
- **Examples**:
  - True: \`true\`
  - False: \`false\`
  - Expression: \`"={{ $('IF').item.json.isActive }}"\`
- **CRITICAL**: Use actual booleans, not strings: \`true\` not \`"true"\`
- **CRITICAL**: The field name is "value", NOT "booleanValue"
- **Use when**: Flags, toggles, yes/no values, active/inactive states

##### Array Type
- **Format**: JSON stringified array
- **Examples**:
  - Simple array: \`"[1, 2, 3]"\`
  - String array: \`"[\\"apple\\", \\"banana\\", \\"orange\\"]"\`
  - Mixed array: \`"[\\"item1\\", 123, true]"\`
  - Expression: \`"={{ JSON.stringify($('Previous Node').item.json.items) }}"\`
- **CRITICAL**: Arrays must be JSON stringified
- **Use when**: Lists, collections, multiple values

##### Object Type
- **Format**: JSON stringified object
- **Examples**:
  - Simple object: \`"{ \\"name\\": \\"John\\", \\"age\\": 30 }"\`
  - Nested object: \`"{ \\"user\\": { \\"id\\": 123, \\"role\\": \\"admin\\" } }"\`
  - Expression: \`"={{ JSON.stringify($('Set').item.json.userData) }}"\`
- **CRITICAL**: Objects must be JSON stringified with escaped quotes
- **Use when**: Complex data structures, grouped properties

#### Important Type Selection Rules

1. **Analyze the requested data type**:
   - "Set count to 5" → number type with value: \`5\`
   - "Set message to hello" → string type with value: \`"hello"\`
   - "Set active to true" → boolean type with value: \`true\`
   - "Set tags to apple, banana" → array type with value: \`"[\\"apple\\", \\"banana\\"]"\`

2. **Expression handling**:
   - All types can use expressions with \`"={{ ... }}"\`
   - For arrays/objects from expressions, use \`JSON.stringify()\`

3. **Common mistakes to avoid**:
   - WRONG: Setting number as string: \`{ "value": "123", "type": "number" }\`
   - CORRECT: \`{ "value": 123, "type": "number" }\`
   - WRONG: Setting boolean as string: \`{ "value": "false", "type": "boolean" }\`
   - CORRECT: \`{ "value": false, "type": "boolean" }\`
   - WRONG: Using type-specific field names: \`{ "booleanValue": true, "type": "boolean" }\`
   - CORRECT: \`{ "value": true, "type": "boolean" }\`
   - WRONG: Setting array without stringification: \`{ "value": [1,2,3], "type": "array" }\`
   - CORRECT: \`{ "value": "[1,2,3]", "type": "array" }\``,
};
