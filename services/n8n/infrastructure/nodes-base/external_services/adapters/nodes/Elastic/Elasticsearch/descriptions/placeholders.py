"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Elastic/Elasticsearch/descriptions/placeholders.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Elastic/Elasticsearch 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:indexSettings、mappings、aliases、query、document。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Elastic/Elasticsearch/descriptions/placeholders.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Elastic/Elasticsearch/descriptions/placeholders.py

export const indexSettings = `{
  "settings": {
    "index": {
      "number_of_shards": 3,
      "number_of_replicas": 2
    }
  }
}`;

export const mappings = `{
  "mappings": {
    "properties": {
      "field1": { "type": "text" }
    }
  }
}`;

export const aliases = `{
  "aliases": {
    "alias_1": {},
    "alias_2": {
      "filter": {
        "term": { "user.id": "kimchy" }
      },
      "routing": "shard-1"
    }
  }
}`;

export const query = `{
  "query": {
    "term": {
      "user.id": "john"
    }
  }
}`;

export const document = `{
  "timestamp": "2099-05-06T16:21:15.000Z",
  "event": {
    "original": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736"
  }
}`;
