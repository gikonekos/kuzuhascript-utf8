# Setup Guide / 設置の手引き

## English

Based on the 2000 kuzuhascript setup guide by Hiroyuki Ishii (石井博之),
updated for this fork: no jcode.pl needed, and permission guidance carried
over as-is since it remains a common source of trouble, especially for
first-time users.

### What you need

- This script (`cgi-bin/kscrr1p9/` or `cgi-bin/kscrr1p9up/`)
- A CGI-capable server, an FTP client, and a text editor
- Empty `log` and `count` directories, created at the same level as `bbs.cgi`

### Directory layout

```
[public_html]  (701)
 └─ [cgi-bin]  (701)
     ├─ bbs.cgi        (700)
     ├─ bbs.log        (600)
     ├─ [log]          (755)
     ├─ [count]        (755)
     └─ [sub]           (701)
         ├─ bbsadmin.pl  (700)
         ├─ bbscust.pl   (700)
         ├─ bbslog.pl    (700)
         ├─ bbssrc.pl    (700)
         └─ bbstopic.pl  (700)
```
`[ ]` = directory, `( )` = permission value.

### Editing bbs.cgi

Example changes when deploying to `http://example.com/cgi-bin/bbs.cgi`:

- Line 1 (`#! /usr/local/bin/perl`): the path to Perl. Must be the very
  first line, with nothing before `#!`. Check your host's FAQ — often
  `/usr/bin/perl` instead. **If you change this, change it identically in
  every file under `sub/`.**
- `$cgiurl`: set to the CGI's public URL.
- `$gzip`: path to `gzip`, or leave as an **empty string** (not a space) if
  your host doesn't support it or you're unsure. A wrong path causes a 500
  error.
- `$bbshost`: the host address the CGI is served from.
- `$difftime`: time difference from Japan, in hours (0 for a Japan-based
  host).
- `$bbstitle`: the board's display name.
- `$oldlogfmt`: `0` = HTML-format old logs (no topic list / no quote-from-log
  features), `1` = binary `.dat` format (smaller, supports both features).
- `$oldlogsavesw` / `$oldlogsaveday`: rotate old logs daily or monthly; with
  daily rotation, logs older than `$oldlogsaveday` days are deleted
  automatically.
- `$protect_a` / `$protect_b`: anti-flood codes — **always change these from
  the defaults.**
- `$adminname`: only needed if you want impersonation protection (blank
  otherwise).
- `$adminpost`: leave blank initially; you'll fill this in after the first
  password-setup step below.
- `$adminkey`: the admin-mode keyword — **always change this from the
  default.** Don't reuse a password from anywhere else; assume the server
  could be viewed by others.
- `$infopage`: your info/contact page URL.

### Uploading files

Upload everything, including directories, in **text (ASCII) mode** via FTP.
Confirm the `cgi-bin` layout matches what's shown above once uploaded.

### Permissions

This is where most first-time setups go wrong — take care here.

```
[public_html]  (701 / 705 / 755)
 └─ [cgi-bin]  (701 / 705 / 755)
     ├─ bbs.cgi        (700 / 705 / 755)
     ├─ bbs.log        (600 / 606 / 666)
     ├─ [log]          (755)
     ├─ [count]        (755)
     └─ [sub]           (701 / 705 / 755)
         ├─ bbsadmin.pl  (700 / 705 / 755)
         ├─ bbscust.pl   (700 / 705 / 755)
         ├─ bbslog.pl    (700 / 705 / 755)
         ├─ bbssrc.pl    (700 / 705 / 755)
         └─ bbstopic.pl  (700 / 705 / 755)
```

If the leftmost value doesn't work on your host, try the next value to the
right. **The further right you go, the looser (less secure) the
permissions become** — only relax them as far as actually necessary, and
don't forget directories need their permissions changed too, not just files.

### First access and password setup

1. Visit the URL where you installed the CGI — a password-setup screen
   appears.
2. Enter any password (6+ alphanumeric characters).
3. An encrypted password string is displayed (e.g. `JBpdYtgMI8.p9`).
4. Put that encrypted string into `$adminpost` in `bbs.cgi`.
5. Re-upload the edited `bbs.cgi`. Done.

### Troubleshooting

- **404 Not Found** — Does the URL you're visiting match `$cgiurl` in
  `bbs.cgi`? Is `bbs.cgi` actually inside `cgi-bin`?
- **403 Forbidden** — Check permissions, including on *directories*, not
  just files.
- **500 Internal Server Error** — Check the Perl path on line 1 (no
  leading space/blank line before `#!`), the `$gzip` path (leave blank if
  unsure), and that you haven't accidentally deleted a `'` or `;` while
  editing.
  If nothing works, it's often fastest to delete everything (local and
  server-side) and start over, changing only the minimum necessary settings.

### Customizing HTML output

A few Perl syntax rules to keep in mind when customizing the HTML this
script generates:

1. Comment lines start with `#`.
2. Perl statements end with `;`.
3. Inside `print "..."；`, a literal `"` inside the string must be written
   as `\"`.
4. A literal `@` in a string (other than via `$adminmail`) must be written
   as `\@` — otherwise Perl tries to interpret it as an array. Prefer using
   the `$adminmail` variable itself rather than hardcoding an address.
5. Full-width spaces can cause errors — use half-width spaces when editing
   generated HTML.

## 日本語

くずはすくりぷと設置の手引き（2000年、石井博之氏作）を参考に、本フォーク向けに
更新したものです。jcode.plは既に不要になったため関連記述を削除し、パーミッション
まわりは初心者が特に躓きやすい重要な箇所として、そのまま引き継いでいます。

### 用意するもの

- 本スクリプト（`cgi-bin/kscrr1p9/` または `cgi-bin/kscrr1p9up/`）
- CGIが動くサーバ、FTPクライアント、エディタ
- bbs.cgiと同じ階層に、空の`log`ディレクトリと`count`ディレクトリ

### ディレクトリ構造

```
[public_html]  (701)
 └─ [cgi-bin]  (701)
     ├─ bbs.cgi        (700)
     ├─ bbs.log        (600)
     ├─ [log]          (755)
     ├─ [count]        (755)
     └─ [sub]           (701)
         ├─ bbsadmin.pl  (700)
         ├─ bbscust.pl   (700)
         ├─ bbslog.pl    (700)
         ├─ bbssrc.pl    (700)
         └─ bbstopic.pl  (700)
```
`[ ]`はディレクトリ、`( )`はパーミッションの値。

### bbs.cgiの設定変更

`http://example.com/cgi-bin/bbs.cgi` に設置する場合の変更例：

- 1行目（`#! /usr/local/bin/perl`）：perlのパス。必ず1行目に記述し、
  `#!`の前にスペースや改行を入れない。サーバのFAQ等で確認（`/usr/bin/perl`
  のことも多い）。**ここを変更する場合は`sub/`内の全ファイルも同様に変更。**
- `$cgiurl`：設置先の公開URL。
- `$gzip`：gzipのパス、または不明・非対応の場合は**空文字列**（空白スペース
  ではない）。パスを間違えると500エラーの原因になる。
- `$bbshost`：設置先のホストアドレス。
- `$difftime`：日本との時差（時間）。国内サーバなら0。
- `$bbstitle`：掲示板名。
- `$oldlogfmt`：`0`＝HTML形式（トピック一覧・過去ログ引用不可）、
  `1`＝バイナリ.dat形式（サイズ小・両機能が使用可能）。
- `$oldlogsavesw` / `$oldlogsaveday`：過去ログを日毎/月毎で保存。日毎の場合、
  指定日数を過ぎたログは自動削除される。
- `$protect_a` / `$protect_b`：連続投稿防止コード。**必ずデフォルトから
  変更すること。**
- `$adminname`：騙り防止機能を使う場合のみ設定（不要なら空）。
- `$adminpost`：最初は空のままにしておく（後述の手順で設定）。
- `$adminkey`：管理モード移行キーワード。**必ずデフォルトから変更する
  こと。** 他で使っているパスワードは流用しない。サーバは他人に覗かれ得る
  ものと考えるのが一番の安全策。
- `$infopage`：連絡先ページのURL。

### ファイルのアップロード

すべてのファイル・ディレクトリを**テキストモード（ASCIIモード）**でFTP
アップロードする。アップロード後、`cgi-bin`内が上記の構造通りになっている
ことを確認する。

### パーミッションの変更

初回設置で最も躓きやすい箇所です。慎重に。

```
[public_html]  (701 / 705 / 755)
 └─ [cgi-bin]  (701 / 705 / 755)
     ├─ bbs.cgi        (700 / 705 / 755)
     ├─ bbs.log        (600 / 606 / 666)
     ├─ [log]          (755)
     ├─ [count]        (755)
     └─ [sub]           (701 / 705 / 755)
         ├─ bbsadmin.pl  (700 / 705 / 755)
         ├─ bbscust.pl   (700 / 705 / 755)
         ├─ bbslog.pl    (700 / 705 / 755)
         ├─ bbssrc.pl    (700 / 705 / 755)
         └─ bbstopic.pl  (700 / 705 / 755)
```

左の数値で動かない場合は、右へ順に試す。**右に行くほどセキュリティが
甘くなる**ので、必要な分だけ緩める。ファイルだけでなく**ディレクトリの
パーミッション変更も忘れずに**。

### 掲示板へのアクセスとパスワード設定

1. 設置したURLにアクセスすると、パスワード設定画面が表示される。
2. 任意のパスワード（6文字以上の半角英数字）を入力する。
3. 暗号化済みパスワード（例：`JBpdYtgMI8.p9`）が表示される。
4. その文字列を`bbs.cgi`の`$adminpost`に記入する。
5. 編集した`bbs.cgi`を再アップロードして完了。

### エラーが出る場合

- **404 file not found**：アクセスしたURLと`$cgiurl`の設定は一致しているか。
  `bbs.cgi`は本当に`cgi-bin`内にあるか。
- **403 forbidden**：パーミッションを確認（ファイルだけでなく
  ディレクトリも）。
- **500 internal server error**：1行目のperlパス（前にスペースや改行が
  ないか）、`$gzip`のパス（不明なら空に）、編集中に`'`や`;`を誤って
  消していないかを確認。
  どうしても直らない場合は、ローカル・サーバ双方のファイルを一旦全て
  消し、必要最小限の設定変更だけで最初からやり直すのが早いことが多い。

### HTML出力のカスタマイズ時の注意

出力されるHTMLをカスタマイズする際に踏まえておきたいPerlの構文ルール：

1. コメント行は`#`で始める。
2. Perl文の行末には`;`を入れる。
3. `print "～"；`の文中でリテラルの`"`を使う場合は`\"`と書く。
4. 文字列中にリテラルの`@`（`$adminmail`経由以外）を書く場合は`\@`と書く。
   そうしないとPerlが配列として解釈しようとする。できれば直書きせず
   `$adminmail`変数を使う。
5. 全角スペースはエラーの原因になるため、生成HTMLを編集する際は半角
   スペースを使う。
