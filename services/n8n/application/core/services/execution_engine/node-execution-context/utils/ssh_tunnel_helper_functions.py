"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/ssh-tunnel-helper-functions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:ssh2；内部:@n8n/di、n8n-workflow；本地:../../ssh-clients-manager。导出:getSSHTunnelFunctions。关键函数/方法:getSSHTunnelFunctions。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/ssh-tunnel-helper-functions.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/ssh_tunnel_helper_functions.py

import { Container } from '@n8n/di';
import type { SSHTunnelFunctions } from 'n8n-workflow';
import type { Client } from 'ssh2';

import { SSHClientsManager } from '../../ssh-clients-manager';

export const getSSHTunnelFunctions = (): SSHTunnelFunctions => {
	const sshClientsManager = Container.get(SSHClientsManager);
	return {
		getSSHClient: async (credentials, abortController) =>
			await sshClientsManager.getClient(credentials, abortController),
		updateLastUsed: (client: Client) => sshClientsManager.updateLastUsed(client),
	};
};
