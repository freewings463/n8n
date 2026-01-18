"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/interfaces、../helpers/utils。导出:无。关键函数/方法:splunkApiRequest、rawError、splunkApiJsonRequest。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/transport/__init__.py

import type {
	IExecuteFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	JsonObject,
	IHttpRequestMethods,
	IHttpRequestOptions,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError, sleep } from 'n8n-workflow';

import type { SplunkCredentials, SplunkError } from '../helpers/interfaces';
import { extractErrorDescription, formatEntry, parseXml } from '../helpers/utils';

export async function splunkApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
): Promise<any> {
	const { baseUrl, allowUnauthorizedCerts } =
		await this.getCredentials<SplunkCredentials>('splunkApi');

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		method,
		form: body,
		qs,
		uri: `${baseUrl}${endpoint}`,
		json: true,
		rejectUnauthorized: !allowUnauthorizedCerts,
		useQuerystring: true, // serialize roles array as `roles=A&roles=B`
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	let result;
	try {
		let attempts = 0;

		do {
			try {
				const response = await this.helpers.requestWithAuthentication.call(
					this,
					'splunkApi',
					options,
				);
				result = await parseXml(response);
				return result;
			} catch (error) {
				if (attempts >= 5) {
					throw error;
				}
				await sleep(1000);
				attempts++;
			}
		} while (true);
	} catch (error) {
		if (error instanceof NodeApiError) throw error;

		if (result === undefined) {
			throw new NodeOperationError(this.getNode(), 'No response from API call', {
				description: "Try to use 'Retry On Fail' option from node's settings",
			});
		}
		if (error?.cause?.code === 'ECONNREFUSED') {
			throw new NodeApiError(this.getNode(), { ...(error as JsonObject), code: 401 });
		}

		const rawError = (await parseXml(error.error as string)) as SplunkError;
		error = extractErrorDescription(rawError);

		if ('fatal' in error) {
			error = { error: error.fatal };
		}

		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function splunkApiJsonRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const { baseUrl, allowUnauthorizedCerts } =
		await this.getCredentials<SplunkCredentials>('splunkApi');

	qs.output_mode = 'json';

	const options: IHttpRequestOptions = {
		method,
		body,
		qs: qs ?? {},
		url: `${baseUrl}${endpoint}`,
		json: true,
		skipSslCertificateValidation: allowUnauthorizedCerts,
	};

	if (!Object.keys(body).length) delete options.body;

	let result;
	try {
		let attempts = 0;

		do {
			try {
				result = await this.helpers.httpRequestWithAuthentication.call(this, 'splunkApi', options);

				if (result.entry) {
					const { entry } = result;
					return (entry as IDataObject[]).map((e) => formatEntry(e, true));
				}

				return result;
			} catch (error) {
				if (attempts >= 5) {
					throw error;
				}
				await sleep(1000);
				attempts++;
			}
		} while (true);
	} catch (error) {
		if (error instanceof NodeApiError) throw error;

		if (result === undefined) {
			throw new NodeOperationError(this.getNode(), 'No response from API call', {
				description: "Try to use 'Retry On Fail' option from node's settings",
			});
		}
		if (error?.cause?.code === 'ECONNREFUSED') {
			throw new NodeApiError(this.getNode(), { ...(error as JsonObject), code: 401 });
		}

		if ('fatal' in error) error = { error: error.fatal };

		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
