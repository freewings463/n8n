"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/role.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/constants、@n8n/db、@n8n/permissions、@/services/role.service；本地:无。导出:RoleController。关键函数/方法:getAllRoles、getRoleBySlug、updateRole、deleteRole、createRole。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/role.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/role_controller.py

import { CreateRoleDto, RoleGetQueryDto, RoleListQueryDto, UpdateRoleDto } from '@n8n/api-types';
import { LICENSE_FEATURES } from '@n8n/constants';
import { AuthenticatedRequest } from '@n8n/db';
import {
	Body,
	Delete,
	Get,
	GlobalScope,
	Licensed,
	Param,
	Patch,
	Post,
	Query,
	RestController,
} from '@n8n/decorators';
import { Role as RoleDTO } from '@n8n/permissions';

import { RoleService } from '@/services/role.service';

@RestController('/roles')
export class RoleController {
	constructor(private readonly roleService: RoleService) {}

	@Get('/')
	async getAllRoles(
		_req: AuthenticatedRequest,
		_res: Response,
		@Query query: RoleListQueryDto,
	): Promise<Record<string, RoleDTO[]>> {
		const allRoles = await this.roleService.getAllRoles(query.withUsageCount);
		return {
			global: allRoles.filter((r) => r.roleType === 'global'),
			project: allRoles.filter((r) => r.roleType === 'project'),
			credential: allRoles.filter((r) => r.roleType === 'credential'),
			workflow: allRoles.filter((r) => r.roleType === 'workflow'),
		};
	}

	@Get('/:slug')
	async getRoleBySlug(
		_req: AuthenticatedRequest,
		_res: Response,
		@Param('slug') slug: string,
		@Query query: RoleGetQueryDto,
	): Promise<RoleDTO> {
		return await this.roleService.getRole(slug, query.withUsageCount);
	}

	@Patch('/:slug')
	@GlobalScope('role:manage')
	@Licensed(LICENSE_FEATURES.CUSTOM_ROLES)
	async updateRole(
		_req: AuthenticatedRequest,
		_res: Response,
		@Param('slug') slug: string,
		@Body updateRole: UpdateRoleDto,
	): Promise<RoleDTO> {
		return await this.roleService.updateCustomRole(slug, updateRole);
	}

	@Delete('/:slug')
	@GlobalScope('role:manage')
	@Licensed(LICENSE_FEATURES.CUSTOM_ROLES)
	async deleteRole(
		_req: AuthenticatedRequest,
		_res: Response,
		@Param('slug') slug: string,
	): Promise<RoleDTO> {
		return await this.roleService.removeCustomRole(slug);
	}

	@Post('/')
	@GlobalScope('role:manage')
	@Licensed(LICENSE_FEATURES.CUSTOM_ROLES)
	async createRole(
		_req: AuthenticatedRequest,
		_res: Response,
		@Body createRole: CreateRoleDto,
	): Promise<RoleDTO> {
		return await this.roleService.createCustomRole(createRole);
	}
}
