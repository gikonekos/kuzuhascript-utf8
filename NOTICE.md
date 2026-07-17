# NOTICE

## English

### Original Work

- Name: kuzuhascript (くずはすくりぷと) Rev.0.1 Preview 9 (2000.9.3)
- Author: kuzuha (くずは)
- Copyright (c) 2000 kuzuha (くずは). All rights reserved.
- Two editions included:
  - `kscrr1p9/` — plain edition
  - `kscrr1p9up/` — edition with uploader plugin

The unmodified original files are included in `archive/kuzuhascript02.zip`.
Note, however, that `kuzuhascript02.zip` itself was repackaged into zip
format by Motoi Kenkichi, for convenience, from the original archives
(`kscrr1p9.lzh`, `kscrr1p9up.lzh`) kept on his own CD-R. The zip container
was created by Motoi Kenkichi, but the `kscrr1p9.lzh` / `kscrr1p9up.lzh`
files inside it are unmodified since they were archived on that CD-R. The
"never touch the archive" principle applies to these lzh files — the true
originals.

`archive/kuzuhascript01.zip` is reference material from an older, unrelated
version lineage (kuzuhascript Final Beta #2 Patch Level 0.3, 1999), including
its readme.txt. It is a different version from the one modified in this
repository (Rev.0.1 Preview 9), and is bundled unmodified as evidence that
its text has not been altered.

### About This Repository

This repository is a fork of the original work above, intended to run in a
modern Perl environment. Main changes:

- Character encoding conversion (cp932 → UTF-8)
- Removal of the jcode.pl dependency
- Vulnerability fixes (see doc/changelog.md)
- Simple bug fixes (see doc/changelog.md)

Full change history: [doc/changelog.md](./doc/changelog.md). Before
deploying anything from this repository, also read
[SECURITY.md](./SECURITY.md).

### License

The original work and the modifications are licensed differently. See
[LICENSE](./LICENSE) for details.

## 日本語

### 原著作物

- 名称: くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
- 著作者: kuzuha (くずは)
- Copyright (c) 2000 kuzuha (くずは). All rights reserved.
- 収録している2系統:
  - `kscrr1p9/` - 無印版
  - `kscrr1p9up/` - アップローダーPlugin付き版

原本（無改変のオリジナルファイル一式）は `archive/kuzuhascript02.zip` 内に
収録しています。ただし、この`kuzuhascript02.zip`自体は、Motoi Kenkichiが
所有するCD-Rに保存されていた原本アーカイブ（`kscrr1p9.lzh`, `kscrr1p9up.lzh`）
を、扱いやすくする目的でzipに再梱包したものです。zipという入れ物自体は
Motoi Kenkichiが作成しましたが、中身の`kscrr1p9.lzh` `kscrr1p9up.lzh`は
CD-R保存時点から無改変です。「アーカイブは弄らない」の原則は、この
lzhファイル（＝真の原本）に対して適用されています。

`archive/kuzuhascript01.zip` は、より古い別系統のバージョン
（くずはすくりぷと Final Beta #2 Patch Level 0.3, 1999年）のreadme.txtを
含む参考資料です。本リポジトリの改造対象（Rev.0.1 Preview 9）とは異なる
バージョンですが、テキストが改変されていないことの証明として、無改変のまま
参考用に同梱しています。

### 本リポジトリの位置づけ

本リポジトリは、上記原著作物を最新のPerl環境で実働させることを目的とした
改造版です。主な改変内容:

- 文字コード変換（cp932 → UTF-8）
- jcode.pl不使用化
- 脆弱性対策（詳細はdoc/changelog.md参照）
- 単純バグの修正（詳細はdoc/changelog.md参照）

改変内容の完全な履歴は [doc/changelog.md](./doc/changelog.md) を参照して
ください。本リポジトリの内容を配置・運用する前に、[SECURITY.md](./SECURITY.md)
も必ずお読みください。

### ライセンス

原著作物と改変部分でライセンスの扱いが異なります。詳細は [LICENSE](./LICENSE)
を参照してください。
