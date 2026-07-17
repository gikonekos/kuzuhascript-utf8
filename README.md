# kuzuhascript-utf8

## English

A UTF-8 / modern-Perl fork of *kuzuhascript (くずはすくりぷと) Rev.0.1 Preview 9*
(2000, by kuzuha), with security fixes, so it can run as a working sample.

- `cgi-bin/kscrr1p9/` — plain edition
- `cgi-bin/kscrr1p9up/` — edition with uploader plugin
- `archive/` — original archives (unmodified) and reference material

Copyright and license: see [LICENSE](./LICENSE) and [NOTICE.md](./NOTICE.md).
Change history: see [doc/changelog.md](./doc/changelog.md).
Setup guide: see [doc/install.md](./doc/install.md).
**Before deploying anything from this repository, please read
[SECURITY.md](./SECURITY.md).**

### Requirements

- Perl 5.38+ (tested on 5.38.2). Likely fine on most Perl 5.x, but untested
  below 5.38.
- No external CPAN modules required — the jcode.pl dependency has been
  removed.

### Known limitations

- Runtime character-code normalization of submitted form data (formerly
  handled by jcode.pl) is currently a no-op; see doc/changelog.md.
- The uploader plugin (`bbsup.pl`, kscrr1p9up only) has not yet been tested
  end-to-end.

## 日本語

2000年にkuzuha(くずは)氏が公開した「くずはすくりぷと Rev.0.1 Preview 9」を、
UTF-8対応・脆弱性対策を施し、最新Perlで動作する実働見本として改造した派生版です。

- `cgi-bin/kscrr1p9/` - 無印版
- `cgi-bin/kscrr1p9up/` - アップローダーPlugin付き版
- `archive/` - 原本アーカイブ（無改変）と参考資料

著作権・ライセンスは [LICENSE](./LICENSE) と [NOTICE.md](./NOTICE.md) を、
変更履歴は [doc/changelog.md](./doc/changelog.md) を、
設置の手引きは [doc/install.md](./doc/install.md) を参照してください。
**本リポジトリの内容を配置・運用する前に、必ず[SECURITY.md](./SECURITY.md)
をお読みください。**

### 動作要件

- Perl 5.38以降（5.38.2で動作確認済み）。それ以下のバージョンでの動作は
  未検証です。
- 外部CPANモジュール不要（jcode.pl依存は削除済み）。

### 既知の制限事項

- 投稿データの実行時文字コード正規化（旧jcode.pl相当）は現状no-opです。
  詳細はdoc/changelog.mdを参照してください。
- アップローダーPlugin（bbsup.pl、kscrr1p9up限定）は実機での網羅的テスト
  未実施です。

## Folder Structure / フォルダ構造

<pre>
├── <a href="./README.md">README.md</a>
├── <a href="./LICENSE">LICENSE</a>
├── <a href="./NOTICE.md">NOTICE.md</a>
├── <a href="./SECURITY.md">SECURITY.md</a>
├── doc/
│   ├── <a href="./doc/changelog.md">changelog.md</a>
│   └── <a href="./doc/install.md">install.md</a>
├── cgi-bin/
│   ├── kscrr1p9/
│   │   ├── <a href="./cgi-bin/kscrr1p9/bbs.cgi">bbs.cgi</a>
│   │   ├── <a href="./cgi-bin/kscrr1p9/bbs.log">bbs.log</a>
│   │   └── sub/
│   │       ├── <a href="./cgi-bin/kscrr1p9/sub/bbsadmin.pl">bbsadmin.pl</a>
│   │       ├── <a href="./cgi-bin/kscrr1p9/sub/bbscust.pl">bbscust.pl</a>
│   │       ├── <a href="./cgi-bin/kscrr1p9/sub/bbslog.pl">bbslog.pl</a>
│   │       ├── <a href="./cgi-bin/kscrr1p9/sub/bbssrc.pl">bbssrc.pl</a>
│   │       └── <a href="./cgi-bin/kscrr1p9/sub/bbstopic.pl">bbstopic.pl</a>
│   └── kscrr1p9up/
│       ├── <a href="./cgi-bin/kscrr1p9up/bbs.cgi">bbs.cgi</a>
│       ├── <a href="./cgi-bin/kscrr1p9up/bbs.log">bbs.log</a>
│       ├── <a href="./cgi-bin/kscrr1p9up/bbs.upd">bbs.upd</a>
│       └── sub/
│           ├── <a href="./cgi-bin/kscrr1p9up/sub/bbsadmin.pl">bbsadmin.pl</a>
│           ├── <a href="./cgi-bin/kscrr1p9up/sub/bbscust.pl">bbscust.pl</a>
│           ├── <a href="./cgi-bin/kscrr1p9up/sub/bbslog.pl">bbslog.pl</a>
│           ├── <a href="./cgi-bin/kscrr1p9up/sub/bbssrc.pl">bbssrc.pl</a>
│           ├── <a href="./cgi-bin/kscrr1p9up/sub/bbstopic.pl">bbstopic.pl</a>
│           └── <a href="./cgi-bin/kscrr1p9up/sub/bbsup.pl">bbsup.pl</a>
└── archive/
    ├── <a href="./archive/kuzuhascript01.zip">kuzuhascript01.zip</a>
    ├── <a href="./archive/kuzuhascript02.zip">kuzuhascript02.zip</a>
    └── <a href="./archive/checksums.txt">checksums.txt</a>
</pre>
