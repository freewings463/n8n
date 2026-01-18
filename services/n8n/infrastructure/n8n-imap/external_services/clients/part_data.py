"""
MIGRATION-META:
  source_path: packages/@n8n/imap/src/part-data.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/imap/src 的模块。导入/依赖:外部:iconv-lite、quoted-printable、utf8、uuencode；内部:无；本地:无。导出:Base64PartData、QuotedPrintablePartData、SevenBitPartData、BinaryPartData、UuencodedPartData。关键函数/方法:toString、fromData。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/imap treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/imap/src/part-data.ts -> services/n8n/infrastructure/n8n-imap/external_services/clients/part_data.py

import * as iconvlite from 'iconv-lite';
import * as qp from 'quoted-printable';
import * as utf8 from 'utf8';
import * as uuencode from 'uuencode';

export abstract class PartData {
	constructor(readonly buffer: Buffer) {}

	toString() {
		return this.buffer.toString();
	}

	static fromData(data: string, encoding: string, charset?: string): PartData {
		if (encoding === 'BASE64') {
			return new Base64PartData(data);
		}

		if (encoding === 'QUOTED-PRINTABLE') {
			return new QuotedPrintablePartData(data, charset);
		}

		if (encoding === '7BIT') {
			return new SevenBitPartData(data);
		}

		if (encoding === '8BIT' || encoding === 'BINARY') {
			return new BinaryPartData(data, charset);
		}

		if (encoding === 'UUENCODE') {
			return new UuencodedPartData(data);
		}

		// if it gets here, the encoding is not currently supported
		throw new Error('Unknown encoding ' + encoding);
	}
}

export class Base64PartData extends PartData {
	constructor(data: string) {
		super(Buffer.from(data, 'base64'));
	}
}

export class QuotedPrintablePartData extends PartData {
	constructor(data: string, charset?: string) {
		const decoded =
			charset?.toUpperCase() === 'UTF-8' ? utf8.decode(qp.decode(data)) : qp.decode(data);
		super(Buffer.from(decoded));
	}
}

export class SevenBitPartData extends PartData {
	constructor(data: string) {
		super(Buffer.from(data));
	}

	toString() {
		return this.buffer.toString('ascii');
	}
}

export class BinaryPartData extends PartData {
	constructor(
		data: string,
		readonly charset: string = 'utf-8',
	) {
		super(Buffer.from(data));
	}

	toString() {
		return iconvlite.decode(this.buffer, this.charset);
	}
}

export class UuencodedPartData extends PartData {
	constructor(data: string) {
		const parts = data.split('\n'); // remove newline characters
		const merged = parts.splice(1, parts.length - 4).join(''); // remove excess lines and join lines with empty string
		const decoded = uuencode.decode(merged);
		super(decoded);
	}
}
