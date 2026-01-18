"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/pubsub/pubsub-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/pubsub 的模块。导入/依赖:外部:无；内部:@n8n/constants、@n8n/di；本地:../types。导出:PubSubEventName、PubSubEventFilter、PubSubMetadata。关键函数/方法:register、getHandlers。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/pubsub/pubsub-metadata.ts -> services/n8n/application/n8n-decorators/services/pubsub/pubsub_metadata.py

import type { InstanceRole, InstanceType } from '@n8n/constants';
import { Service } from '@n8n/di';

import type { EventHandler } from '../types';

export type PubSubEventName =
	| 'add-webhooks-triggers-and-pollers'
	| 'remove-triggers-and-pollers'
	| 'clear-test-webhooks'
	| 'display-workflow-activation'
	| 'display-workflow-deactivation'
	| 'display-workflow-activation-error'
	| 'community-package-install'
	| 'community-package-uninstall'
	| 'community-package-update'
	| 'get-worker-status'
	| 'reload-external-secrets-providers'
	| 'reload-license'
	| 'reload-oidc-config'
	| 'reload-saml-config'
	| 'reload-overwrite-credentials'
	| 'response-to-get-worker-status'
	| 'restart-event-bus'
	| 'relay-execution-lifecycle-event'
	| 'reload-sso-provisioning-configuration';

export type PubSubEventFilter =
	| {
			instanceType: 'main';
			instanceRole?: Omit<InstanceRole, 'unset'>;
	  }
	| {
			instanceType: Omit<InstanceType, 'main'>;
			instanceRole?: never;
	  };

type PubSubEventHandler = EventHandler<PubSubEventName> & { filter?: PubSubEventFilter };

@Service()
export class PubSubMetadata {
	private readonly handlers: PubSubEventHandler[] = [];

	register(handler: PubSubEventHandler) {
		this.handlers.push(handler);
	}

	getHandlers(): PubSubEventHandler[] {
		return this.handlers;
	}
}
