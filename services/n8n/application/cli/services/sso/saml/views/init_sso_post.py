"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/saml/views/init-sso-post.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/sso.ee/saml/views 的SSO页面。导入/依赖:外部:samlify/…/entity；内部:无；本地:无。导出:getInitSSOFormView。关键函数/方法:getInitSSOFormView。用于组装SSO页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - SSO integration orchestration -> application/services/sso
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/saml/views/init-sso-post.ts -> services/n8n/application/cli/services/sso/saml/views/init_sso_post.py

import type { PostBindingContext } from 'samlify/types/src/entity';

export function getInitSSOFormView(context: PostBindingContext): string {
	return `
	<form id="saml-form" method="post" action="${context.entityEndpoint}" autocomplete="off">
    <input type="hidden" name="${context.type}" value="${context.context}" />
    ${context.relayState ? '<input type="hidden" name="RelayState" value="{{relayState}}" />' : ''}
</form>
<script type="text/javascript">
    // Automatic form submission
    (function(){
        document.forms[0].submit();
    })();
</script>`;
}
