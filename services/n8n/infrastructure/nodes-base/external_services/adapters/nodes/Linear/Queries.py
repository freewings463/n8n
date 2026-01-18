"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Linear/Queries.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Linear 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:query。关键函数/方法:getUsers、users、getTeams、teams、getStates、workflowStates、createIssue、issueCreate、deleteIssue、issueDelete 等11项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Linear/Queries.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Linear/Queries.py

export const query = {
	getUsers() {
		return `query Users ($first: Int, $after: String){
			users (first: $first, after: $after){
				nodes {
					id
					name
				},
				pageInfo {
					hasNextPage
					endCursor
			}
		}}`;
	},
	getTeams() {
		return `query Teams ($first: Int, $after: String){
				teams (first: $first, after: $after){
					nodes {
						id
						name
					}
					pageInfo {
						hasNextPage
						endCursor
					}
			}}`;
	},
	getStates() {
		return `query States ($first: Int, $after: String, $filter: WorkflowStateFilter){
				workflowStates (first: $first, after: $after, filter: $filter){
					nodes {
						id
						name
					},
					pageInfo {
						hasNextPage
						endCursor
				}
			}}`;
	},
	createIssue() {
		return `mutation IssueCreate (
			$title: String!,
			$teamId: String!,
			$description: String,
			$assigneeId: String,
			$priorityId: Int,
			$stateId: String){
			issueCreate(
				input: {
					title: $title
					description: $description
					teamId: $teamId
					assigneeId: $assigneeId
					priority: $priorityId
					stateId: $stateId
				}
			) {
				success
					issue {
						id,
						identifier,
						title,
						priority
						archivedAt
						assignee {
							id
							displayName
						}
						state {
							id
							name
						}
						createdAt
						creator {
							id
							displayName
						}
						description
						dueDate
						cycle {
							id
							name
						}
					}
				}
			}`;
	},
	deleteIssue() {
		return `mutation IssueDelete ($issueId: String!) {
					issueDelete(id: $issueId) {
						success
					}
				}`;
	},
	getIssue() {
		return `query Issue($issueId: String!) {
			issue(id: $issueId) {
				id,
				identifier,
				title,
				priority,
				archivedAt,
				assignee {
					id,
					displayName
				}
				state {
					id
					name
				}
				createdAt
				creator {
					id
					displayName
				}
				description
				dueDate
				cycle {
					id
					name
				}
			}
		}`;
	},
	getIssueTeam() {
		return `query Issue($issueId: String!) {
			issue(id: $issueId) {
				team {
					id
				}
			}
		}`;
	},
	getIssues() {
		return `query Issue ($first: Int, $after: String){
					issues (first: $first, after: $after){
						nodes {
						id,
						identifier,
						title,
						priority
						archivedAt
						assignee {
							id
							displayName
						}
						state {
							id
							name
						}
						createdAt
						creator {
							id
							displayName
						}
						description
						dueDate
						cycle {
							id
							name
						}
					}
					pageInfo {
						hasNextPage
						endCursor
					}
				}
			}`;
	},
	updateIssue() {
		return `mutation IssueUpdate (
		$issueId: String!,
		$title: String,
		$teamId: String,
		$description: String,
		$assigneeId: String,
		$priorityId: Int,
		$stateId: String){
		issueUpdate(
			id: $issueId,
			input: {
				title: $title
				description: $description
				teamId: $teamId
				assigneeId: $assigneeId
				priority: $priorityId
				stateId: $stateId
			}
		) {
			success
				issue {
					id,
					identifier,
					title,
					priority
					archivedAt
					assignee {
						id
						displayName
					}
					state {
						id
						name
					}
					createdAt
					creator {
						id
						displayName
					}
					description
					dueDate
					cycle {
						id
						name
					}
				}
			}
		}`;
	},
	addComment() {
		return `mutation CommentCreate ($issueId: String!, $body: String!, $parentId: String) {
			commentCreate(input: {issueId: $issueId, body: $body, parentId: $parentId}) {
				success
				comment {
					id
				}
			}
		}`;
	},
	addIssueLink() {
		return `mutation AttachmentLinkURL($url: String!, $issueId: String!) {
  		attachmentLinkURL(url: $url, issueId: $issueId) {
    		success
  		}
		}`;
	},
};
