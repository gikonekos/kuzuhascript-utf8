# changelog

**English summary:** This file records, in Japanese, the detailed change
history of this fork (character-encoding conversion, vulnerability fixes,
bug fixes). Three stages so far: (1) cp932→UTF-8 conversion and removal of
the jcode.pl dependency, (2) a charset-mismatch bug fix plus functional
testing, (3) three vulnerability fixes (path traversal / command injection
via an unvalidated parameter, a validation gap reusing a stale regex capture,
and missing double-quote escaping enabling attribute-based XSS) and a
systematic corruption bug affecting dozens of labels across the original 2000
source. See the Japanese entries below for full detail, or ask for an English
translation of the complete log.

形式: ISO 8601 (YYYY-MM-DDTHH:MM, JST)

## 2026-07-16T16:07 Stage 1: 文字コード変換 + jcode.pl不使用化（完了）

対象: `kscrr1p9/`（Rev.0.1 Preview 9 素）, `kscrr1p9up/`（+アップローダーPlugin）

- 全.cgi/.plファイル（bbs.cgi, sub/bbsadmin.pl, sub/bbscust.pl, sub/bbslog.pl,
  sub/bbssrc.pl, sub/bbstopic.pl, sub/bbsup.pl）を cp932からUTF-8へ変換
  （`iconv -f CP932 -t UTF-8`）
  - 全ファイルでデコードエラーなし（不正バイトなし）を確認
  - 変換後、`file -i` にて charset=utf-8 を確認
  - 2バイト目が0x5C等になる機種依存文字（例:「表」）による文字化け・破損は
    発生せず（バイト列単位の変換のため）
- jcode.pl不使用化
  - `$jcode = './jcode.pl';` の定義行をコメントアウト
  - `sub jconv` 内の `require "$jcode"` / `&jcode'convert(...)` 呼び出しを
    コメントアウト（jconv自体は空関数として温存、次段階で再実装予定）
- `perl -c` によるシンタックスチェック: 全ファイルOK（perl 5.38.2）
- `arc2/kscrr1p9.lzh`, `arc2/kscrr1p9up.lzh`（原本アーカイブ）は無改変のまま保持

**未着手・次段階へ持ち越し:**
- 実行時（CGI動作時）の文字コード正規化処理の再実装
  （jconv無効化に伴い、投稿/検索フォームのデータ正規化が現状no-op）
- bbslog.pl検索フォームの「jcode.pl使用」チェックボックス表記の扱い
  （現状は死んだUIとして残存、削除/変更は未実施）
- 最新Perlでのbbs.cgi実機動作確認（バグ潰し段階）

---

## 2026-07-16T16:14 Stage 2: バグ潰し（動作確認・1件修正）

対象: `kscrr1p9/`, `kscrr1p9up/`

- 修正: HTMLメタタグのcharset不一致バグ
  - `<META charset=Shift_JIS>` のままだったため、UTF-8変換後のHTML出力と
    矛盾し文字化けの原因になっていた
  - bbs.cgi（board/エラー/管理画面、計3箇所×2インスタンス）、
    sub/bbslog.pl（検索画面、1箇所×2インスタンス）を charset=UTF-8 に修正
    （計8箇所）
- 実機動作確認（perl 5.38.2、CGI環境変数を模擬して実行）
  - 板表示（GET, デフォルト）: 正常動作、文字化けなし
  - 投稿（POST, 日本語UTF-8データ）: 正常動作
    - bbs.logへの書き込み確認（UTF-8バイト列で正しく保存）
    - 過去ログ（log/YYYYMMDD.dat）出力確認
    - 投稿内容の表示確認（文字化けなし）
  - 過去ログ検索・一覧（m=g, bbslog.pl）: 正常動作、作成した過去ログファイルを
    正しく検出
  - kscrr1p9up（アップローダーPlugin版）板表示も同様に確認
  - stderr出力なし、exit code 0（全ケース）
- 確認済み・バグではないもの:
  - `$adminpost`未設定時のパスワード設定画面誘導 → 仕様通りの初回動作
  - `log/`ディレクトリ未作成時の「過去ログ出力に失敗しました」エラー →
    デプロイ時に./log/を用意する前提の既存仕様（今回テスト環境の準備不足に
    よるもの、スクリプト側の不具合ではない）
  - 初回リクエスト時のカウンターファイルエラー表示 → bbs.cnt未作成時の
    想定内動作（「こわれにくさレベル2」設計、自動生成で自己回復）
- テスト用に生成した一時ファイル（bbs_test.cgi, log/, bbs.cnt,
  テスト投稿データ）は全て削除・bbs.logは空の状態に復元済み

**未着手・次段階へ持ち越し:**
- 実行時の文字コード正規化処理の再実装（jconv代替）
- bbslog.pl「jcode.pl使用」チェックボックスの扱い
- multipart/form-data経由のアップローダー機能（bbsup.pl）の実機動作確認
- 過去ログ検索・キーワード検索など、より広範なモードの網羅的テスト

---

## 2026-07-17T01:01 Stage 2続き: 脆弱性対策 + 単純バグ（表\示問題）の修正

対象: `kscrr1p9/`, `kscrr1p9up/`

参考資料: exsample_com.zip（実働あやしいわーるど＠暫定方式改造版、トリップ機能・
ツリー機能は仕様外のため今回は不採用。ただしjcode.pl不使用方針の裏付けとして
有用だった）

**[脆弱性1] `$FORM{'e'}`の未検証使用によるパストラバーサル/コマンド実行**
- sub/bbslog.pl `prtoldlog`、sub/bbstopic.pl `gettopic` の両方で
  `open ( OLDLOG, "$oldlogfiledir$FORM{'e'}" )` と外部入力を無検証で
  2引数open()に渡していた
  - パストラバーサル（../等）による任意ファイル読み込みの危険性
  - Perlの2引数open()仕様上、文字列末尾が"|"だとシェルコマンドとして実行
    される（例: `e=; touch /tmp/x |`）ため、RCEの危険性もあった
- bbslog.pl側はgetlog()内に既存の別の検証（`$FORM{'e'}=~/^([\w.]*)$/`）が
  あり実際にはそちらで防御されていたが、bbstopic.pl側（m=lモード）は上流の
  検証が一切なく、実際に攻撃文字列が素通りすることを確認・再現した
- 対策: `^(\d{6,8}\.(?:html|dat))$` の厳密なホワイトリスト正規表現で検証し、
  不一致ならエラー表示に倒す。あわせて2引数open()を `open(FH, '<', $path)`
  の3引数形式に変更（防御の多層化）
- 動作確認: 正規のファイル名（例: 20260716.dat）は従来通り表示、
  `../../../../etc/passwd` および `; touch /tmp/x |` の両攻撃パターンは
  「不正なログファイル名です。」で拒否されることを確認

**[脆弱性2] `$FORM{'ff'}`の検証漏れ（マッチ失敗時に直前の$1を使い回す）**
- bbs.cgi `loadmessage`内、`$FORM{'ff'} =~ /^([\w.]*)$/;` の結果をチェック
  せず$1をそのまま使用していたため、不一致時に無関係な直前の正規表現結果が
  使われる可能性があった（実害は限定的だが不定動作のため是正）
- 対策: `unless (マッチ) { エラー表示 }` に変更し、不一致時は明示的に
  エラーとするよう修正

**[脆弱性3] HTML属性値への反射時の"（ダブルクォート）未エスケープ**
- getformdata内で&,<,>はエスケープされていたが"が漏れていたため、投稿者名等を
  `value="..."`に反映する箇所で例: `テスト" onmouseover="alert(1)` のような
  入力によりHTML属性からのエスケープ（XSS）が可能だった
- 対策: `$value =~ s/"/&quot;/g;` を追加
- 動作確認: 上記ペイロードを投稿し、`&quot;`に正しく変換され属性から
  抜け出せないことを確認

**[単純バグ] 「表\示」問題（cp932の2バイト目0x5C機種依存文字の重複破損）**
- 原文2000年オリジナルソースの時点で、CP932の2バイト目が0x5C
  （バックスラッシュと同じバイト値）になる文字（表=955C、能=945C等）の
  直後に、余分な0x5Cバイトが挿入されていた
- **【2026-07-17追記・訂正】原因を特定** ks*.zip（ksinst.zip, dauso0036.html /
  ksinst.html「くずはすくりぷと設置の手引き」2000/9/03付）を確認したところ、
  これは編集ツールによる意図しない破損ではなく、**当時のカスタマイズ利用者
  向けに明示的に指導されていた回避策**だったことが判明した。同手引きには
  「文字化けする漢字は、後ろに『\』を置く」とあり、文字化けを起こす例として
  「申」「十」「ソ」「能」「予」「貼」「表」「噂」「圭」「兔」「饅」が
  列挙されている。いずれもCP932の2バイト目が0x5Cになる文字であり、当時の
  一部ツール（HTML編集画面やFTP転送等）がこのバイトを誤ってエスケープ文字と
  解釈する問題を、利用者側でバックスラッシュを追加して回避する、という
  Shift_JIS時代特有の運用上のワークアラウンドだったと考えられる
- 上記の通り原因は「破損」ではなく「意図的な回避策」だが、UTF-8化した
  時点でこの問題（CP932の2バイト目とASCIIバックスラッシュの衝突）自体が
  そもそも発生しなくなるため、このワークアラウンドは完全に不要かつ有害
  （素通しで表示されるとただの誤字にしか見えない）になる。そのため
  UTF-8版では削除するのが正しい対応であり、本修正の妥当性に変わりはない
- 影響箇所: 「表\示」「機能\使用」「機能\設定」等、表示件数・画面表示・
  検索表示・スレッド表示・付加機能設定・表示方法・降順表示・昇順表示等
  多数のラベル文字列（bbs.cgi, bbscust.pl, bbslog.pl, bbstopic.pl, bbsup.pl
  全体で計42箇所）
- 対策: 「UTF-8マルチバイト文字の直後＆直前に挟まれた単独の0x5Cバイト」を
  機械的に検出・削除するスクリプトで一括修正（`s/\r\n/\r/g`等、正当なPerl
  エスケープシーケンスは前後がASCII文字のため対象外であることを確認済み）
- 動作確認: 修正後の板表示HTMLにバックスラッシュが一切残っていないことを
  確認（`grep -c '\\'` で0件）

perl -c シンタックスチェック: 全ファイルOK（perl 5.38.2）
file -i: 全ファイル charset=utf-8 を維持
テスト用一時ファイル（bbs_test.cgi, log/, bbs.cnt等）は削除、bbs.logは空の
状態に復元済み

**未着手・次段階へ持ち越し:**
- 実行時の文字コード正規化処理の再実装（jconv代替）
- bbslog.pl「jcode.pl使用」チェックボックスの扱い
- multipart/form-data経由のアップローダー機能（bbsup.pl）の実機動作確認
- 過去ログ検索・キーワード検索など、より広範なモードの網羅的テスト
- より広範な脆弱性監査（admin機能側の権限チェック等、未着手の範囲）
