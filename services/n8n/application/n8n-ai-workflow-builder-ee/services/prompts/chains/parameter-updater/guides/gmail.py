"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/gmail.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater 的工作流模块。导入/依赖:外部:无；内部:无；本地:../types。导出:GMAIL_GUIDE。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/parameter-updater/guides/gmail.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/parameter-updater/guides/gmail.py

import type { NodeTypeGuide } from '../types';

export const GMAIL_GUIDE: NodeTypeGuide = {
	patterns: ['n8n-nodes-base.gmail'],
	content: `
### Gmail Node Updates

#### Common Parameters
- **resource**: message, draft, label, thread
- **operation**: send, get, list, etc.
- **to**: Recipient email address
- **subject**: Email subject line
- **message**: Email body/content
- **authentication**: OAuth2 or Service Account

#### Common Patterns
1. **Sending Email**:
   - Set resource to "message"
   - Set operation to "send"
   - Configure to, subject, and message fields

2. **Using Expressions**:
   - Can use expressions: "={{ $('Previous Node').item.json.email }}"
   - Can reference previous node data for dynamic values
`,
};
