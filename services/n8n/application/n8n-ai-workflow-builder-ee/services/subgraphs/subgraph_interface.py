"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/subgraphs/subgraph-interface.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/subgraphs 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:ISubgraph。关键函数/方法:create。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/subgraphs/subgraph-interface.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/subgraphs/subgraph_interface.py

type StateRecord = Record<string, unknown>;

interface InvokeConfig {
	recursionLimit?: number;
}

export interface ISubgraph<
	TConfig = unknown,
	TChildState extends StateRecord = StateRecord,
	TParentState extends StateRecord = StateRecord,
> {
	name: string;
	description: string;
	create(config: TConfig): {
		invoke: (input: Partial<TChildState>, config?: InvokeConfig) => Promise<TChildState>;
	};
	transformInput: (parentState: TParentState) => Partial<TChildState>;
	transformOutput: (childOutput: TChildState, parentState: TParentState) => Partial<TParentState>;
}

export abstract class BaseSubgraph<
	TConfig = unknown,
	TChildState extends StateRecord = StateRecord,
	TParentState extends StateRecord = StateRecord,
> implements ISubgraph<TConfig, TChildState, TParentState>
{
	abstract name: string;
	abstract description: string;

	abstract create(config: TConfig): {
		invoke: (input: Partial<TChildState>, config?: InvokeConfig) => Promise<TChildState>;
	};

	/**
	 * Transform parent state to subgraph input state
	 * Returns a partial object with only the fields needed to initialize the child state
	 */
	abstract transformInput(parentState: TParentState): Partial<TChildState>;

	/**
	 * Transform subgraph output state to parent state update
	 * Returns a partial object that will be merged into the parent state
	 */
	abstract transformOutput(
		childOutput: TChildState,
		parentState: TParentState,
	): Partial<TParentState>;
}
