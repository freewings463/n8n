"""
MIGRATION-META:
  source_path: packages/testing/playwright/composables/ExecutionsComposer.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/composables 的执行组合式函数。导入/依赖:外部:无；内部:无；本地:../pages/n8nPage。导出:ExecutionsComposer。关键函数/方法:createExecutions、executeNodeAndCapturePayload。用于封装执行复用逻辑（hooks/composables）供组件组合。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/composables/ExecutionsComposer.ts -> services/n8n/tests/testing/integration/ui/playwright/composables/ExecutionsComposer.py

import type { n8nPage } from '../pages/n8nPage';

/**
 * A class for user interactions with workflow executions that go across multiple pages.
 */
export class ExecutionsComposer {
	constructor(private readonly n8n: n8nPage) {}

	/**
	 * Creates workflow executions by executing the workflow multiple times.
	 * Waits for each execution to complete (by waiting for the POST /rest/workflows/:id/run response)
	 * before starting the next one.
	 *
	 * @param count - Number of executions to create
	 * @example
	 * // Create 10 executions
	 * await n8n.executionsComposer.createExecutions(10);
	 */
	async createExecutions(count: number): Promise<void> {
		for (let i = 0; i < count; i++) {
			const responsePromise = this.n8n.page.waitForResponse(
				(response) =>
					response.url().includes('/rest/workflows/') &&
					response.url().includes('/run') &&
					response.request().method() === 'POST',
			);

			await this.n8n.canvas.clickExecuteWorkflowButton();
			await responsePromise;
		}
	}

	/**
	 * Execute a specific node and capture the workflow run request payload.
	 * Sets up request interception before executing the node, then returns the parsed request body.
	 * Useful for testing the payload structure sent to the workflow run API.
	 *
	 * @param nodeName - The name of the node to execute
	 * @returns The parsed request body from the workflow run API call
	 * @example
	 * // Execute a node and verify payload structure
	 * const payload = await n8n.executionsComposer.executeNodeAndCapturePayload('Process The Data');
	 * expect(payload).toHaveProperty('runData');
	 */
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	async executeNodeAndCapturePayload(nodeName: string): Promise<any> {
		const workflowRunPromise = this.n8n.page.waitForRequest(
			(request) =>
				request.url().includes('/rest/workflows/') &&
				request.url().includes('/run') &&
				request.method() === 'POST',
		);

		await this.n8n.canvas.executeNode(nodeName);

		const workflowRunRequest = await workflowRunPromise;
		return workflowRunRequest.postDataJSON();
	}
}
