# Security / セキュリティに関する注意

## English

This repository contains a fork of 25-year-old (2000) legacy Perl CGI
software. Please read this before deploying anything from this repository.

- **This is unmaintained legacy software.** It was written before modern
  web-security practices existed, for a single-server hobbyist environment.
  It was never designed to withstand today's threat landscape.
- **The fixes in `cgi-bin/` are targeted fixes, not a full security audit.**
  During this fork's development, three vulnerability classes and one
  systematic data-corruption bug were found and fixed (see
  [doc/changelog.md](./doc/changelog.md) for exact details). This does not
  mean the code is now free of vulnerabilities — only that these specific,
  discovered issues were addressed. No formal, exhaustive security audit has
  been performed.
- **`archive/` contains the original, unmodified code, which still has the
  unpatched vulnerabilities described in doc/changelog.md.** Those files are
  included strictly for historical and provenance reasons. Do **not** deploy
  the contents of `archive/` on a live, internet-facing server. Because
  doc/changelog.md documents the exact nature of these issues, treat any
  unpatched deployment of the original code as a known, publicly-documented
  target.
- **No warranty.** As stated in [LICENSE](./LICENSE), this software is
  provided "AS IS", without warranty of any kind. Anyone deploying code from
  this repository — including the fixed `cgi-bin/` edition — does so
  entirely at their own risk and is responsible for their own independent
  review before any public deployment.
- If you find an additional vulnerability, please open an issue rather than
  exploiting it or publishing exploit details without coordination.

## 日本語

本リポジトリには、25年前（2000年）のPerl製レガシーCGIソフトウェアの改造版が
含まれています。本リポジトリの内容を配置・運用する前に、必ずお読みください。

- **これは保守されていないレガシーソフトウェアです。** 現代的なWebセキュリティの
  考え方が確立する以前に、個人運営の単一サーバー環境向けに書かれたものであり、
  今日の脅威環境に耐えるようには設計されていません。
- **`cgi-bin/`の修正は、発見した問題に対する個別対応であり、網羅的なセキュリティ
  監査ではありません。** 本フォークの開発過程で、3種類の脆弱性と1件の系統的な
  データ破損バグを発見・修正しました（詳細は[doc/changelog.md](./doc/changelog.md)
  参照）。これは「今後一切の脆弱性がない」ことを意味するものではなく、あくまで
  発見済みの個別の問題に対応したという意味に留まります。正式かつ網羅的な
  セキュリティ監査は行っていません。
- **`archive/`には原本（無改変）が含まれており、doc/changelog.mdに記載した
  未修正の脆弱性がそのまま存在します。** これらのファイルは、由来の証明・
  歴史的資料としてのみ同梱しています。`archive/`の中身をインターネットに
  公開されたサーバーへそのまま配置しないでください。doc/changelog.mdに具体的な
  問題の内容を記載しているため、原本を無修正のまま運用することは、内容が
  公知となっている攻撃対象を晒すことと同義になります。
- **無保証です。** [LICENSE](./LICENSE)に記載の通り、本ソフトウェアは
  「現状のまま(AS IS)」提供され、いかなる保証もありません。`cgi-bin/`の
  修正版を含め、本リポジトリのコードを配置・運用する場合は、完全に自己責任で
  行っていただくものとし、公開前の独自レビューは利用者ご自身の責任で
  行ってください。
- 追加の脆弱性を発見された場合は、悪用や無調整での詳細公開ではなく、
  Issueを立てる形でのご連絡をお願いします。
