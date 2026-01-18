"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/helpers/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的节点。导入/依赖:外部:xml2js；内部:n8n-workflow；本地:./interfaces、../v1/types。导出:formatEntry、extractErrorDescription、toUnixEpoch、formatFeed、setReturnAllOrLimit、populate、getId。关键函数/方法:compactEntryContent、formatEntryContent、formatEntry、parseXml、parseString、extractErrorDescription、toUnixEpoch、formatFeed、setReturnAllOrLimit、populate 等1项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/helpers/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/helpers/utils.py

import type { IExecuteFunctions, IDataObject } from 'n8n-workflow';
import { parseString } from 'xml2js';

import type { SplunkError, SplunkFeedResponse } from './interfaces';
import { SPLUNK } from '../../v1/types';

function compactEntryContent(splunkObject: any): any {
	if (typeof splunkObject !== 'object') {
		return {};
	}

	if (Array.isArray(splunkObject)) {
		return splunkObject.reduce((acc, cur) => {
			acc = { ...acc, ...compactEntryContent(cur) };
			return acc;
		}, {});
	}

	if (splunkObject[SPLUNK.DICT]) {
		const obj = splunkObject[SPLUNK.DICT][SPLUNK.KEY];
		return { [splunkObject.$.name]: compactEntryContent(obj) };
	}

	if (splunkObject[SPLUNK.LIST]) {
		const items = splunkObject[SPLUNK.LIST][SPLUNK.ITEM];
		return { [splunkObject.$.name]: items };
	}

	if (splunkObject._) {
		return {
			[splunkObject.$.name]: splunkObject._,
		};
	}

	return {
		[splunkObject.$.name]: '',
	};
}

function formatEntryContent(content: any): any {
	return content[SPLUNK.DICT][SPLUNK.KEY].reduce((acc: any, cur: any) => {
		acc = { ...acc, ...compactEntryContent(cur) };
		return acc;
	}, {});
}

export function formatEntry(entry: any, doNotFormatContent = false): any {
	const { content, link, ...rest } = entry;
	const formattedContent = doNotFormatContent ? content : formatEntryContent(content);
	const formattedEntry = { ...rest, ...formattedContent };

	if (formattedEntry.id) {
		formattedEntry.entryUrl = formattedEntry.id;
		formattedEntry.id = formattedEntry.id.split('/').pop();
	}

	return formattedEntry;
}

export async function parseXml(xml: string) {
	return await new Promise((resolve, reject) => {
		parseString(xml, { explicitArray: false }, (error, result) => {
			error ? reject(error) : resolve(result);
		});
	});
}

export function extractErrorDescription(rawError: SplunkError) {
	const messages = rawError.response?.messages;
	return messages ? { [messages.msg.$.type.toLowerCase()]: messages.msg._ } : rawError;
}

export function toUnixEpoch(timestamp: string) {
	return Date.parse(timestamp) / 1000;
}

export function formatFeed(responseData: SplunkFeedResponse) {
	const { entry: entries } = responseData.feed;

	if (!entries) return [];

	return Array.isArray(entries)
		? entries.map((entry) => formatEntry(entry))
		: [formatEntry(entries)];
}

export function setReturnAllOrLimit(this: IExecuteFunctions, qs: IDataObject) {
	qs.count = this.getNodeParameter('returnAll', 0) ? 0 : this.getNodeParameter('limit', 0);
}

export function populate(source: IDataObject, destination: IDataObject) {
	if (Object.keys(source).length) {
		Object.assign(destination, source);
	}
}

export function getId(
	this: IExecuteFunctions,
	i: number,
	idType: 'userId' | 'searchJobId' | 'searchConfigurationId',
	endpoint: string,
) {
	const id = this.getNodeParameter(idType, i) as string;

	return id.includes(endpoint) ? id.split(endpoint).pop() : id;
}
