"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/load-options-context.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context 的执行模块。导入/依赖:外部:lodash/get；内部:无；本地:./node-execution-context、./utils/data-table-helper-functions、./utils/extract-value、./utils/request-helper-functions 等1项。导出:LoadOptionsContext。关键函数/方法:getCurrentNodeParameter、getCurrentNodeParameters。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/load-options-context.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/load_options_context.py

import get from 'lodash/get';
import type {
	ICredentialDataDecryptedObject,
	IGetNodeParameterOptions,
	INode,
	ILoadOptionsFunctions,
	IWorkflowExecuteAdditionalData,
	NodeParameterValueType,
	Workflow,
} from 'n8n-workflow';

import { NodeExecutionContext } from './node-execution-context';
import { getDataTableHelperFunctions } from './utils/data-table-helper-functions';
import { extractValue } from './utils/extract-value';
import { getRequestHelperFunctions } from './utils/request-helper-functions';
import { getSSHTunnelFunctions } from './utils/ssh-tunnel-helper-functions';

export class LoadOptionsContext extends NodeExecutionContext implements ILoadOptionsFunctions {
	readonly helpers: ILoadOptionsFunctions['helpers'];

	constructor(
		workflow: Workflow,
		node: INode,
		additionalData: IWorkflowExecuteAdditionalData,
		private readonly path: string,
	) {
		super(workflow, node, additionalData, 'internal');

		this.helpers = {
			...getSSHTunnelFunctions(),
			...getRequestHelperFunctions(workflow, node, additionalData),
			...getDataTableHelperFunctions(additionalData, workflow, node),
		};
	}

	async getCredentials<T extends object = ICredentialDataDecryptedObject>(type: string) {
		return await this._getCredentials<T>(type);
	}

	getCurrentNodeParameter(
		parameterPath: string,
		options?: IGetNodeParameterOptions,
	): NodeParameterValueType | object | undefined {
		const nodeParameters = this.additionalData.currentNodeParameters;

		if (parameterPath.charAt(0) === '&') {
			parameterPath = `${this.path.split('.').slice(1, -1).join('.')}.${parameterPath.slice(1)}`;
		}

		let returnData = get(nodeParameters, parameterPath);

		// This is outside the try/catch because it throws errors with proper messages
		if (options?.extractValue) {
			const nodeType = this.workflow.nodeTypes.getByNameAndVersion(
				this.node.type,
				this.node.typeVersion,
			);
			returnData = extractValue(
				returnData,
				parameterPath,
				this.node,
				nodeType,
			) as NodeParameterValueType;
		}

		return returnData;
	}

	getCurrentNodeParameters() {
		return this.additionalData.currentNodeParameters;
	}
}
