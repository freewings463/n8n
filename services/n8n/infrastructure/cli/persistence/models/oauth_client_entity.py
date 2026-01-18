"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/database/entities/oauth-client.entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/mcp/database 的OAuth模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/typeorm；本地:./oauth-access-token.entity、./oauth-authorization-code.entity、./oauth-refresh-token.entity、./oauth-user-consent.entity。导出:OAuthClient。关键函数/方法:无。用于承载OAuth实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/database/entities/oauth-client.entity.ts -> services/n8n/infrastructure/cli/persistence/models/oauth_client_entity.py

import { JsonColumn, WithTimestamps } from '@n8n/db';
import { Column, Entity, OneToMany } from '@n8n/typeorm';

import type { AccessToken } from './oauth-access-token.entity';
import type { AuthorizationCode } from './oauth-authorization-code.entity';
import type { RefreshToken } from './oauth-refresh-token.entity';
import type { UserConsent } from './oauth-user-consent.entity';

@Entity('oauth_clients')
export class OAuthClient extends WithTimestamps {
	@Column({ type: 'varchar', primary: true })
	id: string;

	@Column({ type: String })
	name: string;

	@JsonColumn()
	redirectUris: string[];

	@JsonColumn()
	grantTypes: string[];

	@Column({ type: String, default: 'none' })
	tokenEndpointAuthMethod: string;

	@OneToMany('AuthorizationCode', 'client')
	authorizationCodes: AuthorizationCode[];

	@OneToMany('AccessToken', 'client')
	accessTokens: AccessToken[];

	@OneToMany('RefreshToken', 'client')
	refreshTokens: RefreshToken[];

	@OneToMany('UserConsent', 'client')
	userConsents: UserConsent[];

	@Column({ type: String, nullable: true })
	clientSecret: string | null;

	@Column({ type: 'int', nullable: true })
	clientSecretExpiresAt: number | null;
}
