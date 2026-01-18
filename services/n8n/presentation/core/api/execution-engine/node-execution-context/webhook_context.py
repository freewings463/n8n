"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/webhook-context.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context 的Webhook模块。导入/依赖:外部:express；内部:n8n-workflow；本地:./node-execution-context、./utils/binary-helper-functions 等4项。导出:WebhookContext。关键函数/方法:getBodyData、getHeaderData、getParamsData、getQueryData、getRequestObject、getResponseObject、assertHttpRequest、getNodeWebhookUrl、getWebhookName、getInputConnectionData。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/webhook-context.ts -> services/n8n/presentation/core/api/execution-engine/node-execution-context/webhook_context.py

import type { Request, Response } from 'express';
import type {
	AINodeConnectionType,
	CloseFunction,
	ICredentialDataDecryptedObject,
	IDataObject,
	IExecuteData,
	INode,
	INodeExecutionData,
	IRunExecutionData,
	ITaskDataConnections,
	IWebhookData,
	IWebhookFunctions,
	IWorkflowExecuteAdditionalData,
	WebhookType,
	Workflow,
	WorkflowExecuteMode,
} from 'n8n-workflow';
import { ApplicationError, createDeferredPromise, createEmptyRunExecutionData } from 'n8n-workflow';

import { NodeExecutionContext } from './node-execution-context';
import { copyBinaryFile, getBinaryHelperFunctions } from './utils/binary-helper-functions';
import { getInputConnectionData } from './utils/get-input-connection-data';
import { getRequestHelperFunctions } from './utils/request-helper-functions';
import { returnJsonArray } from './utils/return-json-array';
import { getNodeWebhookUrl } from './utils/webhook-helper-functions';
export class WebhookContext extends NodeExecutionContext implements IWebhookFunctions {
	readonly helpers: IWebhookFunctions['helpers'];

	readonly nodeHelpers: IWebhookFunctions['nodeHelpers'];

	constructor(
		workflow: Workflow,
		node: INode,
		additionalData: IWorkflowExecuteAdditionalData,
		mode: WorkflowExecuteMode,
		private readonly webhookData: IWebhookData,
		private readonly closeFunctions: CloseFunction[],
		runExecutionData: IRunExecutionData | null,
	) {
		let connectionInputData: INodeExecutionData[] = [];
		let executionData: IExecuteData | undefined;

		if (runExecutionData?.executionData !== undefined) {
			executionData = runExecutionData.executionData.nodeExecutionStack[0];
			if (executionData !== undefined) {
				connectionInputData = executionData.data.main[0]!;
			}
		}

		super(
			workflow,
			node,
			additionalData,
			mode,
			runExecutionData,
			0,
			connectionInputData,
			executionData,
		);

		this.helpers = {
			createDeferredPromise,
			returnJsonArray,
			...getRequestHelperFunctions(workflow, node, additionalData),
			...getBinaryHelperFunctions(additionalData, workflow.id),
		};

		this.nodeHelpers = {
			copyBinaryFile: async (filePath, fileName, mimeType) =>
				await copyBinaryFile(
					this.workflow.id,
					this.additionalData.executionId!,
					filePath,
					fileName,
					mimeType,
				),
		};
	}

	async getCredentials<T extends object = ICredentialDataDecryptedObject>(type: string) {
		return await this._getCredentials<T>(type);
	}

	getBodyData() {
		return this.assertHttpRequest().body as IDataObject;
	}

	getHeaderData() {
		return this.assertHttpRequest().headers;
	}

	getParamsData(): object {
		return this.assertHttpRequest().params;
	}

	getQueryData(): object {
		return this.assertHttpRequest().query;
	}

	getRequestObject(): Request {
		return this.assertHttpRequest();
	}

	getResponseObject(): Response {
		if (this.additionalData.httpResponse === undefined) {
			throw new ApplicationError('Response is missing');
		}
		return this.additionalData.httpResponse;
	}

	private assertHttpRequest() {
		const { httpRequest } = this.additionalData;
		if (httpRequest === undefined) {
			throw new ApplicationError('Request is missing');
		}
		return httpRequest;
	}

	getNodeWebhookUrl(name: WebhookType): string | undefined {
		return getNodeWebhookUrl(
			name,
			this.workflow,
			this.node,
			this.additionalData,
			this.mode,
			this.additionalKeys,
		);
	}

	getWebhookName() {
		return this.webhookData.webhookDescription.name;
	}

	async getInputConnectionData(
		connectionType: AINodeConnectionType,
		itemIndex: number,
	): Promise<unknown> {
		// To be able to use expressions like "$json.sessionId" set the
		// body data the webhook received to what is normally used for
		// incoming node data.
		const connectionInputData: INodeExecutionData[] = [
			// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
			{ json: this.additionalData.httpRequest?.body || {} },
		];
		const runExecutionData = this.runExecutionData ?? createEmptyRunExecutionData();
		const executeData: IExecuteData = {
			data: {
				main: [connectionInputData],
			},
			node: this.node,
			source: null,
		};

		return await getInputConnectionData.call(
			this,
			this.workflow,
			runExecutionData,
			this.runIndex,
			connectionInputData,
			{} as ITaskDataConnections,
			this.additionalData,
			executeData,
			this.mode,
			this.closeFunctions,
			connectionType,
			itemIndex,
		);
	}
}
