"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/breaking-changes.rule-registry.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes 的服务。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/di；本地:./types。导出:RuleRegistry。关键函数/方法:register、registerAll、getRule、getRules。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/breaking-changes.rule-registry.service.ts -> services/n8n/application/cli/services/breaking-changes/breaking_changes_rule_registry_service.py

import { Logger } from '@n8n/backend-common';
import { Service } from '@n8n/di';

import type { IBreakingChangeRule } from './types';

@Service()
export class RuleRegistry {
	private readonly rules = new Map<string, IBreakingChangeRule>();

	constructor(private readonly logger: Logger) {
		this.logger = logger.scoped('breaking-changes');
	}

	register(rule: IBreakingChangeRule): void {
		if (this.rules.has(rule.id)) {
			this.logger.warn(`Rule with ID ${rule.id} is already registered. Overwriting.`);
		}
		this.rules.set(rule.id, rule);
		this.logger.debug(`Registered rule: ${rule.id}`);
	}

	registerAll(rules: IBreakingChangeRule[]): void {
		rules.forEach((rule) => this.register(rule));
	}

	getRule(id: string): IBreakingChangeRule | undefined {
		return this.rules.get(id);
	}

	getRules(version?: string): IBreakingChangeRule[] {
		const rules = Array.from(this.rules.values());
		if (!version) {
			return rules;
		}
		return rules.filter((rule) => rule.getMetadata().version === version);
	}
}
