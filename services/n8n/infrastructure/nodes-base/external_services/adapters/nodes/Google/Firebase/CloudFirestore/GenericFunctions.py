"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Firebase/CloudFirestore/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Firebase 的节点。导入/依赖:外部:moment-timezone；内部:n8n-workflow；本地:../../GenericFunctions。导出:jsonToDocument、documentToJson、fullDocumentToJson。关键函数/方法:googleApiRequest、googleApiRequestAllItems、isValidDate、moment、jsonToDocument、documentToJson、fullDocumentToJson。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Firebase/CloudFirestore/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Firebase/CloudFirestore/GenericFunctions.py

import moment from 'moment-timezone';
import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { isSafeObjectProperty, NodeApiError } from 'n8n-workflow';

import { getGoogleAccessToken } from '../../GenericFunctions';

export async function googleApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: any = {},
	qs: IDataObject = {},
	uri: string | null = null,
): Promise<any> {
	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs,
		qsStringifyOptions: {
			arrayFormat: 'repeat',
		},
		uri: uri || `https://firestore.googleapis.com/v1/projects${resource}`,
		json: true,
	};
	try {
		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}

		let credentialType = 'googleFirebaseCloudFirestoreOAuth2Api';
		const authentication = this.getNodeParameter('authentication', 0) as string;

		if (authentication === 'serviceAccount') {
			const credentials = await this.getCredentials('googleApi');
			credentialType = 'googleApi';

			const { access_token } = await getGoogleAccessToken.call(this, credentials, 'firestore');

			(options.headers as IDataObject).Authorization = `Bearer ${access_token}`;
		}

		return await this.helpers.requestWithAuthentication.call(this, credentialType, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function googleApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
	uri: string | null = null,
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	query.pageSize = 100;

	do {
		responseData = await googleApiRequest.call(this, method, endpoint, body, query, uri);
		query.pageToken = responseData.nextPageToken;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (responseData.nextPageToken !== undefined && responseData.nextPageToken !== '');

	return returnData;
}

const isValidDate = (str: string) =>
	moment(str, ['YYYY-MM-DD HH:mm:ss Z', moment.ISO_8601], true).isValid();

// Both functions below were taken from Stack Overflow jsonToDocument was fixed as it was unable to handle null values correctly
// https://stackoverflow.com/questions/62246410/how-to-convert-a-firestore-document-to-plain-json-and-vice-versa
// Great thanks to https://stackoverflow.com/users/3915246/mahindar
export function jsonToDocument(value: string | number | IDataObject | IDataObject[]): IDataObject {
	if (value === 'true' || value === 'false' || typeof value === 'boolean') {
		return { booleanValue: value };
	} else if (value === null) {
		return { nullValue: null };
	} else if (value !== '' && !isNaN(value as number)) {
		if (value.toString().indexOf('.') !== -1) {
			return { doubleValue: value };
		} else {
			return { integerValue: value };
		}
	} else if (isValidDate(value as string)) {
		const date = new Date(Date.parse(value as string));
		return { timestampValue: date.toISOString() };
	} else if (typeof value === 'string') {
		return { stringValue: value };
	} else if (value && value.constructor === Array) {
		return { arrayValue: { values: value.map((v) => jsonToDocument(v)) } };
	} else if (typeof value === 'object') {
		const obj: IDataObject = {};
		for (const key of Object.keys(value)) {
			if (value.hasOwnProperty(key) && isSafeObjectProperty(key)) {
				obj[key] = jsonToDocument((value as IDataObject)[key] as IDataObject);
			}
		}
		return { mapValue: { fields: obj } };
	}

	return {};
}

export function documentToJson(fields: IDataObject): IDataObject {
	if (fields === undefined) return {};
	const result = {};
	for (const f of Object.keys(fields)) {
		const key = f,
			value = fields[f],
			isDocumentType = [
				'stringValue',
				'booleanValue',
				'doubleValue',
				'integerValue',
				'timestampValue',
				'mapValue',
				'arrayValue',
				'nullValue',
				'geoPointValue',
			].find((t) => t === key);
		if (isDocumentType) {
			const item = [
				'stringValue',
				'booleanValue',
				'doubleValue',
				'integerValue',
				'timestampValue',
				'nullValue',
				'geoPointValue',
			].find((t) => t === key);
			if (item) {
				return value as IDataObject;
			} else if ('mapValue' === key) {
				//@ts-ignore
				return documentToJson((value!.fields as IDataObject) || {});
			} else if ('arrayValue' === key) {
				// @ts-ignore
				const list = value.values as IDataObject[];
				// @ts-ignore
				return list ? list.map((l) => documentToJson(l)) : [];
			}
		} else {
			// @ts-ignore
			result[key] = documentToJson(value);
		}
	}
	return result;
}

export function fullDocumentToJson(data: IDataObject): IDataObject {
	if (data === undefined) {
		return data;
	}

	return {
		_name: data.name,
		_id: data.id,
		_createTime: data.createTime,
		_updateTime: data.updateTime,
		...documentToJson(data.fields as IDataObject),
	};
}
