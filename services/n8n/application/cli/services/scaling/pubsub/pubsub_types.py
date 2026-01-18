"""
MIGRATION-META:
  source_path: packages/cli/src/scaling/pubsub/pubsub.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/scaling/pubsub 的类型。导入/依赖:外部:无；内部:@/utlity.types；本地:./pubsub.event-map、../constants。导出:Channel、HandlerFn、ReloadLicense、ReloadOIDCConfiguration、ReloadSamlConfiguration、ReloadCredentialsOverwrites、RestartEventBus、ReloadExternalSecretsProviders 等15项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/scaling/pubsub/pubsub.types.ts -> services/n8n/application/cli/services/scaling/pubsub/pubsub_types.py

import type { Resolve } from '@/utlity.types';

import type { PubSubCommandMap, PubSubWorkerResponseMap } from './pubsub.event-map';
import type { COMMAND_PUBSUB_CHANNEL, WORKER_RESPONSE_PUBSUB_CHANNEL } from '../constants';

export namespace PubSub {
	// ----------------------------------
	//             channels
	// ----------------------------------

	/** Pubsub channel used by scaling mode. */
	export type Channel = typeof COMMAND_PUBSUB_CHANNEL | typeof WORKER_RESPONSE_PUBSUB_CHANNEL;

	/** Handler function for every message received via a pubsub channel. */
	export type HandlerFn = (msg: string) => void;

	// ----------------------------------
	//            commands
	// ----------------------------------

	type _ToCommand<CommandKey extends keyof PubSubCommandMap> = {
		command: CommandKey;

		/** Host ID of the sender, added during publishing. */
		senderId?: string;

		/** Host IDs of the receivers. */
		targets?: string[];

		/** Whether the command should be sent to the sender as well. */
		selfSend?: boolean;

		/** Whether the command should be debounced when received. */
		debounce?: boolean;
	} & (PubSubCommandMap[CommandKey] extends never
		? { payload?: never } // some commands carry no payload
		: { payload: PubSubCommandMap[CommandKey] });

	type ToCommand<CommandKey extends keyof PubSubCommandMap> = Resolve<_ToCommand<CommandKey>>;

	namespace Commands {
		export type ReloadLicense = ToCommand<'reload-license'>;
		export type ReloadOIDCConfiguration = ToCommand<'reload-oidc-config'>;
		export type ReloadSamlConfiguration = ToCommand<'reload-saml-config'>;
		export type ReloadCredentialsOverwrites = ToCommand<'reload-overwrite-credentials'>;
		export type RestartEventBus = ToCommand<'restart-event-bus'>;
		export type ReloadExternalSecretsProviders = ToCommand<'reload-external-secrets-providers'>;
		export type CommunityPackageInstall = ToCommand<'community-package-install'>;
		export type CommunityPackageUpdate = ToCommand<'community-package-update'>;
		export type CommunityPackageUninstall = ToCommand<'community-package-uninstall'>;
		export type GetWorkerId = ToCommand<'get-worker-id'>;
		export type GetWorkerStatus = ToCommand<'get-worker-status'>;
		export type AddWebhooksTriggersAndPollers = ToCommand<'add-webhooks-triggers-and-pollers'>;
		export type RemoveTriggersAndPollers = ToCommand<'remove-triggers-and-pollers'>;
		export type DisplayWorkflowActivation = ToCommand<'display-workflow-activation'>;
		export type DisplayWorkflowDeactivation = ToCommand<'display-workflow-deactivation'>;
		export type DisplayWorkflowActivationError = ToCommand<'display-workflow-activation-error'>;
		export type RelayExecutionLifecycleEvent = ToCommand<'relay-execution-lifecycle-event'>;
		export type ClearTestWebhooks = ToCommand<'clear-test-webhooks'>;
		export type ReloadSsoProvisioningConfiguration =
			ToCommand<'reload-sso-provisioning-configuration'>;
	}

	/** Command sent via the `n8n.commands` pubsub channel. */
	export type Command =
		| Commands.ReloadLicense
		| Commands.RestartEventBus
		| Commands.ReloadExternalSecretsProviders
		| Commands.CommunityPackageInstall
		| Commands.CommunityPackageUpdate
		| Commands.CommunityPackageUninstall
		| Commands.GetWorkerId
		| Commands.GetWorkerStatus
		| Commands.AddWebhooksTriggersAndPollers
		| Commands.RemoveTriggersAndPollers
		| Commands.DisplayWorkflowActivation
		| Commands.DisplayWorkflowDeactivation
		| Commands.DisplayWorkflowActivationError
		| Commands.RelayExecutionLifecycleEvent
		| Commands.ClearTestWebhooks
		| Commands.ReloadOIDCConfiguration
		| Commands.ReloadSamlConfiguration
		| Commands.ReloadCredentialsOverwrites
		| Commands.ReloadSsoProvisioningConfiguration;

	// ----------------------------------
	//         worker responses
	// ----------------------------------

	type _ToWorkerResponse<WorkerResponseKey extends keyof PubSubWorkerResponseMap> = {
		/** ID of worker sending the response. */
		senderId: string;

		/** IDs of processes to send the response to. */
		targets?: string[];

		/** Content of worker response. */
		response: WorkerResponseKey;

		/** Whether the worker response should be debounced when received. */
		debounce?: boolean;
	} & (PubSubWorkerResponseMap[WorkerResponseKey] extends never
		? { payload?: never } // some responses carry no payload
		: { payload: PubSubWorkerResponseMap[WorkerResponseKey] });

	type ToWorkerResponse<WorkerResponseKey extends keyof PubSubWorkerResponseMap> = Resolve<
		_ToWorkerResponse<WorkerResponseKey>
	>;

	/** Response sent via the `n8n.worker-response` pubsub channel. */
	export type WorkerResponse = ToWorkerResponse<'response-to-get-worker-status'>;
}
