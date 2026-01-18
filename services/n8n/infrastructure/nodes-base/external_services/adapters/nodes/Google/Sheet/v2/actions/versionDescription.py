"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./sheet/Sheet.resource、./spreadsheet/SpreadSheet.resource。导出:authentication、versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/actions/versionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import type { INodeProperties, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import * as sheet from './sheet/Sheet.resource';
import * as spreadsheet from './spreadsheet/SpreadSheet.resource';

export const authentication: INodeProperties = {
	displayName: 'Authentication',
	name: 'authentication',
	type: 'options',
	options: [
		{
			name: 'Service Account',
			value: 'serviceAccount',
		},
		{
			// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
			name: 'OAuth2 (recommended)',
			value: 'oAuth2',
		},
	],
	default: 'oAuth2',
};

export const versionDescription: INodeTypeDescription = {
	displayName: 'Google Sheets',
	name: 'googleSheets',
	icon: 'file:googleSheets.svg',
	group: ['input', 'output'],
	version: [3, 4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7],
	subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
	description: 'Read, update and write data to Google Sheets',
	defaults: {
		name: 'Google Sheets',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	usableAsTool: true,
	hints: [
		{
			message:
				"Use the 'Minimise API Calls' option for greater efficiency if your sheet is uniformly formatted without gaps between columns or rows",
			displayCondition:
				'={{$parameter["operation"] === "append" && !$parameter["options"]["useAppend"]}}',
			whenToDisplay: 'beforeExecution',
			location: 'outputPane',
		},
		{
			message: 'No columns found in Google Sheet. All rows will be appended',
			displayCondition:
				'={{ ["appendOrUpdate", "append"].includes($parameter["operation"]) && $parameter?.columns?.mappingMode === "defineBelow" && !$parameter?.columns?.schema?.length }}',
			whenToDisplay: 'beforeExecution',
			location: 'outputPane',
		},
		{
			type: 'info',
			message:
				'Note on using an expression for Sheet: It will be evaluated only once, so all items will use the <em>same</em> sheet. It will be calculated by evaluating the expression for the <strong>first input item</strong>.',
			displayCondition:
				'={{ $rawParameter.sheetName?.startsWith("=") && $input.all().length > 1 }}',
			whenToDisplay: 'always',
			location: 'outputPane',
		},
		{
			type: 'info',
			message:
				'Note on using an expression for Document: It will be evaluated only once, so all items will use the <em>same</em> document. It will be calculated by evaluating the expression for the <strong>first input item</strong>.',
			displayCondition:
				'={{ $rawParameter.documentId?.startsWith("=") && $input.all().length > 1 }}',
			whenToDisplay: 'always',
			location: 'outputPane',
		},
	],
	credentials: [
		{
			name: 'googleApi',
			required: true,
			displayOptions: {
				show: {
					authentication: ['serviceAccount'],
				},
			},
			testedBy: 'googleApiCredentialTest',
		},
		{
			name: 'googleSheetsOAuth2Api',
			required: true,
			displayOptions: {
				show: {
					authentication: ['oAuth2'],
				},
			},
		},
	],
	properties: [
		authentication,
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			options: [
				{
					name: 'Document',
					value: 'spreadsheet',
				},
				{
					name: 'Sheet Within Document',
					value: 'sheet',
				},
			],
			default: 'sheet',
		},
		...sheet.descriptions,
		...spreadsheet.descriptions,
	],
};
