"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/JavaScriptSandbox.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的节点。导入/依赖:外部:无；内部:@n8n/vm2、n8n-workflow；本地:./ExecutionError、./Sandbox、./ValidationError。导出:vmResolver、JavaScriptSandbox。关键函数/方法:executionResult、runCodeAllItems、mapItemsNotDefinedErrorIfNeededForRunForAll、runCodeEachItem、validateNoDisallowedMethodsInRunForEach、mapItemNotDefinedErrorIfNeededForRunForEach。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/JavaScriptSandbox.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/JavaScriptSandbox.py

import { NodeVM, makeResolverFromLegacyOptions, type Resolver } from '@n8n/vm2';
import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';

import { ExecutionError } from './ExecutionError';
import {
	mapItemNotDefinedErrorIfNeededForRunForEach,
	mapItemsNotDefinedErrorIfNeededForRunForAll,
	validateNoDisallowedMethodsInRunForEach,
} from './JsCodeValidator';
import type { SandboxContext } from './Sandbox';
import { Sandbox } from './Sandbox';
import { ValidationError } from './ValidationError';

const { NODE_FUNCTION_ALLOW_BUILTIN: builtIn, NODE_FUNCTION_ALLOW_EXTERNAL: external } =
	process.env;

export const vmResolver = makeResolverFromLegacyOptions({
	external: external
		? {
				modules: external.split(','),
				transitive: false,
			}
		: false,
	builtin: builtIn?.split(',') ?? [],
});

export class JavaScriptSandbox extends Sandbox {
	private readonly vm: NodeVM;

	constructor(
		context: SandboxContext,
		private jsCode: string,
		helpers: IExecuteFunctions['helpers'],
		options?: { resolver?: Resolver },
	) {
		super(
			{
				object: {
					singular: 'object',
					plural: 'objects',
				},
			},
			helpers,
		);
		this.vm = new NodeVM({
			console: 'redirect',
			sandbox: context,
			require: options?.resolver ?? vmResolver,
			wasm: false,
		});

		this.vm.on('console.log', (...args: unknown[]) => this.emit('output', ...args));
	}

	async runCode<T = unknown>(): Promise<T> {
		const script = `module.exports = async function() {${this.jsCode}\n}()`;
		try {
			const executionResult = (await this.vm.run(script, __dirname)) as T;
			return executionResult;
		} catch (error) {
			throw new ExecutionError(error);
		}
	}

	async runCodeAllItems(options?: {
		multiOutput?: boolean;
	}): Promise<INodeExecutionData[] | INodeExecutionData[][]> {
		const script = `module.exports = async function() {${this.jsCode}\n}()`;

		let executionResult: INodeExecutionData | INodeExecutionData[] | INodeExecutionData[][];

		try {
			executionResult = await this.vm.run(script, __dirname);
		} catch (error) {
			// anticipate user expecting `items` to pre-exist as in Function Item node
			mapItemsNotDefinedErrorIfNeededForRunForAll(this.jsCode, error);

			throw new ExecutionError(error);
		}

		if (executionResult === null) return [];

		if (options?.multiOutput === true) {
			// Check if executionResult is an array of arrays
			if (!Array.isArray(executionResult) || executionResult.some((item) => !Array.isArray(item))) {
				throw new ValidationError({
					message: "The code doesn't return an array of arrays",
					description:
						'Please return an array of arrays. One array for the different outputs and one for the different items that get returned.',
				});
			}

			return executionResult.map((data) => {
				return this.validateRunCodeAllItems(data);
			});
		}

		return this.validateRunCodeAllItems(
			executionResult as INodeExecutionData | INodeExecutionData[],
		);
	}

	async runCodeEachItem(itemIndex: number): Promise<INodeExecutionData | undefined> {
		const script = `module.exports = async function() {${this.jsCode}\n}()`;

		validateNoDisallowedMethodsInRunForEach(this.jsCode, itemIndex);

		let executionResult: INodeExecutionData;

		try {
			executionResult = await this.vm.run(script, __dirname);
		} catch (error) {
			// anticipate user expecting `item` to pre-exist as in Function Item node
			mapItemNotDefinedErrorIfNeededForRunForEach(this.jsCode, error);

			throw new ExecutionError(error, itemIndex);
		}

		if (executionResult === null) return undefined;

		return this.validateRunCodeEachItem(executionResult, itemIndex);
	}
}
