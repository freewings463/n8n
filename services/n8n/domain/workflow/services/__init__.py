"""
MIGRATION-META:
  source_path: packages/workflow/src/index.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流入口。导入/依赖:外部:无；内部:无；本地:./logger-proxy、./node-helpers、./observable-object、./telemetry-helpers。再导出:./errors、./constants、./common、./cron 等32项。导出:LoggerProxy、NodeHelpers、ObservableObject、TelemetryHelpers、ExpressionExtensions、type Alias、type AliasCompletion、NativeMethods 等1项。关键函数/方法:readRawBody。用于汇总导出并完成工作流模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/index.ts -> services/n8n/domain/workflow/services/__init__.py

import * as LoggerProxy from './logger-proxy';
import * as NodeHelpers from './node-helpers';
import * as ObservableObject from './observable-object';
import * as TelemetryHelpers from './telemetry-helpers';

export * from './errors';
export * from './constants';
export * from './common';
export * from './cron';
export * from './data-table.types';
export * from './deferred-promise';
export * from './execution-context';
export * from './execution-context-establishment-hooks';
export * from './global-state';
export * from './interfaces';
export * from './run-execution-data-factory';
export * from './message-event-bus';
export * from './execution-status';
export * from './expression';
export * from './expressions/expression-helpers';
export * from './from-ai-parse-utils';
export * from './node-helpers';
export * from './tool-helpers';
export * from './node-reference-parser-utils';
export * from './metadata-utils';
export * from './workflow';
export * from './workflow-checksum';
export * from './workflow-data-proxy';
export * from './workflow-data-proxy-env-provider';
export * from './workflow-validation';
export * from './versioned-node-type';
export * from './type-validation';
export * from './result';
export * from './schemas';
export * from './run-execution-data/run-execution-data';
export { LoggerProxy, NodeHelpers, ObservableObject, TelemetryHelpers };
export {
	isObjectEmpty,
	deepCopy,
	jsonParse,
	base64DecodeUTF8,
	jsonStringify,
	replaceCircularReferences,
	sleep,
	sleepWithAbort,
	fileTypeFromMimeType,
	assert,
	removeCircularRefs,
	updateDisplayOptions,
	randomInt,
	randomString,
	isSafeObjectProperty,
	setSafeObjectProperty,
	isDomainAllowed,
	isCommunityPackageName,
	dedupe,
	sanitizeFilename,
} from './utils';
export {
	isINodeProperties,
	isINodePropertyOptions,
	isINodePropertyCollection,
	isINodePropertiesList,
	isINodePropertyCollectionList,
	isINodePropertyOptionsList,
	isResourceMapperValue,
	isResourceLocatorValue,
	isFilterValue,
	isNodeConnectionType,
	isBinaryValue,
} from './type-guards';

export {
	parseExtractableSubgraphSelection,
	buildAdjacencyList,
	type ExtractableErrorResult,
	type ExtractableSubgraphData,
	type IConnectionAdjacencyList as AdjacencyList,
} from './graph/graph-utils';
export { ExpressionExtensions, type Alias, type AliasCompletion } from './extensions';
export * as ExpressionParser from './extensions/expression-parser';
export { NativeMethods } from './native-methods';
export * from './node-parameters/filter-parameter';
export * from './node-parameters/parameter-type-validation';
export * from './node-parameters/node-parameter-value-type-guard';
export * from './node-parameters/path-utils';
export * from './evaluation-helpers';
export * from './workflow-diff';

export type {
	DocMetadata,
	NativeDoc,
	DocMetadataArgument,
	DocMetadataExample,
	Extension,
} from './extensions';

declare module 'http' {
	export interface IncomingMessage {
		contentType?: string;
		encoding: BufferEncoding;
		contentDisposition?: { type: string; filename?: string };
		rawBody: Buffer;
		readRawBody(): Promise<void>;
		_body: boolean;

		// This gets added by the `follow-redirects` package
		responseUrl?: string;

		// This is added to response objects for all outgoing requests
		req?: ClientRequest;
	}
}
