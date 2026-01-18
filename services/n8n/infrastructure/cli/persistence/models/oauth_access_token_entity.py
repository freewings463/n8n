"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/database/entities/oauth-access-token.entity.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/mcp/database 的OAuth模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/typeorm；本地:./oauth-client.entity。导出:AccessToken。关键函数/方法:无。用于承载OAuth实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/database/entities/oauth-access-token.entity.ts -> services/n8n/infrastructure/cli/persistence/models/oauth_access_token_entity.py

import { User } from '@n8n/db';
import { Column, Entity, Index, ManyToOne } from '@n8n/typeorm';

import { OAuthClient } from './oauth-client.entity';

@Entity('oauth_access_tokens')
export class AccessToken {
	@Column({ type: 'varchar', primary: true })
	token: string;

	@ManyToOne(
		() => OAuthClient,
		(client) => client.accessTokens,
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
}
