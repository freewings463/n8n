"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/waiting-forms.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/webhooks 的Webhook模块。导入/依赖:外部:express；内部:@n8n/db、@n8n/di、n8n-workflow、n8n-core、@/errors/…/conflict.error、@/executions/execution.utils 等3项；本地:./webhook-request-sanitizer、./webhook.types。导出:WaitingForms。关键函数/方法:disableNode、getWorkflow、findCompletionPage、executeWebhook、sanitizeWebhookRequest、applyCors。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/waiting-forms.ts -> services/n8n/presentation/cli/api/webhooks/waiting_forms.py

import type { IExecutionResponse } from '@n8n/db';
import { Service } from '@n8n/di';
import type express from 'express';
import type { IRunData } from 'n8n-workflow';
import { getWebhookSandboxCSP } from 'n8n-core';
import {
	FORM_NODE_TYPE,
	WAIT_NODE_TYPE,
	WAITING_FORMS_EXECUTION_STATUS,
	Workflow,
} from 'n8n-workflow';

import { ConflictError } from '@/errors/response-errors/conflict.error';
import { getWorkflowActiveStatusFromWorkflowData } from '@/executions/execution.utils';
import { NotFoundError } from '@/errors/response-errors/not-found.error';
import { WaitingWebhooks } from '@/webhooks/waiting-webhooks';

import { sanitizeWebhookRequest } from './webhook-request-sanitizer';
import type { IWebhookResponseCallbackData, WaitingWebhookRequest } from './webhook.types';
import { applyCors } from '@/utils/cors.util';

@Service()
export class WaitingForms extends WaitingWebhooks {
	protected override includeForms = true;

	protected override logReceivedWebhook(method: string, executionId: string) {
		this.logger.debug(`Received waiting-form "${method}" for execution "${executionId}"`);
	}

	protected disableNode(execution: IExecutionResponse, method?: string) {
		if (method === 'POST') {
			execution.data.executionData!.nodeExecutionStack[0].node.disabled = true;
		}
	}

	protected getWorkflow(execution: IExecutionResponse) {
		const { workflowData } = execution;
		return new Workflow({
			id: workflowData.id,
			name: workflowData.name,
			nodes: workflowData.nodes,
			connections: workflowData.connections,
			active: getWorkflowActiveStatusFromWorkflowData(workflowData),
			nodeTypes: this.nodeTypes,
			staticData: workflowData.staticData,
			settings: workflowData.settings,
		});
	}

	findCompletionPage(workflow: Workflow, runData: IRunData, lastNodeExecuted: string) {
		const parentNodes = workflow.getParentNodes(lastNodeExecuted);
		const lastNode = workflow.nodes[lastNodeExecuted];

		if (
			!lastNode.disabled &&
			lastNode.type === FORM_NODE_TYPE &&
			lastNode.parameters.operation === 'completion'
		) {
			return lastNodeExecuted;
		} else {
			return parentNodes.reverse().find((nodeName) => {
				const node = workflow.nodes[nodeName];
				return (
					!node.disabled &&
					node.type === FORM_NODE_TYPE &&
					node.parameters.operation === 'completion' &&
					runData[nodeName]
				);
			});
		}
	}

	async executeWebhook(
		req: WaitingWebhookRequest,
		res: express.Response,
	): Promise<IWebhookResponseCallbackData> {
		const { path: executionId, suffix } = req.params;

		this.logReceivedWebhook(req.method, executionId);

		sanitizeWebhookRequest(req);

		// Reset request parameters
		req.params = {} as WaitingWebhookRequest['params'];

		const execution = await this.getExecution(executionId);

		if (suffix === WAITING_FORMS_EXECUTION_STATUS) {
			let status: string = execution?.status ?? 'null';
			const { node } = execution?.data.executionData?.nodeExecutionStack[0] ?? {};

			if (node && status === 'waiting') {
				if (node.type === FORM_NODE_TYPE) {
					status = 'form-waiting';
				}
				if (node.type === WAIT_NODE_TYPE && node.parameters.resume === 'form') {
					status = 'form-waiting';
				}
			}

			applyCors(req, res);

			res.send(status);
			return { noWebhookResponse: true };
		}

		if (!execution) {
			throw new NotFoundError(`The execution "${executionId}" does not exist.`);
		}

		if (execution.data.resultData.error) {
			const message = `The execution "${executionId}" has finished with error.`;
			this.logger.debug(message, { error: execution.data.resultData.error });
			throw new ConflictError(message);
		}

		if (execution.status === 'running') {
			return { noWebhookResponse: true };
		}

		let lastNodeExecuted = execution.data.resultData.lastNodeExecuted as string;

		if (execution.finished) {
			// find the completion page to render
			// if there is no completion page, render the default page
			const workflow = this.getWorkflow(execution);

			const completionPage = this.findCompletionPage(
				workflow,
				execution.data.resultData.runData,
				lastNodeExecuted,
			);

			if (!completionPage) {
				res.setHeader('Content-Security-Policy', getWebhookSandboxCSP());
				res.render('form-trigger-completion', {
					title: 'Form Submitted',
					message: 'Your response has been recorded',
					formTitle: 'Form Submitted',
				});

				return {
					noWebhookResponse: true,
				};
			} else {
				lastNodeExecuted = completionPage;
			}
		}

		applyCors(req, res);

		return await this.getWebhookExecutionData({
			execution,
			req,
			res,
			lastNodeExecuted,
			executionId,
			suffix,
		});
	}
}
