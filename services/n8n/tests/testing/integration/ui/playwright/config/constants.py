"""
MIGRATION-META:
  source_path: packages/testing/playwright/config/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/config 的配置。导入/依赖:外部:无；内部:无；本地:无。导出:BACKEND_BASE_URL、N8N_AUTH_COOKIE、DEFAULT_USER_PASSWORD、MANUAL_TRIGGER_NODE_NAME、MANUAL_TRIGGER_NODE_DISPLAY_NAME、MANUAL_CHAT_TRIGGER_NODE_NAME、CHAT_TRIGGER_NODE_DISPLAY_NAME、SCHEDULE_TRIGGER_NODE_NAME 等34项。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/config/constants.ts -> services/n8n/tests/testing/integration/ui/playwright/config/constants.py

export const BACKEND_BASE_URL = 'http://localhost:5678';
export const N8N_AUTH_COOKIE = 'n8n-auth';

export const DEFAULT_USER_PASSWORD = 'PlaywrightTest123';

export const MANUAL_TRIGGER_NODE_NAME = 'Manual Trigger';
export const MANUAL_TRIGGER_NODE_DISPLAY_NAME = 'When clicking ‘Execute workflow’';
export const MANUAL_CHAT_TRIGGER_NODE_NAME = 'Chat Trigger';
export const CHAT_TRIGGER_NODE_DISPLAY_NAME = 'When chat message received';
export const SCHEDULE_TRIGGER_NODE_NAME = 'Schedule Trigger';
export const CODE_NODE_NAME = 'Code';
export const CODE_NODE_DISPLAY_NAME = 'Code in JavaScript';
export const SET_NODE_NAME = 'Set';
export const EDIT_FIELDS_SET_NODE_NAME = 'Edit Fields (Set)';
export const LOOP_OVER_ITEMS_NODE_NAME = 'Loop Over Items';
export const IF_NODE_NAME = 'If';
export const MERGE_NODE_NAME = 'Merge';
export const SWITCH_NODE_NAME = 'Switch';
export const GMAIL_NODE_NAME = 'Gmail';
export const TRELLO_NODE_NAME = 'Trello';
export const NOTION_NODE_NAME = 'Notion';
export const PIPEDRIVE_NODE_NAME = 'Pipedrive';
export const HTTP_REQUEST_NODE_NAME = 'HTTP Request';
export const AGENT_NODE_NAME = 'AI Agent';
export const BASIC_LLM_CHAIN_NODE_NAME = 'Basic LLM Chain';
export const AI_MEMORY_WINDOW_BUFFER_MEMORY_NODE_NAME = 'Simple Memory';
export const AI_TOOL_CALCULATOR_NODE_NAME = 'Calculator';
export const AI_TOOL_CODE_NODE_NAME = 'Code Tool';
export const AI_TOOL_WIKIPEDIA_NODE_NAME = 'Wikipedia';
export const AI_TOOL_HTTP_NODE_NAME = 'HTTP Request Tool';
export const AI_LANGUAGE_MODEL_OPENAI_CHAT_MODEL_NODE_NAME = 'OpenAI Chat Model';
export const AI_MEMORY_POSTGRES_NODE_NAME = 'Postgres Chat Memory';
export const AI_MEMORY_REDIS_CHAT_NODE_NAME = 'Redis Chat Memory';
export const AI_OUTPUT_PARSER_AUTO_FIXING_NODE_NAME = 'Auto-fixing Output Parser';
export const WEBHOOK_NODE_NAME = 'Webhook';
export const EXECUTE_WORKFLOW_NODE_NAME = 'Execute Workflow';
export const NO_OPERATION_NODE_NAME = 'No Operation, do nothing';
export const HACKER_NEWS_NODE_NAME = 'Hacker News';

export const NEW_GOOGLE_ACCOUNT_NAME = 'Gmail account';
export const NEW_TRELLO_ACCOUNT_NAME = 'Trello account';
export const NEW_NOTION_ACCOUNT_NAME = 'Notion account';
export const NEW_QUERY_AUTH_ACCOUNT_NAME = 'Query Auth account';
export const E2E_TEST_NODE_NAME = 'E2E Test';

export const ROUTES = {
	NEW_WORKFLOW_PAGE: '/workflow/new',
};
