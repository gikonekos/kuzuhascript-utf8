#! /usr/local/bin/perl

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (アップローダープラグイン)
#

#
#  ※MethodはPOSTのみ使用可能です。
#  ※MacOSからのアップロードや、拡張子のないファイルのアップロードは、正常に
#    行われないかも知れません。(当方では確認が取れません)
#  ※このスクリプトを使用して、著作権を侵害するような行為が行われていたとして
#    も、当方は一切責任を負いません。設置及び運用は全て管理人の自己責任でお願
#    いします。
#

###############################################################################
#  設定
###############################################################################

# 添付ファイルの最大サイズ(byte)
#  ※下記の条件に１つでも該当するサーバーでは、できるだけ少なめに設定すること
#    をお薦めします。デフォルトサイズは500kバイトです
#    ・httpdのタイムアウトが短い
#    ・メモリ搭載量が少ない
#    ・常時負荷がかかっている
#    ・回線が細い
#    ・使用できるディスク容量が少ない
$upmaxsize = 500 * 1024;

# サーバーのOSタイプ
#  ※Windows系の場合、誤った設定を行うと、ファイルが破損する可能性があります。
#   0 : UNIX系 (Solaris, Linux, BSD系, IRIX, AIX, DigitalUNIX, HP-UXなど)
#   1 : Windows系 (Windows 9x, NT, 2000など)
$ostype = 0;

# ファイル名の命名方法
#   0 : スクリプト側で自動的に命名（連番）
#   1 : アップされるファイル名と同じファイル名を使用
#       (重複する場合はファイル名の先頭に連番を付加します)
$fnamemode = 0;

# ファイル保存数
$filesave = 200;

# アップロードログファイル名
$uplogfilename = './frame.upd';

# アップロードファイル保存用ディレクトリの名前
$upfiledir = './upload/';

# アップロードファイルの格納先ディレクトリのURL
$upfileurl = 'http://strange.kurumi.ne.jp/frame/upload/';


###############################################################################
#  システム用設定・変数
###############################################################################

$UP_fname[0] = '';	# アップロードファイル名
$UP_fext[0] = '';	# アップロードファイル拡張子


###############################################################################
#  multipartフォームデコード
###############################################################################

sub getmultipart {
	
	my ( @formbuf, $bound, $fname, $fnum, $ctype );
	
	binmode ( STDIN ) if $ostype;
	@formbuf = <STDIN>;
	$formbuf[0] =~ /^(.+)\r\n/;
	$bound = $1;
	
	$fname = '';
	$i = 0;
	while ( $formbuf[$i] ) {
		if ( $formbuf[$i] =~ /$bound/ ) {
			if ( $fname && ! ( $fname =~ /fileurl/ ) ) {
				$FORM{$fname} =~ s/&/&amp;/g;
				$FORM{$fname} =~ s/</&lt;/g;
				$FORM{$fname} =~ s/>/&gt;/g;
				$FORM{$fname} =~ s/\r\n/\r/g;
				$FORM{$fname} =~ s/\n/\r/g;
				$FORM{$fname} =~ s/\r$//;
				$FORM{$fname} =~ s/\,/\0/g;
			}
			$formbuf[++$i] =~ / name=\"(\w+)\"/;
			$fname = $1;
			if ( $fname =~ /fileurl(\d+)/ ) {
				$fnum = $1;
				$formbuf[$i] =~ / filename=\"(.*)\"/;
				$UP_fname[$fnum] = $1;
				$UP_fname[$fnum] =~ s#/##g;
				$UP_fname[$fnum] =~ s/^\.//g;
				if ( $UP_fname[$fnum] =~ /\\/ || $UP_fname[$fnum] =~ /\// ) {
					$UP_fname[$fnum] =~ /.*(\\|\/)(\S+)$/;
					$UP_fname[$fnum] = $2;
				}
				$formbuf[++$i] =~ /Content-Type: (.*)/;
				$ctype = $1;
				if ( $ctype =~ /jpeg/ ) {
					$UP_fext[$fnum] = 'jpg';
				} elsif ( $ctype eq 'image/gif' ) {
					$UP_fext[$fnum] = 'gif';
				} elsif ( $ctype eq 'image/png' ) {
					$UP_fext[$fnum] = 'png';
				} elsif ( $UP_fname[$fnum] =~ /\.(\w+)$/ ) {
					$UP_fext[$fnum] = $1;
				} else {
					$UP_fext[$fnum] = 'xxx';
				}
				$i++;
			} else {
				$i+=2;
				$FORM{$fname} = $formbuf[$i];
			}
		} elsif ( $fname ) {
			$FORM{$fname} .= $formbuf[$i];
		}
		$i++;
	}
}


###############################################################################
#  ファイル出力
###############################################################################

sub putupfile {
	
	my ( $current, @uplog, $nlog, @items, $upfile, $upcnt, $delfile );
	
	if ( $ENV{'CONTENT_LENGTH'} > $upmaxsize ) {
		&prterror ( '添付するファイルのサイズが大きすぎます。' );
	}
	
	for ( $current = 0 ; $UP_fname[$current] ; $current++ ) {
		
		open ( ULOG, "+<$uplogfilename" ) || &prterror ( 'アップロードログファイルを開けませんでした。' );
		eval 'flock ( ULOG, 2 )';
		seek ( ULOG, 0, 0 );
		@uplog = <ULOG>;
		if ( $uplog[0] ) {
			@items = split ( /\,/, $uplog[0] );
			$upcnt = $items[0];
		} else {
			$upcnt = 0;
		}
		
		$upcnt++;
		$upcnt = sprintf ( "%04d", $upcnt );
		if ( $fnamemode ) {
			if ( ( -s "$upfiledir$UP_fname[$current]" ) > 0 ) {
				$upfile = "$upcnt$UP_fname[$current]";
			} else {
				$upfile = "$UP_fname[$current]";
			}
		} else {
			$upfile = "$upcnt.$UP_fext[$current]";
		}
		$nlog = "$upcnt,$upfile,$host,$agent\n";
		
		if ( @uplog > $filesave ) {
			$delfile = $uplog[$filesave - 1];
			@items = split ( /\,/, $delfile );
			unlink ( "$upfiledir$items[1]" );
			@uplog = @uplog[0 .. $filesave - 2];
		}
		unshift ( @uplog, $nlog );
		
		$oldstream = select ( FLOG );
		$| = 1;
		seek ( ULOG, 0, 0 );
		truncate ( ULOG, 0 );
		print ULOG @uplog;
		eval 'flock ( ULOG, 8 )';
		close ( ULOG );
		select ( $oldstream );
		
		$FORM{"fileurl$current"} =~ s/\r\n$//;
		
		open ( FILE, ">$upfiledir$upfile" ) || &prterror ( 'ファイルを作成できませんでした。' );
		binmode ( FILE ) if $ostype;
		print FILE $FORM{"fileurl$current"};
		close FILE;
		
		# メッセージにアップロードファイルへのリンクを追加
		$FORM{'v'} .= "\r\r<A href=\"$upfileurl$upfile\" target=\"link\">添付ファイル：$upfile</A>";
	}
}


###############################################################################
#  入力フォーム表示
###############################################################################

sub prtupform {
	
	my $dtitle = $_[0];
	my $dmsg = $_[1];
	my $dlink = $_[2];
	my ( $bbslink, $gzipchk, $counter, $mbrcount );
	
	my $ptext = &pcode;
	
	# プロテクトコード生成
	my $ptext = &pcode;
	
	# カウンタ
	$counter = &counter;
	$mbrcount = &mbrcount;
	
	if ( $gzip ) {
		$gzipchk = qq#  　<FONT size="-1">gzip圧縮転送 <INPUT type="checkbox" name="g" value="checked" $S_gzchk[$gzipu]></FONT>#;
	} else {
		$gzipchk = '';
	}
	
	if ( $FORM{'m'} eq 'o' || $FORM{'m'} eq 'op' ) {
		
		# ログ読み専用フォーム
		$bbslink = qq#<A href="$cgiurl?c=$FORM{'c'}">標準画面</A>#;
		print <<EOF;
<FORM method="$formmethod" action="$cgiurl">
  <INPUT type="hidden" name="m" value="op">
  <INPUT type="hidden" name="k" value="あ">
  <INPUT type="hidden" name="c" value="$FORM{'c'}">
  <P><FONT size="-1">表示件数 <INPUT size="6" type="text" name="d" value="$FORM{'d'}">
$gzipchk
  　<FONT size="-1">URL自動リンク <INPUT type="checkbox" name="a" value="checked" $S_alchk[$autolink]></FONT>
  　<INPUT type="submit" name="setup" value="その他の設定"></FONT></P>
  <FONT size="-1">$countdate から $counter（こわれにくさレベル$countlevel）$mbrcount</FONT>
  <HR>
  <FONT size="-1">| 
  <A href="/">広報室</A> |
  <A href="$cgiurl?m=g&c=$FORM{'c'}">最近の過去ログ</A> |
  $bbslink |
  <A href="../bbs2.cgi">はじあや</A> |
  <A href="../bbs3.cgi">☆</A> |
  <A href="http://members.tripod.co.uk/~strange_walker/index.htm">ぁゃιぃ WALKER (復活最新版)</A> |
  </FONT>
  <HR>
  <FONT size="-1">$txtfollow : フォロー投稿画面表示 　 $txtauthor : 投稿者検索表示 　 $txtthread : スレッド表示
  　　　最大登録件数 : $logsave件</FONT>
  <HR>
  <FONT size="-1"><INPUT type="submit" name="reload" value="リロード"></FONT>
  <INPUT type="hidden" name="p" value="$toppostid">
</FORM>
EOF
		
	} else {
		
		# 標準投稿フォーム
		$bbslink = qq#<A href="$cgiurl?m=o&c=$FORM{'c'}">ログ読み専用画面</A>#;
		print <<EOF;
<FORM enctype="multipart/form-data" method="post" action="$cgiurl" >
  <INPUT type="hidden" name="m" value="p">
  投稿者 <INPUT size="20" type="text" name="u" maxlength="30" value="$FORM{'u'}"><BR>
  メール <INPUT size="30" type="text" name="i" maxlength="255" value="$FORM{'i'}"><BR>
  題名 　<INPUT size="30" type="text" name="t" maxlength="40" value="$dtitle">
  <INPUT type="submit" name="post" value="投稿／リロード"> <INPUT type="reset" value="消す"><BR> <BR>
  内容 <FONT size="-1"><I>
  （適当に改行を入れてください。タグは使えません。内容を書かずに投稿ボタンを押すとリロードになります）
  </I></FONT><BR>
  <TEXTAREA rows="5" cols="70" name="v">$dmsg</TEXTAREA><BR> <BR>
  URL <FONT size="-1"><I>（リンクを入れたい場合はここに記入します）</I></FONT><BR>
  <INPUT size="70" type="text" name="l" maxlength="255" value="$dlink"><BR>
  添付ファイル <FONT size="-1"><I> ($upmaxsizeバイトを超えるものは添付できません)</I></FONT><BR>
  <INPUT type="file" name="fileurl0" size="70"><BR>
  $ptext
  <INPUT type="hidden" name="k" value="あ">
  <INPUT type="hidden" name="c" value="$FORM{'c'}">
EOF
		if ( $FORM{'m'} ne 'f' && !$FORM{'f'} ) {
			print <<EOF;
  <P><FONT size="-1">表示件数 <INPUT size="6" type="text" name="d" value="$FORM{'d'}">
  $gzipchk
  　<FONT size="-1">URL自動リンク <INPUT type="checkbox" name="a" value="checked" $S_alchk[$autolink]></FONT>
  　<INPUT type="submit" name="setup" value="その他の設定"></FONT></P>
  <FONT size="-1">$countdate から $counter（こわれにくさレベル$countlevel）$mbrcount</FONT>
  <HR>
  <FONT size="-1">| 
  <A href="/">広報室</A> |
  <A href="$cgiurl?m=g&c=$FORM{'c'}">最近の過去ログ</A> |
  $bbslink |
  <A href="../bbs2.cgi">はじあや</A> |
  <A href="../bbs3.cgi">☆</A> |
  <A href="http://members.tripod.co.uk/~strange_walker/index.htm">ぁゃιぃ WALKER (復活最新版)</A> |
  </FONT>
  <HR>
  <FONT size="-1">$txtfollow : フォロー投稿画面表示 　 $txtauthor : 投稿者検索表示 　 $txtthread : スレッド表示
  　　　最大登録件数 : $logsave件</FONT>
  <HR>
  <FONT size="-1"><INPUT type="submit" name="reload" value="リロード"></FONT>
  <INPUT type="hidden" name="p" value="$toppostid">
</FORM>
EOF
		}
	}
}

1;
