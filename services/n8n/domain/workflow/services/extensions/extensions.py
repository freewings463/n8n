"""
MIGRATION-META:
  source_path: packages/workflow/src/extensions/extensions.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/extensions 的工作流模块。导入/依赖:外部:@codemirror/autocomplete；内部:无；本地:无。导出:Alias、AliasCompletion、ExtensionMap、Extension、NativeDoc、DocMetadataArgument、DocMetadataExample、DocMetadata。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/extensions/extensions.ts -> services/n8n/domain/workflow/services/extensions/extensions.py

import type { Completion } from '@codemirror/autocomplete';

export type Alias = { label: string; info?: string; mode?: 'prefix' | 'exact' };
export interface AliasCompletion extends Completion {
	alias?: Alias[];
}

export interface ExtensionMap {
	typeName: string;
	functions: Record<string, Extension>;
}

// eslint-disable-next-line @typescript-eslint/no-restricted-types
export type Extension = Function & { doc?: DocMetadata };

export type NativeDoc = {
	typeName: string;
	properties?: Record<string, { doc?: DocMetadata }>;
	functions: Record<string, { doc?: DocMetadata }>;
};

export type DocMetadataArgument = {
	name: string;
	type?: string;
	optional?: boolean;
	variadic?: boolean;
	description?: string;
	default?: string;
	// Function arguments have nested arguments
	args?: DocMetadataArgument[];
};
export type DocMetadataExample = {
	example: string;
	evaluated?: string;
	description?: string;
};

export type DocMetadata = {
	name: string;
	returnType: string;
	description?: string;
	section?: string;
	hidden?: boolean;
	aliases?: string[];
	aliasMode?: 'prefix' | 'exact';
	args?: DocMetadataArgument[];
	examples?: DocMetadataExample[];
	docURL?: string;
};
