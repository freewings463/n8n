"""
MIGRATION-META:
  source_path: packages/testing/playwright/Types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright 的类型。导入/依赖:外部:无；内部:@n8n/api-types；本地:无。导出:TestError、TestRequirements、InterceptConfig。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/Types.ts -> services/n8n/tests/testing/integration/ui/playwright/Types.py

import type { FrontendSettings } from '@n8n/api-types';

export class TestError extends Error {
	constructor(message: string) {
		super(message);
		this.name = 'TestError';
	}
}

/**
 * Test requirements for Playwright tests.
 *
 * This interface allows you to declaratively specify all test setup requirements
 * in one place, making tests more readable and maintainable.
 * If a workflow is specified, the starting point for the test is now the canvas after the workflow is imported.
 *
 * @example
 * ```typescript
 * const requirements: TestRequirements = {
 *   config: {
 *     features: {
 *       aiAssistant: true,
 *       debugInEditor: true,
 *       sharing: true
 *     },
 *     settings: { telemetry: { enabled: false } }
 *   },
 *   workflow: {
 *     'ai_assistant_test_workflow.json': 'AI Assistant Test Workflow'
 *   },
 *   intercepts: {
 *     'ai-chat': {
 *       url: '*\/rest/ai/chat',
 *       response: { sessionId: '1', messages: [] }
 *     }
 *   },
 *   storage: {
 *     'n8n-telemetry': '{"enabled": true}'
 *   }
 * };
 * ```
 */
export interface TestRequirements {
	/**
	 * Configuration settings for the test environment
	 */
	config?: {
		/** Frontend settings to override (merged with default settings) */
		settings?: Partial<FrontendSettings>;

		/** Feature flags to enable/disable for the test */
		features?: Record<string, boolean>;
	};

	/**
	 * API route intercepts and their mock responses
	 *
	 * @example
	 * ```typescript
	 * intercepts: {
	 *   'ai-chat': {
	 *     url: '*\/rest/ai/chat',
	 *     response: {
	 *       sessionId: '1',
	 *       messages: [{ role: 'assistant', type: 'message', text: 'Hello!' }]
	 *     }
	 *   },
	 *   'become-creator': {
	 *     url: '*\/rest/cta/become-creator',
	 *     response: true
	 *   },
	 *   'credentials-test': {
	 *     url: '*\/rest/credentials/test',
	 *     response: { data: { status: 'success', message: 'Tested successfully' } }
	 *   }
	 * }
	 * ```
	 */
	intercepts?: Record<string, InterceptConfig>;

	/**
	 * Single workflow to import for the test
	 *
	 * Key: Import file location (relative to workflows folder)
	 * Value: Name to give the workflow when imported
	 *
	 * Note: Only one workflow is supported. Multiple workflows will throw an error.
	 *
	 * @example
	 * ```typescript
	 * workflow: {
	 *   'ai_assistant_test_workflow.json': 'AI Assistant Test Workflow'
	 * }
	 * ```
	 */
	workflow?: string | Record<string, string>;

	/**
	 * Browser storage values to set before the test
	 *
	 * Supports localStorage, sessionStorage, and other browser storage APIs
	 *
	 * @example
	 * ```typescript
	 * storage: {
	 *   'n8n-telemetry': '{"enabled": true}',
	 *   'n8n-instance-id': 'test-instance-id'
	 * }
	 * ```
	 */
	storage?: Record<string, string>;
}

/**
 * Configuration for API route interception in Playwright
 *
 * @example
 * ```typescript
 * {
 *   url: '*\/rest/ai/chat',
 *   response: { sessionId: '1', messages: [] },
 *   status: 200
 * }
 * ```
 *
 * @example Network error simulation
 * ```typescript
 * {
 *   url: '*\/rest/credentials/test',
 *   forceNetworkError: true
 * }
 * ```
 */
export interface InterceptConfig {
	/** URL pattern to intercept (supports wildcards) */
	url: string;

	/** Mock response data */
	response?: unknown;

	/** HTTP status code to return (default: 200) */
	status?: number;

	/** HTTP headers to return */
	headers?: Record<string, string>;

	/** Content type for the response (default: 'application/json') */
	contentType?: string;

	/** Force network error instead of mock response */
	forceNetworkError?: boolean;
}
