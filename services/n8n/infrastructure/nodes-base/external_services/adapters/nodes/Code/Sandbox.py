"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/Sandbox.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的节点。导入/依赖:外部:无；内部:无；本地:./result-validation。导出:SandboxContext、getSandboxContext。关键函数/方法:getSandboxContext、validateRunCodeEachItem、validateRunCodeAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/Sandbox.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/Sandbox.py

import { EventEmitter } from 'events';
import type {
	IExecuteFunctions,
	INodeExecutionData,
	ISupplyDataFunctions,
	IWorkflowDataProxyData,
} from 'n8n-workflow';

import { validateRunCodeAllItems, validateRunCodeEachItem } from './result-validation';

interface SandboxTextKeys {
	object: {
		singular: string;
		plural: string;
	};
}

export interface SandboxContext extends IWorkflowDataProxyData {
	$getNodeParameter: IExecuteFunctions['getNodeParameter'];
	$getWorkflowStaticData: IExecuteFunctions['getWorkflowStaticData'];
	helpers: IExecuteFunctions['helpers'];
}

export function getSandboxContext(
	this: IExecuteFunctions | ISupplyDataFunctions,
	index: number,
): SandboxContext {
	const helpers = {
		...this.helpers,
		httpRequestWithAuthentication: this.helpers.httpRequestWithAuthentication.bind(this),
		requestWithAuthenticationPaginated: this.helpers.requestWithAuthenticationPaginated.bind(this),
	};
	return {
		// from NodeExecuteFunctions
		$getNodeParameter: this.getNodeParameter.bind(this),
		$getWorkflowStaticData: this.getWorkflowStaticData.bind(this),
		helpers,

		// to bring in all $-prefixed vars and methods from WorkflowDataProxy
		// $node, $items(), $parameter, $json, $env, etc.
		...this.getWorkflowDataProxy(index),
	};
}

export abstract class Sandbox extends EventEmitter {
	constructor(
		private textKeys: SandboxTextKeys,
		protected helpers: IExecuteFunctions['helpers'],
	) {
		super();
	}

	abstract runCode<T = unknown>(): Promise<T>;

	abstract runCodeAllItems(): Promise<INodeExecutionData[] | INodeExecutionData[][]>;

	abstract runCodeEachItem(itemIndex: number): Promise<INodeExecutionData | undefined>;

	validateRunCodeEachItem(
		executionResult: INodeExecutionData | undefined,
		itemIndex: number,
	): INodeExecutionData {
		return validateRunCodeEachItem(
			executionResult,
			itemIndex,
			this.textKeys,
			this.helpers.normalizeItems.bind(this.helpers),
		);
	}

	validateRunCodeAllItems(
		executionResult: INodeExecutionData | INodeExecutionData[] | undefined,
	): INodeExecutionData[] {
		return validateRunCodeAllItems(
			executionResult,
			this.textKeys,
			this.helpers.normalizeItems.bind(this.helpers),
		);
	}
}
