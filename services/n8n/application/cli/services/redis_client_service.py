"""
MIGRATION-META:
  source_path: packages/cli/src/services/redis-client.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的服务。导入/依赖:外部:ioredis；内部:@n8n/backend-common、@n8n/config、@n8n/decorators、@n8n/di、@/typed-emitter；本地:../redis/redis.types。导出:RedisClientService。关键函数/方法:isConnected、createClient、toValidPrefix、createRegularClient、createClusterClient、getOptions、getClusterOptions、retryStrategy、clusterNodes、registerListeners 等1项。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/redis-client.service.ts -> services/n8n/application/cli/services/redis_client_service.py

import { Logger } from '@n8n/backend-common';
import { GlobalConfig } from '@n8n/config';
import { Debounce } from '@n8n/decorators';
import { Service } from '@n8n/di';
import ioRedis from 'ioredis';
import type { Cluster, ClusterOptions, RedisOptions } from 'ioredis';

import { TypedEmitter } from '@/typed-emitter';

import type { RedisClientType } from '../scaling/redis/redis.types';

type RedisEventMap = {
	'connection-lost': number;
	'connection-recovered': never;
};

@Service()
export class RedisClientService extends TypedEmitter<RedisEventMap> {
	private readonly clients = new Set<ioRedis | Cluster>();

	private readonly config = {
		/** How long (in ms) to try to reconnect for before exiting. */
		maxTimeout: this.globalConfig.queue.bull.redis.timeoutThreshold,

		/** How long (in ms) to wait between reconnection attempts. */
		retryInterval: 1000,

		/** How long (in ms) to wait before resetting the cumulative timeout. */
		resetLength: 30_000,
	};

	/** Whether any client has lost connection to Redis. */
	private lostConnection = false;

	constructor(
		private readonly logger: Logger,
		private readonly globalConfig: GlobalConfig,
	) {
		super();

		this.logger = this.logger.scoped(['redis', 'scaling']);

		this.registerListeners();
	}

	isConnected() {
		return !this.lostConnection;
	}

	createClient(arg: { type: RedisClientType; extraOptions?: RedisOptions }) {
		const client =
			this.clusterNodes().length > 0
				? this.createClusterClient(arg)
				: this.createRegularClient(arg);

		client.on('error', (error: Error) => {
			if ('code' in error && error.code === 'ECONNREFUSED') return; // handled by retryStrategy

			this.logger.error(`[Redis client] ${error.message}`, { error });
		});

		client.on('ready', () => {
			if (this.lostConnection) {
				this.emit('connection-recovered');
				this.lostConnection = false;
			}
		});

		this.clients.add(client);

		return client;
	}

	/**
	 * Ensure prefix is wrapped in curly braces for Redis cluster.
	 * See: https://github.com/OptimalBits/bull/blob/develop/PATTERNS.md
	 */
	toValidPrefix(prefix: string) {
		if (this.clusterNodes().length > 0) {
			if (!prefix.startsWith('{')) prefix = '{' + prefix;
			if (!prefix.endsWith('}')) prefix += '}';
		}

		return prefix;
	}

	// ----------------------------------
	//            private
	// ----------------------------------

	private createRegularClient({
		type,
		extraOptions,
	}: {
		type: RedisClientType;
		extraOptions?: RedisOptions;
	}) {
		const options = this.getOptions({ extraOptions });

		const { host, port } = this.globalConfig.queue.bull.redis;

		options.host = host;
		options.port = port;

		const client = new ioRedis(options);

		this.logger.debug(`Started Redis client ${type}`, { type, host, port });

		return client;
	}

	private createClusterClient({
		type,
		extraOptions,
	}: {
		type: string;
		extraOptions?: RedisOptions;
	}) {
		const options = this.getOptions({ extraOptions });

		const clusterNodes = this.clusterNodes();

		const clusterOptions = this.getClusterOptions(options, this.retryStrategy());

		const clusterClient = new ioRedis.Cluster(clusterNodes, clusterOptions);

		this.logger.debug(`Started Redis cluster client ${type}`, { type, clusterNodes });

		return clusterClient;
	}

	private getOptions({ extraOptions }: { extraOptions?: RedisOptions }) {
		const { username, password, db, tls, dualStack } = this.globalConfig.queue.bull.redis;

		/**
		 * Disabling ready check allows quick reconnection to Redis if Redis becomes
		 * temporarily unreachable. With ready check enabled, the client might take
		 * minutes to realize Redis is back up and resume working.
		 *
		 * See:
		 * - https://github.com/OptimalBits/bull/issues/890
		 * - https://github.com/OptimalBits/bull/issues/1873
		 * - https://github.com/OptimalBits/bull/pull/2185
		 */
		const options: RedisOptions = {
			username,
			password,
			db,
			enableReadyCheck: false,
			maxRetriesPerRequest: null,
			retryStrategy: this.retryStrategy(),
			...extraOptions,
		};

		if (dualStack) options.family = 0;

		if (tls) options.tls = {}; // enable TLS with default Node.js settings

		return options;
	}

	private getClusterOptions(
		options: RedisOptions,
		retryStrategy: () => number | null,
	): ClusterOptions {
		const { slotsRefreshTimeout, slotsRefreshInterval, dnsResolveStrategy } =
			this.globalConfig.queue.bull.redis;
		const clusterOptions: ClusterOptions = {
			redisOptions: options,
			clusterRetryStrategy: retryStrategy,
			slotsRefreshTimeout,
			slotsRefreshInterval,
		};

		// NOTE: this is necessary to use AWS Elasticache Clusters with TLS.
		// See https://github.com/redis/ioredis?tab=readme-ov-file#special-note-aws-elasticache-clusters-with-tls.
		if (dnsResolveStrategy === 'NONE') {
			clusterOptions.dnsLookup = (address, lookupFn) => lookupFn(null, address);
		}

		return clusterOptions;
	}

	/**
	 * Strategy to retry connecting to Redis on connection failure.
	 *
	 * Try to reconnect every 500ms. On every failed attempt, increment a timeout
	 * counter - if the cumulative timeout exceeds a limit, exit the process.
	 * Reset the cumulative timeout if >30s between reconnection attempts.
	 */
	private retryStrategy() {
		let lastAttemptTs = 0;
		let cumulativeTimeout = 0;

		return () => {
			const nowTs = Date.now();

			if (nowTs - lastAttemptTs > this.config.resetLength) {
				cumulativeTimeout = 0;
				lastAttemptTs = nowTs;
			} else {
				cumulativeTimeout += nowTs - lastAttemptTs;
				lastAttemptTs = nowTs;
				if (cumulativeTimeout > this.config.maxTimeout) {
					const maxTimeout = Math.round(this.config.maxTimeout / 1000) + 's';
					this.logger.error(`Unable to connect to Redis after trying to connect for ${maxTimeout}`);
					this.logger.error('Exiting process due to Redis connection error');
					process.exit(1);
				}
			}

			this.emit('connection-lost', cumulativeTimeout);

			return this.config.retryInterval;
		};
	}

	private clusterNodes() {
		return this.globalConfig.queue.bull.redis.clusterNodes
			.split(',')
			.filter((pair) => pair.trim().length > 0)
			.map((pair) => {
				const [host, port] = pair.split(':');
				return { host, port: parseInt(port) };
			});
	}

	@Debounce(1000)
	emit<Event extends keyof RedisEventMap>(
		event: Event,
		...args: Array<RedisEventMap[Event]>
	): boolean {
		return super.emit(event, ...args);
	}

	private registerListeners() {
		const { maxTimeout: maxTimeoutMs, retryInterval: retryIntervalMs } = this.config;

		const retryInterval = this.formatTimeout(retryIntervalMs);
		const maxTimeout = this.formatTimeout(maxTimeoutMs);

		this.on('connection-lost', (cumulativeTimeoutMs) => {
			const cumulativeTimeout = this.formatTimeout(cumulativeTimeoutMs);
			const reconnectionMsg = `Trying to reconnect in ${retryInterval}...`;
			const timeoutDetails = `${cumulativeTimeout}/${maxTimeout}`;

			this.logger.warn(`Lost Redis connection. ${reconnectionMsg} (${timeoutDetails})`);

			this.lostConnection = true;
		});

		this.on('connection-recovered', () => {
			this.logger.info('Recovered Redis connection');
		});
	}

	private formatTimeout(timeoutMs: number) {
		const timeoutSeconds = timeoutMs / 1000;
		const roundedTimeout = Math.round(timeoutSeconds * 10) / 10;

		return roundedTimeout + 's';
	}
}
