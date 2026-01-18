"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/shared/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:parseLinkHeader。关键函数/方法:parseLinkHeader。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/shared/utils.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/shared/utils.py

export function parseLinkHeader(header?: string): { [rel: string]: string } {
	const links: { [rel: string]: string } = {};

	for (const part of header?.split(',') ?? []) {
		const section = part.trim();
		const match = section.match(/^<([^>]+)>\s*;\s*rel="?([^"]+)"?/);
		if (match) {
			const [, url, rel] = match;
			links[rel] = url;
		}
	}

	return links;
}
