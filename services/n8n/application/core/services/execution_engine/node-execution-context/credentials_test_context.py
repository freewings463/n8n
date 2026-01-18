"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/credentials-test-context.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context 的执行模块。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/decorators、@n8n/di、n8n-workflow；本地:./utils/request-helper-functions、./utils/ssh-tunnel-helper-functions。导出:CredentialTestContext。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/credentials-test-context.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/credentials_test_context.py

import { Logger } from '@n8n/backend-common';
import { Memoized } from '@n8n/decorators';
import { Container } from '@n8n/di';
import type { ICredentialTestFunctions } from 'n8n-workflow';

import { proxyRequestToAxios } from './utils/request-helper-functions';
import { getSSHTunnelFunctions } from './utils/ssh-tunnel-helper-functions';

export class CredentialTestContext implements ICredentialTestFunctions {
	readonly helpers: ICredentialTestFunctions['helpers'];

	constructor() {
		this.helpers = {
			...getSSHTunnelFunctions(),
			request: async (uriOrObject: string | object, options?: object) => {
				// eslint-disable-next-line @typescript-eslint/no-unsafe-return
				return await proxyRequestToAxios(undefined, undefined, undefined, uriOrObject, options);
			},
		};
	}

	@Memoized
	get logger() {
		return Container.get(Logger);
	}
}
