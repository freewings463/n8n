"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/get-secrets-proxy.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getSecretsProxy。关键函数/方法:get、set、buildSecretsValueProxy、getSecretsProxy、ownKeys。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/get-secrets-proxy.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/get_secrets_proxy.py

import type { IDataObject, IWorkflowExecuteAdditionalData } from 'n8n-workflow';
import { ExpressionError } from 'n8n-workflow';

function buildSecretsValueProxy(value: IDataObject): unknown {
	return new Proxy(value, {
		get(_target, valueName) {
			if (typeof valueName !== 'string') {
				return;
			}
			if (!(valueName in value)) {
				throw new ExpressionError('Could not load secrets', {
					description:
						'The credential in use tries to use secret from an external store that could not be found',
				});
			}
			const retValue = value[valueName];
			if (typeof retValue === 'object' && retValue !== null) {
				return buildSecretsValueProxy(retValue as IDataObject);
			}
			return retValue;
		},
	});
}

export function getSecretsProxy(additionalData: IWorkflowExecuteAdditionalData): IDataObject {
	const { externalSecretsProxy } = additionalData;
	return new Proxy(
		{},
		{
			get(_target, providerName) {
				if (typeof providerName !== 'string') {
					return {};
				}
				if (externalSecretsProxy.hasProvider(providerName)) {
					return new Proxy(
						{},
						{
							get(_target2, secretName) {
								if (typeof secretName !== 'string') {
									return;
								}
								if (!externalSecretsProxy.hasSecret(providerName, secretName)) {
									throw new ExpressionError('Could not load secrets', {
										description:
											'The credential in use tries to use secret from an external store that could not be found',
									});
								}
								const retValue = externalSecretsProxy.getSecret(providerName, secretName);
								if (typeof retValue === 'object' && retValue !== null) {
									return buildSecretsValueProxy(retValue as IDataObject);
								}
								return retValue;
							},
							set() {
								return false;
							},
							ownKeys() {
								return externalSecretsProxy.listSecrets(providerName);
							},
						},
					);
				}
				throw new ExpressionError('Could not load secrets', {
					description:
						'The credential in use pulls secrets from an external store that is not reachable',
				});
			},
			set() {
				return false;
			},
			ownKeys() {
				return externalSecretsProxy.listProviders();
			},
		},
	);
}
