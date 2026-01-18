"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/database/entities/oauth-authorization-code.entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/mcp/database 的OAuth模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/typeorm；本地:./oauth-client.entity。导出:AuthorizationCode。关键函数/方法:无。用于承载OAuth实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/database/entities/oauth-authorization-code.entity.ts -> services/n8n/infrastructure/cli/persistence/models/oauth_authorization_code_entity.py

import { User, WithTimestamps } from '@n8n/db';
import { Column, Entity, Index, ManyToOne } from '@n8n/typeorm';

import { OAuthClient } from './oauth-client.entity';

@Entity('oauth_authorization_codes')
export class AuthorizationCode extends WithTimestamps {
	@Column({ type: 'varchar', primary: true })
	code: string;

	@ManyToOne(
		() => OAuthClient,
		(client) => client.authorizationCodes,
		{ onDelete: 'CASCADE' },
	)
	client: OAuthClient;

	@Index()
	@Column({ type: String })
	clientId: string;

	@ManyToOne(() => User, { onDelete: 'CASCADE' })
	user: User;

	@Index()
	@Column({ type: String })
	userId: string;

	@Column({ type: String })
	redirectUri: string;

	@Column({ type: String })
	codeChallenge: string;

	@Column({ type: String })
	codeChallengeMethod: string;

	@Column({ type: String, nullable: true })
	state: string | null;

	@Index()
	@Column({ type: 'int' })
	expiresAt: number;

	@Column({ type: Boolean, default: false })
	used: boolean;
}
