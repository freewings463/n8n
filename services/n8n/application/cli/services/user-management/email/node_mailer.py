"""
MIGRATION-META:
  source_path: packages/cli/src/user-management/email/node-mailer.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/user-management/email 的模块。导入/依赖:外部:lodash/pick、nodemailer、nodemailer/…/smtp-connection；内部:@n8n/backend-common、@n8n/config、@n8n/di、n8n-core；本地:./interfaces。导出:NodeMailer。关键函数/方法:sendMail。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/user-management/email/node-mailer.ts -> services/n8n/application/cli/services/user-management/email/node_mailer.py

import { Logger } from '@n8n/backend-common';
import { GlobalConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import pick from 'lodash/pick';
import { ErrorReporter } from 'n8n-core';
import path from 'node:path';
import type { Transporter } from 'nodemailer';
import { createTransport } from 'nodemailer';
import type SMTPConnection from 'nodemailer/lib/smtp-connection';

import type { MailData, SendEmailResult } from './interfaces';

@Service()
export class NodeMailer {
	readonly sender: string;

	private transport: Transporter;

	constructor(
		globalConfig: GlobalConfig,
		private readonly logger: Logger,
		private readonly errorReporter: ErrorReporter,
	) {
		const smtpConfig = globalConfig.userManagement.emails.smtp;
		const transportConfig: SMTPConnection.Options = pick(smtpConfig, ['host', 'port', 'secure']);
		transportConfig.ignoreTLS = !smtpConfig.startTLS;

		const { auth } = smtpConfig;
		if (auth.user && auth.pass) {
			transportConfig.auth = pick(auth, ['user', 'pass']);
		}
		if (auth.serviceClient && auth.privateKey) {
			transportConfig.auth = {
				type: 'OAuth2',
				user: auth.user,
				serviceClient: auth.serviceClient,
				privateKey: auth.privateKey.replace(/\\n/g, '\n'),
			};
		}
		this.transport = createTransport(transportConfig);

		this.sender = smtpConfig.sender;
		if (!this.sender && auth.user.includes('@')) {
			this.sender = auth.user;
		}
	}

	async sendMail(mailData: MailData): Promise<SendEmailResult> {
		try {
			await this.transport.sendMail({
				from: this.sender,
				to: mailData.emailRecipients,
				subject: mailData.subject,
				text: mailData.textOnly,
				html: mailData.body,
				attachments: [
					{
						cid: 'n8n-logo',
						filename: 'n8n-logo.png',
						path: path.resolve(__dirname, 'templates/n8n-logo.png'),
						contentDisposition: 'inline',
					},
				],
			});
			this.logger.debug(
				`Email sent successfully to the following recipients: ${mailData.emailRecipients.toString()}`,
			);
		} catch (error) {
			this.errorReporter.error(error);
			this.logger.error('Failed to send email', {
				recipients: mailData.emailRecipients,
				error: error as Error,
			});
			throw error;
		}

		return { emailSent: true };
	}
}
