"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/hook-context.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context 的执行模块。导入/依赖:外部:无；内部:@n8n/errors；本地:./node-execution-context、./utils/request-helper-functions、./utils/webhook-helper-functions。导出:HookContext。关键函数/方法:getActivationMode、getNodeWebhookUrl、getWebhookName、getWebhookDescription。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/hook-context.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/hook_context.py

import { ApplicationError } from '@n8n/errors';
import type {
	ICredentialDataDecryptedObject,
	INode,
	IHookFunctions,
	IWorkflowExecuteAdditionalData,
	Workflow,
	WorkflowActivateMode,
	WorkflowExecuteMode,
	IWebhookData,
	WebhookType,
} from 'n8n-workflow';

import { NodeExecutionContext } from './node-execution-context';
import { getRequestHelperFunctions } from './utils/request-helper-functions';
import { getNodeWebhookUrl, getWebhookDescription } from './utils/webhook-helper-functions';

export class HookContext extends NodeExecutionContext implements IHookFunctions {
	readonly helpers: IHookFunctions['helpers'];

	constructor(
		workflow: Workflow,
		node: INode,
		additionalData: IWorkflowExecuteAdditionalData,
		mode: WorkflowExecuteMode,
		private readonly activation: WorkflowActivateMode,
		private readonly webhookData?: IWebhookData,
	) {
		super(workflow, node, additionalData, mode);

		this.helpers = getRequestHelperFunctions(workflow, node, additionalData);
	}

	getActivationMode() {
		return this.activation;
	}

	async getCredentials<T extends object = ICredentialDataDecryptedObject>(type: string) {
		return await this._getCredentials<T>(type);
	}

	getNodeWebhookUrl(name: WebhookType): string | undefined {
		return getNodeWebhookUrl(
			name,
			this.workflow,
			this.node,
			this.additionalData,
			this.mode,
			this.additionalKeys,
			this.webhookData?.isTest,
		);
	}

	getWebhookName(): string {
		if (this.webhookData === undefined) {
			throw new ApplicationError('Only supported in webhook functions');
		}
		return this.webhookData.webhookDescription.name;
	}

	getWebhookDescription(name: WebhookType) {
		return getWebhookDescription(name, this.workflow, this.node);
	}
}
