"""
MIGRATION-META:
  source_path: packages/testing/containers/services/registry.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers/services 的服务。导入/依赖:外部:无；内部:无；本地:./gitea、./keycloak、./load-balancer、./mailpit 等10项。导出:services、helperFactories。关键函数/方法:无。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/services/registry.ts -> services/n8n/tests/testing/fixtures/containers/services/registry.py

import { gitea, createGiteaHelper } from './gitea';
import { keycloak, createKeycloakHelper } from './keycloak';
import { loadBalancer } from './load-balancer';
import { mailpit, createMailpitHelper } from './mailpit';
import { createObservabilityHelper } from './observability';
import { postgres } from './postgres';
import { proxy } from './proxy';
import { redis } from './redis';
import { taskRunner } from './task-runner';
import { tracing, createTracingHelper } from './tracing';
import type { Service, ServiceName, ServiceResult, HelperFactories } from './types';
import { vector } from './vector';
import { victoriaLogs } from './victoria-logs';
import { victoriaMetrics } from './victoria-metrics';

/** Service registry - must include all ServiceName entries */
export const services: Record<ServiceName, Service<ServiceResult>> = {
	postgres,
	redis,
	mailpit,
	gitea,
	keycloak,
	victoriaLogs,
	victoriaMetrics,
	vector,
	tracing,
	proxy,
	taskRunner,
	loadBalancer,
};

export const helperFactories: Partial<HelperFactories> = {
	mailpit: createMailpitHelper,
	gitea: createGiteaHelper,
	keycloak: createKeycloakHelper,
	observability: createObservabilityHelper,
	tracing: createTracingHelper,
};
