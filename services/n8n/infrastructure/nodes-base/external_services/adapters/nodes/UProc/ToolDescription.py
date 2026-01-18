"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UProc/ToolDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UProc 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./Json/Groups、./Json/Tools。导出:toolOperations、toolParameters。关键函数/方法:capitalize。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UProc/ToolDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UProc/ToolDescription.py

import type { IDataObject, INodeProperties } from 'n8n-workflow';
import { deepCopy } from 'n8n-workflow';

import { groups } from './Json/Groups';
import { tools } from './Json/Tools';

function capitalize(str: string): string {
	if (!str) {
		return '';
	} else {
		return str.charAt(0).toUpperCase() + str.slice(1);
	}
}

const operations = [];

for (const group of (groups as IDataObject).groups as IDataObject[]) {
	const item = {
		displayName: 'Operation',
		name: 'tool',
		type: 'options',
		description: 'The Operation to consume',
		displayOptions: {
			show: {
				group: [group.name],
			},
		},
		default: '',
		options: [],
	};

	const options = [];
	for (const tool of (tools as IDataObject).processors as IDataObject[]) {
		if (tool.g === group.name) {
			const link =
				'https://app.uproc.io/#/tools/processor/' +
				(tool.k as string)
					.replace(/([A-Z]+)/g, '-$1')
					.toLowerCase()
					.replace('-', '/')
					.replace('-', '/');
			const option = {
				name: tool.d as string,
				value: tool.k,
				description: (tool.ed as string) + ` <a href="${link}" target='_blank'>Info</a>`,
			};
			options.push(option);
		}
	}

	//Tool
	item.options = options.sort((a, b) => (a.name > b.name ? 1 : -1)) as any;
	item.default = options[0].value as string;
	operations.push(item);
}

export const toolOperations = operations as INodeProperties[];

let parameters = [];
//all tools
for (const tool of (tools as IDataObject).processors as IDataObject[]) {
	//all parameters in tool
	for (const param of tool.p as IDataObject[]) {
		const displayName = param.n as string;
		const capitalizedDisplayName = capitalize(displayName.replace(/_/g, ' '));
		const description = `The "${capitalizedDisplayName}" value to use as a parameter for this Operation`;
		const parameter = {
			displayName: capitalizedDisplayName,
			name: param.n,
			type: param.t,
			default: '',
			placeholder: param.p,
			required: param.r,
			options: param.o,
			displayOptions: {
				show: {
					group: [tool.g],
					tool: [tool.k],
				},
			},
			description: deepCopy(description),
		};

		let modifiedParam = null;
		//Check if param exists previously
		for (const currentParam of parameters) {
			//Get old param in parameters array
			if (currentParam.name === param.n) {
				modifiedParam = currentParam;
			}
		}
		//if exists, other wise
		if (modifiedParam) {
			//Assign new group and tool
			modifiedParam.displayOptions.show.group.push(tool.g);
			modifiedParam.displayOptions.show.tool.push(tool.k);

			//build new array
			const newParameters = [];
			for (const currentParam of parameters) {
				//Get old param in parameters array
				if (currentParam.name === modifiedParam.name) {
					newParameters.push(modifiedParam);
				} else {
					newParameters.push(currentParam);
				}
			}
			// eslint-disable-next-line n8n-local-rules/no-json-parse-json-stringify
			parameters = JSON.parse(JSON.stringify(newParameters));
		} else {
			parameters.push(parameter);
		}
	}
}

export const toolParameters = parameters as INodeProperties[];
