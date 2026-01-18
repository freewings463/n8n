"""
MIGRATION-META:
  source_path: packages/cli/src/ldap.ee/ldap.controller.ee.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/ldap.ee 的LDAP控制器。导入/依赖:外部:lodash/pick；内部:@n8n/decorators、@/errors/…/bad-request.error、@/events/event.service；本地:./constants、./helpers.ee、./ldap.service.ee、./types。导出:LdapController。关键函数/方法:getConfig、testConnection、updateConfig、getLdapSync、syncLdap。用于处理LDAP接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/ldap.ee/ldap.controller.ee.ts -> services/n8n/presentation/cli/api/v1/controllers/ldap.ee/ldap_controller_ee.py

import { Get, Post, Put, RestController, GlobalScope, Licensed } from '@n8n/decorators';
import pick from 'lodash/pick';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { EventService } from '@/events/event.service';

import { NON_SENSIBLE_LDAP_CONFIG_PROPERTIES } from './constants';
import { getLdapSynchronizations } from './helpers.ee';
import { LdapService } from './ldap.service.ee';
import { LdapConfiguration } from './types';

@RestController('/ldap')
export class LdapController {
	constructor(
		private readonly ldapService: LdapService,
		private readonly eventService: EventService,
	) {}

	@Get('/config')
	@Licensed('feat:ldap')
	@GlobalScope('ldap:manage')
	async getConfig() {
		return await this.ldapService.loadConfig();
	}

	@Post('/test-connection')
	@Licensed('feat:ldap')
	@GlobalScope('ldap:manage')
	async testConnection() {
		try {
			await this.ldapService.testConnection();
		} catch (error) {
			throw new BadRequestError((error as { message: string }).message);
		}
	}

	@Put('/config')
	@Licensed('feat:ldap')
	@GlobalScope('ldap:manage')
	async updateConfig(req: LdapConfiguration.Update) {
		try {
			await this.ldapService.updateConfig(req.body);
		} catch (error) {
			throw new BadRequestError((error as { message: string }).message);
		}

		const data = await this.ldapService.loadConfig();

		this.eventService.emit('ldap-settings-updated', {
			userId: req.user.id,
			...pick(data, NON_SENSIBLE_LDAP_CONFIG_PROPERTIES),
		});

		return data;
	}

	@Get('/sync')
	@Licensed('feat:ldap')
	@GlobalScope('ldap:sync')
	async getLdapSync(req: LdapConfiguration.GetSync) {
		const { page = '0', perPage = '20' } = req.query;
		return await getLdapSynchronizations(parseInt(page, 10), parseInt(perPage, 10));
	}

	@Post('/sync')
	@Licensed('feat:ldap')
	@GlobalScope('ldap:sync')
	async syncLdap(req: LdapConfiguration.Sync) {
		try {
			await this.ldapService.runSync(req.body.type);
		} catch (error) {
			throw new BadRequestError((error as { message: string }).message);
		}
	}
}
