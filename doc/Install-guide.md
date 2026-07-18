# インストールガイド（kuzuhascript-utf8 / bbs.cgi）

Ubuntu + Apache2 環境に、Perl製CGI掲示板 `bbs.cgi` を設置する手順。
本ガイドの内容は、実際のトラブルシューティングで確認された事実に
基づく。

## 1. 動作要件

- Apache 2.4系（`mod_cgi` を推奨。詳細は「6. 補足：mod_cgiとmod_cgidについて」参照）
- Perl（設置先サーバーの実際のパスを`which perl`で確認すること）

## 2. 配布ファイル構成

実際の配布構成は、バージョンフォルダ（例：`kscrr1p9`）の配下に
一式がまとまっている。`bbs.cgi`は単体完結ではなく、`sub/`配下の
各`.pl`ファイルを`require`する分割構成になっている。

> **注記**：リポジトリには`kscrr1p9up`（画像アップローダー機能
> 付きの派生版と思われる）も存在するが、本ガイドで検証済みなのは
> `kscrr1p9`（本番稼働版）のみである。`kscrr1p9up`はまだ実際に
> 動作確認をしていないため、アップロード先ディレクトリの権限設定
> など、本ガイドに記載の無い追加対応が必要になる可能性がある。

```
cgi-bin/
└── kscrr1p9/            # 本番稼働バージョン
    ├── bbs.cgi           # 本体（sub/*.plをrequire）
    ├── bbs.log           # 空ファイル（0バイト）。必須（詳細は3.3）
    ├── sub/
    │   ├── bbsadmin.pl
    │   ├── bbscust.pl
    │   ├── bbslog.pl
    │   ├── bbssrc.pl
    │   └── bbstopic.pl
    ├── count/
    │   └── dummy.txt     # プレースホルダ（詳細は3.4）
    └── log/
        └── dummy.txt     # プレースホルダ（count/と同じ理由。詳細は3.4）
```

`dummy.txt`の中身（`count/`・`log/`共通）：

```
#This file is dummy:Directory permission is 777.
```

空のディレクトリはzip圧縮やGitでは保持されないことがあるため、
ディレクトリ自体を配布物に含めるための目印としてこのファイルを
置いている（ファイル自体に機能上の意味は無い）。

## 3. セットアップ手順

### 3.1 ファイルの配置

上記の構成で `cgi-bin/` 以下をサーバーにアップロードする。

### 3.2 シバン行の確認

`bbs.cgi` の1行目が、設置先サーバーの実際のPerlパスと一致している
ことを確認する。

```bash
which perl
head -1 /path/to/cgi-bin/bbs.cgi
```

一致しない場合は書き換える（例：`#!/usr/local/bin/perl` →
`#!/usr/bin/perl`）。

あわせて、シバン行を含むファイル全体の改行コードがUnix形式（LF）に
なっていることを確認する。Windows形式（CRLF）が混入していると、
シバン行にCR（`\r`）が残り、Apacheがインタプリタのパスを正しく
認識できず実行に失敗する。

```bash
dos2unix /path/to/cgi-bin/bbs.cgi
```

### 3.3 bbs.log について（重要）

`bbs.log` は、投稿メッセージを保持するデータファイルである。
`bbs.cgi` 内部では次のように開いている。

```perl
open ( FLOG, "+<$logfilename" ) || &prterror ( 'メッセージ読み込みに失敗しました' );
```

Perlの `"+<"`（読み書き両用オープン）は**既存のファイルしか開けず、
存在しない場合に自動作成はされない**。そのため、配布物に必ず
**空（0バイト）の`bbs.log`をあらかじめ同梱**しておく必要がある。
これが無い状態でアクセスすると、初回から「メッセージ読み込みに
失敗しました」というエラーで停止する。これはバグではなく、この
実装の仕様である。

### 3.4 count/dummy.txt・log/dummy.txt について

`count/` はアクセスカウンタ等、`log/` は過去ログの初期データ
ファイルを、それぞれ生成・更新するために使用される。**どちらも
`bbs.log`と同様、ディレクトリ自体が存在し、かつ書き込み権限が
無いと、投稿処理の中で`open`が失敗しエラーになる（詳細は
「4. 過去ログ機能についての注意」参照）。**

空のディレクトリはzip圧縮やGitではそのまま保持されないことが
あるため、ディレクトリ自体を配布物に含めるための**プレースホルダ**
として、それぞれに`dummy.txt`を1つ置いている（`dummy.txt`自体に
機能上の意味は無い）。

### 3.5 パーミッション設定

| 対象 | 推奨パーミッション | 理由 |
|---|---|---|
| `bbs.cgi` | 755 | 実行権限が必要 |
| `bbs.log` | 666（または664＋Apache実行ユーザーと同一グループ） | Apache実行ユーザー（例：`www-data`）による読み書きが必要 |
| `count/` | 777（または775＋グループ調整） | Apache実行ユーザーによる新規ファイル作成（書き込み）が必要 |
| `log/` | 777（または775＋グループ調整） | 同上。過去ログファイルを新規作成するため |

環境によっては、777より厳密に「所有者/グループをApache実行ユーザー
（`www-data`等）に合わせた上で775」とする方が望ましい場合もある。
運用ポリシーに応じて調整すること。

```bash
chmod 755 cgi-bin/bbs.cgi
chmod 666 cgi-bin/bbs.log
chmod 777 cgi-bin/count cgi-bin/log
```

### 3.6 Apacheの設定

CGIモジュールを有効化する。

```bash
sudo a2enmod cgi
```

`ScriptAlias` と `ExecCGI` を設定する。**httpとhttps、両方の
VirtualHost設定ファイルに同じ内容を書くこと。** 片方にしか書かれて
いないと、もう片方のポートでアクセスした際にサーバー標準の
CGIパス（例：Ubuntuでは`/usr/lib/cgi-bin/`）にフォールバックし、
意図した`bbs.cgi`が実行されない。

```apache
ScriptAlias /cgi-bin/ /var/www/html/cgi-bin/

<Directory "/var/www/html/cgi-bin/">
    Options +ExecCGI
    Require all granted
</Directory>
```

設定後、構文チェックと再起動を行う。

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```

### 3.7 動作確認

```bash
curl -sk -o /dev/null -w "%{http_code}\n" https://<ホスト名>/cgi-bin/bbs.cgi
```

`200` が返れば、掲示板トップページの表示・投稿・過去ログ出力を
それぞれブラウザで確認する。

## 4. 過去ログ機能についての注意（必須ディレクトリ・保存モード）

`log/`は`count/`と同じく**必須のディレクトリ**である。

```perl
# 過去ログ保存用ディレクトリの名前
$oldlogfiledir = './log/';
```

この設定が空文字でない限り、投稿処理（`putmessage`）の中で必ず
過去ログ出力用の`open`が実行される。

```perl
if ( $oldlogfiledir ) {
    ...
    open ( CLOG, ">>$oldlogfilename" ) || &prterror ( '過去ログ出力に失敗しました' );
    ...
}
```

`log/`ディレクトリが存在しない、または書き込み権限が無い場合、
**過去ログを閲覧する時ではなく、投稿する時点で**このエラーが
発生する（`bbs.log`への保存自体は先に成功しているため、投稿処理の
後半で止まる形になる）。

さらに、`$oldlogsavesw`（保存方法）の設定によって、ファイル名の
組み立て方が変わる。
ファイル名の組み立て処理には、ディレクトリとファイル名を区切る
`/`が含まれていない。

```perl
$oldlogfilename = sprintf ( "%s%d%02d.$oldlogext", $oldlogfiledir, $year, $mon );
```

そのため `$oldlogfiledir` の設定値には、**必ず末尾にスラッシュを
付ける**こと（例：`'./log/'`。`'./log'`ではない）。付け忘れると、
過去ログファイルが`log/`ディレクトリの中ではなく、`cgi-bin`直下に
誤った名前（例：`log202607.dat`）で作成されてしまう。

## 5. トラブルシューティング早見表

| 症状 | 主な原因 |
|---|---|
| ソースコードがそのまま表示される | CGIとして認識されていない（`ExecCGI`未設定等） |
| 404（見つからない） | `ScriptAlias`の設定漏れ、または該当ポート（http/https）側の設定漏れ |
| 500＋`exec ... failed` | シバンのパス不一致、またはシバン行のCRLF残存 |
| 「メッセージ読み込みに失敗しました」 | `bbs.log`が存在しない、または書き込み権限不足 |
| 「過去ログ出力に失敗しました」 | `log/`ディレクトリの権限不足、または`$oldlogfiledir`の末尾スラッシュ抜け |

## 6. 補足：mod_cgiとmod_cgidについて

`mod_cgid`は、スレッド型MPMでのfork負荷を避けるために常駐デーモンが
CGIを実行する方式。`mod_cgi`は、リクエストごとにサーバー本体が
直接CGIを起動する、より素朴な方式で、実行時にスクリプト自身の
ディレクトリへ確実に移動してから実行する。

サーバーのMPMがprefork（非スレッド型）である場合、`mod_cgid`である
必然性は無く、`mod_cgi`の方が実行時のディレクトリ解決に関するトラブル
が少ない。

```bash
sudo a2dismod cgid
sudo a2enmod cgi
sudo systemctl restart apache2
```

上記の設定・パーミッションがすべて揃っていれば、`bbs.cgi`内の実行時
ディレクトリ解決用コード（`use Cwd 'abs_path'; use File::Basename;
chdir dirname(abs_path($0));`）は不要であることを確認済み。動態保存の
方針（コード本体は変更しない）に従う場合、このコードは追加しない
運用を推奨する。
