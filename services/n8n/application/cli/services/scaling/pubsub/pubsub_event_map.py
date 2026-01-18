"""
MIGRATION-META:
  source_path: packages/cli/src/scaling/pubsub/pubsub.event-map.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/scaling/pubsub 的模块。导入/依赖:外部:无；内部:@n8n/api-types、n8n-workflow；本地:无。导出:PubSubCommandMap、PubSubWorkerResponseMap、PubSubEventMap。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/scaling/pubsub/pubsub.event-map.ts -> services/n8n/application/cli/services/scaling/pubsub/pubsub_event_map.py

import type { PushMessage, WorkerStatus } from '@n8n/api-types';
import type { IWorkflowBase } from 'n8n-workflow';

export type PubSubCommandMap = {
	// #region Lifecycle

	'reload-license': never;

	'restart-event-bus': never;

	'reload-external-secrets-providers': never;

	// #endregion

	// # region Credentials
	'reload-overwrite-credentials': never;
	// #endregion

	// # region SSO

	'reload-oidc-config': never;
	'reload-saml-config': never;

	// # sso provisioning
	'reload-sso-provisioning-configuration': never;

	// #endregion

	// #region Community packages

	'community-package-install': {
		packageName: string;
		packageVersion: string;
	};

	'community-package-update': {
		packageName: string;
		packageVersion: string;
	};

	'community-package-uninstall': {
		packageName: string;
	};

	// #endregion

	// #region Worker view

	'get-worker-id': never;

	'get-worker-status': never;

	// #endregion

	// #region Multi-main setup

	'add-webhooks-triggers-and-pollers': {
		workflowId: string;
		activeVersionId: string;
	};

	'remove-triggers-and-pollers': {
		workflowId: string;
	};

	'display-workflow-activation': {
		workflowId: string;
		activeVersionId: string;
	};

	'display-workflow-deactivation': {
		workflowId: string;
	};

	'display-workflow-activation-error': {
		workflowId: string;
		errorMessage: string;
	};

	'relay-execution-lifecycle-event': PushMessage & {
		pushRef: string;
		asBinary: boolean;
	};

	'clear-test-webhooks': {
		webhookKey: string;
		workflowEntity: IWorkflowBase;
		pushRef: string;
	};

	// #endregion
};

export type PubSubWorkerResponseMap = {
	'response-to-get-worker-status': WorkerStatus;
};

export type PubSubEventMap = PubSubCommandMap & PubSubWorkerResponseMap;
