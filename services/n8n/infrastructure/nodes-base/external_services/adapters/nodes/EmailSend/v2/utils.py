"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/EmailSend/v2/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/EmailSend/v2 的节点。导入/依赖:外部:nodemailer、nodemailer/…/smtp-transport；内部:无；本地:无。导出:EmailSendOptions、configureTransport。关键函数/方法:configureTransport、smtpConnectionTest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/EmailSend/v2/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/EmailSend/v2/utils.py

import type {
	IDataObject,
	ICredentialsDecrypted,
	ICredentialTestFunctions,
	INodeCredentialTestResult,
} from 'n8n-workflow';
import { createTransport } from 'nodemailer';
import type SMTPTransport from 'nodemailer/lib/smtp-transport';

export type EmailSendOptions = {
	appendAttribution?: boolean;
	allowUnauthorizedCerts?: boolean;
	attachments?: string;
	ccEmail?: string;
	bccEmail?: string;
	replyTo?: string;
};

export function configureTransport(credentials: IDataObject, options: EmailSendOptions) {
	const connectionOptions: SMTPTransport.Options = {
		host: credentials.host as string,
		port: credentials.port as number,
		secure: credentials.secure as boolean,
	};

	if (credentials.secure === false) {
		connectionOptions.ignoreTLS = credentials.disableStartTls as boolean;
	}

	if (typeof credentials.hostName === 'string' && credentials.hostName) {
		connectionOptions.name = credentials.hostName;
	}

	if (credentials.user || credentials.password) {
		connectionOptions.auth = {
			user: credentials.user as string,
			pass: credentials.password as string,
		};
	}

	if (options.allowUnauthorizedCerts === true) {
		connectionOptions.tls = {
			rejectUnauthorized: false,
		};
	}

	return createTransport(connectionOptions);
}

export async function smtpConnectionTest(
	this: ICredentialTestFunctions,
	credential: ICredentialsDecrypted,
): Promise<INodeCredentialTestResult> {
	const credentials = credential.data!;
	const transporter = configureTransport(credentials, {});
	try {
		await transporter.verify();
		return {
			status: 'OK',
			message: 'Connection successful!',
		};
	} catch (error) {
		return {
			status: 'Error',
			message: error.message,
		};
	} finally {
		transporter.close();
	}
}
