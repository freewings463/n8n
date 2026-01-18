"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Merge/v3/helpers/interfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Merge/v3 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:MatchFieldsOptions、ClashResolveOptions、MatchFieldsOutput、MatchFieldsJoinMode。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Merge/v3/helpers/interfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Merge/v3/helpers/interfaces.py

type MultipleMatches = 'all' | 'first';

export type MatchFieldsOptions = {
	joinMode: MatchFieldsJoinMode;
	outputDataFrom: MatchFieldsOutput;
	multipleMatches: MultipleMatches;
	disableDotNotation: boolean;
	fuzzyCompare?: boolean;
};

type ClashMergeMode = 'deepMerge' | 'shallowMerge';
type ClashResolveMode = 'addSuffix' | 'preferInput1' | 'preferLast';

export type ClashResolveOptions = {
	resolveClash: ClashResolveMode;
	mergeMode: ClashMergeMode;
	overrideEmpty: boolean;
};

export type MatchFieldsOutput = 'both' | 'input1' | 'input2';

export type MatchFieldsJoinMode =
	| 'keepEverything'
	| 'keepMatches'
	| 'keepNonMatches'
	| 'enrichInput2'
	| 'enrichInput1';
