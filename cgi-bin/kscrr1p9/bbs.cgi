#! /usr/local/bin/perl

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (掲示板本体)
#	
#	  mailto	kuzuha@kurumi.ne.jp
#	  webpage	http://kuzuha.tripod.co.jp/
#	
#	TABSIZE=4
#

###############################################################################
#  設定
###############################################################################

# 掲示板CGIのURL
$cgiurl = 'http://strange.kurumi.ne.jp/strangeworld/bbs.cgi';

# jcode.plのパス
$jcode = './jcode.pl';

# gzipのパス
#  (gzip圧縮転送機能を使用しない場合は空のままにしておきます)
$gzip = '/bin/gzip';

# gzip圧縮の初期値
#   0 : 圧縮しない
#   1 : 圧縮する
$gzipu = 0;

# CGIを設置するホストアドレス
$bbshost = 'strange.kurumi.ne.jp';

# ログファイル名
$logfilename = './bbs.log';

# カウンターのスタート日付
$countdate = '2000/01/01';

# カウンターのファイル名の先頭部分
$countfile = './count/count';

# カウンターの壊れにくさレベル
$countlevel = 2;

# リアルタイム参加者カウント用ファイル名
#  (リアルタイム参加者カウント機能使用しない場合は空のままにしておきます)
$cntfilename = './bbs.cnt';

# リアルタイム参加者カウント間隔 (秒)
# （最終ページビューからこの時間を超えた参加者は集計から除外されます）
$cntlimit = 300;

# メッセージの保存数
$logsave = 500;

# １画面に表示するメッセージの表示数
#  (1～メッセージの保存数)
$msgdisp = 20;

# サーバー設置場所と日本との時差
#   日本             : 0
#   グリニッジ標準時 : -9
#   アメリカ         : -14 (ワシントン)
#                    : -20 (ミッドウェー諸島)
#   ニュージーランド : 3
$difftime = 0;

# 掲示板の名前
$bbstitle = 'あやしいわーるど＠くずは';

# 背景色
$bgc    = '004040';

# テキスト色
$textc  = 'ffffff';

# リンク色
$linkc  = 'eeffee';
$vlinkc = 'dddddd';
$alinkc = 'ff0000';

# 題名の色
$subjc  = 'fffffe';

# 引用メッセージの色
# （色を変えない場合は空にしてください）
$qmsgc  = 'd1d1d1';

# フォロー投稿画面ボタンに表示する文字
$txtfollow = '■';

# 投稿者検索ボタンに表示する文字
$txtauthor = '★';

# スレッド表示ボタンに表示する文字
$txtthread = '◆';

# フォロー投稿時に相手の投稿者名に付加する文字
# （一般の掲示板では「さん」などを付けると良いでしょう）
$fsubj = '';

# 過去ログ保存用ディレクトリの名前
$oldlogfiledir = './log/';

# 過去ログの保存形式
#   0 : HTML形式 (トピック一覧、過去ログからの引用機能は使用できません)
#   1 : バイナリ形式
$oldlogfmt = 1;

# 過去ログからのフォロー投稿・投稿者検索
#   0 : 不可
#   1 : 可 (過去ログの保存形式がHTML形式の場合は設定できません)
$oldlogbtn = 1;

# 過去ログの保存方法
#   0 : 日毎
#   1 : 月毎
$oldlogsavesw = 0;

# 過去ログの保存日数
#  (過去ログの保存方法が日毎の場合にのみ有効)
$oldlogsaveday = 5;

# 過去ログの最大ファイルサイズ
$maxoldlogsize = 4 * 1024 * 1024;

# 二重書き込みチェック件数
$checkcount = 30;

# １メッセージの最大桁数
$maxmsgcol = 192;

# １メッセージの最大行数
$maxmsgline = 100;

# １メッセージの最大サイズ(byte)
$maxmsgsize = 8400;

# 連続投稿防止コード（必ず変更すること）
$protect_a = 12345678;	# 0以外の数字から始まる8桁の数字
$protect_b = 45;		# 0以外の数字から始まる2桁の数字

# 自動リンク機能の初期値
#   0 : 無効
#   1 : 有効
$autolink = 1;

# フォロー投稿画面表示
#   0 : 新規ウィンドウをオープンして表示
#   1 : 同一画面に表示
$followwin = 0;

# 投稿者IPアドレスの記録
#   0 : 記録しない
#   1 : 匿名プロクシのみ記録
#   2 : 全て記録
$iprec = 0;

# User Agent(ブラウザ名)の記録
#   0 : 無効
#   1 : 有効
$uarec = 0;

# 投稿者IPアドレスの表示
# （投稿者IPアドレスの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$ipprint = 0;

# User Agent(ブラウザ名)の表示
# （User Agentの記録が有効になっている必要があります）
#   0 : 無効
#   1 : 有効
$uaprint = 0;

# 同一IPアドレスからの投稿を拒否する時間 (秒)
# （投稿者IPアドレスの記録が有効になっている必要があります
#   0に設定すると一切制限しません）
$sptime = 20;

# Cookieによる投稿者／メールアドレス記憶機能の使用
#   0 : 無効
#   1 : 有効
$cookie = 0;

# 管理人の名前
$adminname = 'くずは';

# 管理人のメールアドレス
$adminmail = 'kuzuha@kurumi.ne.jp';

# 管理用パスワード（最初は空のままにしておいてください）
$adminpost = '';

# 管理モード移行用キーワード（必ず変更すること）
$adminkey = 'adminlogin';

# 広報室のURL
$infopage = 'http://kuzuha.tripod.co.jp/';

# データの受渡方法
$formmethod = 'post';


###############################################################################
#  システム用設定・変数（特に指示がない限り変更不可）
###############################################################################

$tmpl_msg = <<EOF;
<!-- \$postid -->
<FONT size="+1" color="#\$CC{'subj'}"><B>\$title</B></FONT>
　投稿者：<B>\$user</B>
　<FONT size="-1">投稿日：\$wdate\$btn</FONT>
<BLOCKQUOTE>
<PRE>
\$msg
</PRE>
\$envlist
</BLOCKQUOTE>
<HR>
<!-- -->
EOF

$S_pstime = 1;
$S_pltime = 3600;
$S_cexp = 7776000;
$S_alchk[0] = '';
$S_alchk[1] = 'checked';
$S_gzchk[0] = '';
$S_gzchk[1] = 'checked';


###############################################################################
#  時刻フォーマット変換
###############################################################################

sub getnowdate {
	
	( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdat )
		= localtime ( $_[0] );
	$year += 1900;
	$mon++;
	$nowdate = sprintf ( "%d/%02d/%02d(%s)%02d時%02d分%02d秒", 
	  $year, $mon, $mday, 
	  ( '日', '月', '火', '水', '木', '金', '土' )[$wday],
	  $hour, $min, $sec );
}


###############################################################################
#  フォームデータ取得
###############################################################################

sub getformdata {
	
	my ( $formbuf, $name, $value );
	
	if ( $ENV{'REQUEST_METHOD'} eq 'POST' ) {
		read ( STDIN, $formbuf[0], $ENV{'CONTENT_LENGTH'} );
	} else {
		$formbuf[0] = $ENV{'QUERY_STRING'};
	}
	
	if ( $formbuf[0] ) {
		
		&prterror ( '呼び出し元が不正です。' ) 
		  if ( $ENV{'HTTP_HOST'} && ! ( $ENV{'HTTP_HOST'} =~ /$bbshost/i ) );
		
		$referer = $ENV{'HTTP_REFERER'};
		$referer =~ s/\+/ /g;
		$referer =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack ( "C", hex ( $1 ) )/eg;
		
		foreach ( split ( /&/, $formbuf[0] ) ) {
			( $name, $value ) = split ( /=/ );
			$value =~ s/\+/ /g;
			$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack ( "C", hex ( $1 ) )/eg;
			$value =~ s/&/&amp;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
			$value =~ s/\r\n/\r/g;
			$value =~ s/\n/\r/g;
			$value =~ s/\r$//;
			$value =~ s/\,/\0/g;
			$FORM{$name} = $value;
		}
	}
}


###############################################################################
#  日本語文字コード変換
###############################################################################

sub jconv {
	
	if ( ( $FORM{'k'} ne 'あ' && $FORM{'v'} ) || $FORM{'j'} ) {
		require "$jcode";
		foreach ( keys %FORM ) {
			&jcode'convert ( *FORM{$_}, 'sjis' );
		}
	}
}


###############################################################################
#  環境変数取得
###############################################################################

sub getenv {
	
	if ( $uarec ) {
		$agent = $ENV{'HTTP_USER_AGENT'};
		$agent =~ s/</&lt;/g;
		$agent =~ s/>/&gt;/g;
		$agent =~ s/,/./g;
	}
	
	if ( !$iprec ) { return; }
	
	$addr = $ENV{'REMOTE_ADDR'};
	$host = $ENV{'REMOTE_HOST'};
	if ( $addr eq $host || !$host ) {
		$host = gethostbyaddr ( pack ( 'C4', split ( /\./, $addr ) ), 2 ) || $addr;
	}
	
	$proxyflg = 0;
	
	if ( $ENV{'HTTP_CACHE_CONTROL'} )			{ $proxyflg = 1; }
	if ( $ENV{'HTTP_CACHE_INFO'} )				{ $proxyflg += 2; }
	if ( $ENV{'HTTP_CLIENT_IP'} )				{ $proxyflg += 4; }
	if ( $ENV{'HTTP_FORWARDED'} )				{ $proxyflg += 8; }
	if ( $ENV{'HTTP_FROM'} )					{ $proxyflg += 16; }
	if ( $ENV{'HTTP_PROXY_AUTHORIZATION'} )		{ $proxyflg += 32; }
	if ( $ENV{'HTTP_PROXY_CONNECTION'} )		{ $proxyflg += 64; }
	if ( $ENV{'HTTP_SP_HOST'} )					{ $proxyflg += 128; }
	if ( $ENV{'HTTP_VIA'} )						{ $proxyflg += 256; }
	if ( $ENV{'HTTP_X_FORWARDED_FOR'} )			{ $proxyflg += 512; }
	if ( $ENV{'HTTP_X_LOCKING'} )				{ $proxyflg += 1024; }
	if ( $agent =~ /cache|delegate|gateway|httpd|proxy|squid|www|via/i ) {
		$proxyflg += 2048;
	}
	if ( $host =~ /cache|^dns|dummy|^ns|firewall|gate|keep|mail|^news|pop|proxy|smtp|w3|^web|www/i ) {
		$proxyflg += 4096;
	}
	if ( $host eq $addr ) {
		$proxyflg += 8192;
	}
	
	$realaddr = '';
	$realhost = '';
	if ( $proxyflg > 0 ) {
		
		if ( $ENV{'HTTP_X_FORWARDED_FOR'} =~
		  s/^(\d+)\.(\d+)\.(\d+)\.(\d+).*/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_FORWARDED'} =~ 
		  s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_VIA'} =~
		  s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_CLIENT_IP'} =~
		  s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_SP_HOST'} =~
		  s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ ) {
			$realaddr = "$1.$2.$3.$4";
		} elsif ( $ENV{'HTTP_FORWARDED'} =~ s/.*\sfor\s(.+)/$1/ ) {
			$realhost = "$1";
		} elsif ( $ENV{'HTTP_FROM'} =~ s/\-\@(.+)/$1/ ) {
			$realhost = "$1";
		}
		
		if ( !$realaddr && $realhost ) {
			$realpackaddr = gethostbyname ( $realhost );
			( $a, $b, $c, $d ) = unpack ( 'C4', $realpackaddr );
			$realaddr = "$a.$b.$c.$d";
		}
		
		if ( $realaddr && $iprec != 2 ) {
			$host = '(leak)';
		}
	} else {
		$host = '(none)' if ( $iprec != 2 );
	}
}


###############################################################################
#  文字列のエンコード
###############################################################################

sub escstring {
	
	my ( $srcstr ) = $_[0];
	
	$srcstr =~ s/([^a-zA-Z0-9\s])/sprintf ( "%%%lx", ( unpack ( "C", $1 ) ) )/eg;
	$srcstr =~ s/ /\+/g;
	
	return $srcstr;
}


###############################################################################
#  メッセージ読み込み
###############################################################################

sub loadmessage {
	
	my $openlog;
	
	if ( !$FORM{'ff'} ) {
		$openlog = $logfilename;
	} else {
		$FORM{'ff'} =~ /^([\w.]*)$/;
		$openlog = "$oldlogfiledir/$1";
	}
	
	open ( READLOG, "$openlog" ) || &prterror ( 'メッセージ読み込みに失敗しました' );
	eval 'flock ( READLOG, 1 )';
	seek ( READLOG, 0, 0 );
	@logdata = <READLOG>;
	eval 'flock ( READLOG, 8 )';
	close ( READLOG );
}


###############################################################################
#  メッセージ１件取得
###############################################################################

sub getmessage {
	
	( $ndate, $postid, $protect, $thread, $phost, $agent, $user, $mail, $title, $msg )
	  = split ( /\,/, $_[0] );
	$msg =~ s/\n$//;
	$title =~ s/\0/\,/g;
	$mail =~ s/\0/\,/g;
	$user =~ s/\0/\,/g;
	$msg =~ s/\0/\,/g;
	$wdate = &getnowdate ( $ndate );
}


###############################################################################
#  メッセージ１件出力
###############################################################################

sub prtmessage {
	
	my $mode = $_[0];	# 0 : 掲示板 1 : 過去ログ(ボタン表示あり) 2 : 過去ログ(ボタン表示なし) 3 : 検索窓
	my $tlog = $_[1];
	my ( $tag, $refdate, $prtmessage, $btn, $btnfollow, $btnauthor, $btnthread, $newwin,
	  $envlist, $envaddr, $envua, $envbr );
	
	# 「参考」
	if ( $mode == 0 || $mode == 3 ) {
		$msg =~ s/<A href=\"m=f\&s=(\d+)\&r=(\S+)\">(.*)<\/A>/<A href=\"$cgiurl\?m=f\&c=$FORM{'c'}&s=$1\&r=$2\">$3<\/A>/i;
		$msg =~ s/<A href=\"mode=follow\&search=(\d+)\&ref=(\S+)\">(.*)<\/A>/<A href=\"$cgiurl\?m=f\&c=$FORM{'c'}&s=$1\&r=$2\">$3<\/A>/i;
	} else {
		$msg =~ s/<A href=\"m=f\&s=(\d+)\&r=(\S+)\">(.*)<\/A>/<A href=\"#$1\">$3<\/A>/i;
		$msg =~ s/<A href=\"mode=follow\&search=(\d+)\&ref=(\S+)\">(.*)<\/A>/<A href=\"#$1\">$3<\/A>/i;
	}
	
	if ( $mode == 0 || $mode == 3 || ( $mode == 1 && $oldlogbtn && $oldlogfmt ) ) {
		
		if ( !$followwin ) { $newwin = " target=\"link\""; }
		else { $newwin = '' };
		
		# フォロー投稿ボタン
		$btnfollow = "<A href=\"$cgiurl\?m=f\&u=".
		  &escstring ( $FORM{'u'} ) .
		  "&d=$FORM{'d'}&p=$toppostid&s=$postid\&c=$FORM{'c'}";
		if ( !$mode ) {
			$btnfollow .= "\"";
		} elsif ( $mode == 3 ) {
			$btnfollow .= "&ac=1\"";
		} else {
			$btnfollow .= "&ff=$tlog\"";
		}
		$btnfollow .= "$newwin>$txtfollow</A>　\n";
		
		# 投稿者検索ボタン
		$btnauthor = "<A href=\"$cgiurl\?m\=s\&s\=".
		  &escstring ( $user ) .
		  "\&c=$FORM{'c'}\"".
		  " target=\"link\">$txtauthor</A>　\n";
		
		# スレッド表示ボタン
		if ( $thread ) {
			$btnthread = "<A href=\"$cgiurl\?m\=t\&c=$FORM{'c'}".
			  "\&s\=$thread\" target=\"link\">$txtthread</A>\n";
		} else {
			$btnthread = '';
		}
		
		$btn = "　\n  $btnfollow  $btnauthor  $btnthread";
	} else {
		$btn = '';
	}
	
	# メールアドレス
	if ( $mail ) {
		$user = "<A href=\"mailto\:$mail\">$user<\/A>";
	}
	
	# 引用色変更
	if ( !$mode ) {
		$msg =~ s/(^|\r)(&gt;[^\r]*)/$1<FONT color=\"#$CC{'qmsgc'}\">$2<\/FONT>/g;
		$msg =~ s/<\/FONT>\r<FONT color=\"#$CC{'qmsgc'}\">/\r/g;
	} elsif ( $mode >= 1 && $qmsgc ) {
		$msg =~ s/(^|\r)(&gt;[^\r]*)/$1<FONT color=\"#$qmsgc\">$2<\/FONT>/g;
		$msg =~ s/<\/FONT>\r<FONT color=\"#$qmsgc\">/\r/g;
	}
	
	# 環境変数
	if ( $ipprint ) {
		$envaddr = $phost;
	} else {
		$envaddr = '';
	}
	if ( $uaprint ) {
		$envua = $agent;
	} else {
		$envua = '';
	}
	if ( $ipprint && $uaprint ) {
		$envbr = '<BR>';
	}
	if ( $envaddr || $envua ) {
		$envlist = qq!<FONT size="-1"><I>$envaddr$envbr$envua</I></FONT>!;
	} else {
		$envlist = '';
	}
	
	# メッセージ表示内容定義
	$prtmessage = qq(<A name="$postid"></A>\n$tmpl_msg);
	$prtmessage =~ s/(\$[A-Za-z0-9\'\{\}]+)/$1/eeg;
	
	return $prtmessage;
}


###############################################################################
#  こわれにくいカウンター処理
###############################################################################

sub counter {
	
	my ( @count, @filenumber, @sortedcount, $maxcount, $mincount );
	
	for ( $i = 0 ; $i < $countlevel ; $i++ ) {
		open ( IN, "$countfile$i.dat" );
		$count[$i] = <IN>;
		$filenumber{$count[$i]} = $i;
		close ( IN );
	}
	
	@sortedcount = sort { $a <=> $b; } @count;
	$maxcount = $sortedcount[$countlevel-1];
	$mincount = $sortedcount[0];
	
	$maxcount++;
	
	if ( open ( OUT, ">$countfile$filenumber{$mincount}.dat" ) ) {
		print OUT $maxcount;
		close ( OUT );
		return $maxcount;
	} else {
		return '<FONT color="red">カウンターファイルの出力エラーです</FONT>';
	}
}


###############################################################################
#  参加者カウント
###############################################################################

sub mbrcount {
	
	my ( @hostbin, @ukey, @cntdata, $mbrcount, $cuser, $ctime, $cadd );
	
	if ( $cntfilename ) {
		undef @cntdata;
		$mbrcount = 0;
		@hostbin = split ( /\./, $ENV{'REMOTE_ADDR'} );
		for ( $i = 0 ; $i < 4 ; $i++ ) {
			$hostbin[$i] = vec ( pack ( 'C4', $hostbin[$i] ), 0, 8 );
		}
		$ukey[0] = $hostbin[0] + $hostbin[1] + $hostbin[2] + $hostbin[3];
		$ukey[1] = $hostbin[0] ^ $hostbin[1] & $hostbin[2] ^ $hostbin[3];
		$ukey[2] = $ukey[0] * $ukey[1];
		
		if ( open ( UCNT, $cntfilename ) ) {
			eval 'flock ( UCNT, 1 )';
			seek ( UCNT, 0, 0 );
			@cntdata = <UCNT>;
			eval 'flock ( UCNT, 8 )';
			close ( UCNT );
			
			$cadd = 0;
			for ( $i = 0 ; $i < @cntdata ; $i++ ) {
				( $cuser, $ctime ) = split ( /\,/, $cntdata[$i] );
				chomp ( $ctime );
				if ( $cuser eq $ukey[2] ) {
					$cntdata[$i] = "$ukey[2],$nowtime\n";
					$cadd = 1;
					$mbrcount++;
				} elsif ( ( $ctime + $cntlimit ) < $nowtime ) {
					# 除外
					$cntdata[$i] = '';
				} else {
					$mbrcount++;
				}
			}
			if ( !$cadd ) {
				push ( @cntdata, "$ukey[2],$nowtime\n" );
				$mbrcount++;
			}
		} else {
			push ( @cntdata, "$ukey[2],$nowtime\n" );
			$mbrcount++;
		}
		
		open ( UCNT, ">>$cntfilename" ) || &prterror ( '参加者カウントファイルの書き込みに失敗しました。' );
		eval 'flock ( UCNT, 2 )';
		truncate ( UCNT, 0 );
		seek ( UCNT, 0, 0 );
		print UCNT @cntdata;
		close ( UCNT );
		
		return "　現在の参加者 : $mbrcount名 ($cntlimit秒以内)";
	} else {
		return;
	}
}


###############################################################################
#  HTMLヘッダ部分表示
###############################################################################

sub prthtmlhead {
	
	my $headtitle = $_[0];
	
	# ヘッダ出力
	print "Content-type: text/html\n";
	if ( $gzip && $gzipu && ( $ENV{'HTTP_ACCEPT_ENCODING'} =~ /gzip/ ) ) {
		print "Content-encoding: gzip\n\n";
		open ( STDOUT, "| $gzip -1 -c" );
		print "<!-- gzip enable -->";
	} else {
		print "\n<!-- gzip disable -->";
	}
	
	print <<EOF;
<HTML>
<HEAD>
<TITLE>$headtitle</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
</HEAD>

$body
EOF
}


###############################################################################
#  エラーメッセージ表示
###############################################################################

sub prterror {
	
	my $error = $_[0];
	
	print <<EOF;
Content-type: text/html

<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<META http-equiv="Pragma" content="no-cache">
<TITLE>$bbstitle (エラー)</TITLE>
</HEAD>
$body
<H3>$error</H3>
</BODY>
</HTML>
EOF
	exit;
}


###############################################################################
#  フォロー画面表示
###############################################################################

sub prtfollow {
	
	my $retry = $_[0];
	my $success = 0;
	my $formmsg;
	
	&loadmessage;
	
	&prterror ( 'パラメータがありません。' ) if ( !$FORM{'s'} );
	
	&prthtmlhead ( "$bbstitle フォロー投稿" );
	print "<HR>\n";
	
	foreach ( 0 .. @logdata - 1 ) {
		&getmessage ( $logdata[$_] );
		if ( $postid eq $FORM{'s'} ) {
			$success = 1;
			last;
		}
		$i++;
	}
	
	if ( !$success ) {
		print "<H3>指定されたメッセージが見つかりません。</H3></BODY></HTML>";
		exit;
	}
	
	if ( !$retry ) {
		$formmsg = $msg;
		$formmsg =~ s/&gt; &gt;.*?\r//g;
		$formmsg =~ s/<A href=\"m=f\S+\">.*<\/A>//i;
		$formmsg =~ s/<A href=\S+ target=\"link\">(\S+)<\/A>/$1/ig;
		$formmsg =~ s/\r/\r&gt; /g;
		$formmsg = "&gt; $formmsg\r";
		$formmsg =~ s/\r&gt;\s+\r/\r/g;
		$formmsg =~ s/\r&gt;\s+\r$/\r/g;
	} else {
		$formmsg = "$FORM{'v'}";
		$formmsg =~ s/<A href=\"m=f\S+\">.*<\/A>//i;
	}
	
	print &prtmessage ( 0, '' );
	
	if ( !$thread ) {
		$thread = $postid;
	}
	
	if ( $user =~ /\<A\shref=\"mailto\:.*\"\>(.*)\<\/A\>/ ) {
		$user = $1;
	}
	print "フォロー記事投稿<BR>\n";
	&prtform ( "＞$user$fsubj", "$formmsg\r", '' );
	
	print <<EOF;
  <BR>
  <INPUT type="hidden" name="d" value="$FORM{'d'}">
  <FONT size="-1">URL自動リンク <INPUT type="checkbox" name="a" value="checked" $S_alchk[$autolink]></FONT><BR>
  <INPUT type="hidden" name="g" value="checked" $S_gzchk[$gzipu]>
  <INPUT type="hidden" name="p" value="$FORM{'p'}">
  <INPUT type="hidden" name="s" value="$FORM{'s'}">
  <INPUT type="hidden" name="h" value="$thread">
  <INPUT type="hidden" name="f" value="$postid:$wdate">
  <INPUT type="hidden" name="ac" value="$FORM{'ac'}">
  <HR>
</FORM>
</BODY>
</HTML>
EOF
	
	exit;
}


###############################################################################
#  パスワードチェック
###############################################################################

sub chkpasswd {
	
	my $slen;
	
	if ( $adminpost =~ /^\$1\$/ ) {
		$slen = 5;
	} else {
		$slen = 2;
	}
	
	if ( crypt ( $FORM{'u'}, substr ( $adminpost, 0, $slen ) ) eq $adminpost ) {
		return 1;
	} else {
		return 0;
	}
}


###############################################################################
#  メッセージチェック
###############################################################################

sub chkmessage {
	
	my ( @hostbin, $admincheck, $adminfname );
	
	if ( $referer && ! ( $referer =~ /$cgiurl/i ) ) {
		&chkerror ( "投稿画面のＵＲＬが<BR>$cgiurl<BR>" .
		  '以外からの投稿はできません。',  3 );
	}
	
	$i = 0;
	foreach ( split ( /\r/, $FORM{'v'} ) ) {
		if ( length ( $_ ) > $maxmsgcol ) {
			$i++;
		}
	}
	if ( $i != 0 ) { &chkerror ( '投稿内容の桁数が大きすぎます。', 10 ); }
	
	if ( ( $FORM{'v'} =~ tr/\r/\r/ ) > ( $maxmsgline - 1 ) ) {
		&chkerror ( '投稿内容の行数が大きすぎます。', 11 );
	}
	
	if ( length ( $FORM{'v'} ) > $maxmsgsize ) {
		&chkerror ( '投稿内容が大きすぎます。', 12 );
	}
	
	if ( $FORM{'pc'} ) {
		@hostbin = split ( /\./, $ENV{'REMOTE_ADDR'} );
		for ( $i = 0 ; $i < 4 ; $i++ ) {
			$hostbin[$i] = vec ( pack ( 'C4', $hostbin[$i] ), 0, 8 );
		}
		$protect_c = $hostbin[0] ^ $hostbin[1] ^ $hostbin[2] ^ $hostbin[3];
		$pcheck = ( $FORM{'pc'} - $protect_c ) / $protect_b - $protect_a;
		&getnowdate ( $pcheck );
		if ( ( $sec  < 0 ) || ( $sec  > 60 ) || 
		  ( $min  < 0 ) || ( $min  > 60 ) ||
		  ( $hour < 0 ) || ( $hour > 24 ) ) {
			&chkerror ( '', 32 );
		}
		if ( ( $nowtime - $pcheck ) < $S_pstime ) {
			&chkerror ( 'もう一度やり直して下さい。', 30 );
		}
		if ( ( $nowtime - $pcheck ) > $S_pltime ) {
			&chkerror ( '', 31 );
			if ( $FORM{'f'} ) {
				&prtfollow ( 1 );
			} else {
				&prtmain ( $FORM{'t'}, $FORM{'v'}, $FORM{'l'} );
			}
			exit;
		}
	} else {
		&chkerror ( 'フォームデータの一部に欠落があります。もう一度やり直して下さい。', 33 );
	}
	
	if ( $FORM{'i'} =~ / /i ) {
		$FORM{'i'} = '';
	}
	if ( $FORM{'i'} ) {
		if ( ! ( $FORM{'i'} =~ /.*\@.*\..*/ ) ) {
			&chkerror ( 'メールアドレスが正しく入力されていません。', 20 );
		} elsif ( $FORM{'i'} =~ /,/ ) {
			&chkerror ( 'メールアドレスは複数指定できません。', 21 );
		}
	}
	
	if ( !$FORM{'t'} ) {
		$FORM{'t'} = ' ';
	}
	
	if ( !$FORM{'u'} ) {
		$FORM{'u'} = '　';
	} else {
		if ( &chkpasswd ) {
			if ( $FORM{'v'} =~ /^$adminkey/ ) {
				require 'sub/bbsadmin.pl';
				&adminmain;
				exit;
			} else {
				$FORM{'u'} = $adminname;
				$FORM{'i'} = $adminmail;
			}
		} elsif ( $FORM{'u'} eq $adminpost ) {
			$FORM{'u'} = "$adminname（ハカー）";
		} else {
			$adminfname = quotemeta $adminname;
			if ( $FORM{'u'} =~ /$adminfname/i ) {
				$admincheck = $FORM{'u'};
				$admincheck =~ s/ //g;
				$admincheck =~ s/　//g;
				$admincheck =~ s/_//g;
				if ( $admincheck eq $adminname ) {
					$FORM{'u'} =~ s/$adminfname/$adminname（騙り）/;
				}
			}
		}
	}
	
	if ( $autolink ) {
		$FORM{'v'} =~ s#((https?|ftp|gopher|telnet|whois|news)://(=[\x21-\xfc]+|[\x21-\x7e])+)#<A href="$1" target="link">$1</A>#ig;
	}
	
	if ( $FORM{'l'} =~ /\s+/ || !$FORM{'l'} ) {
		$FORM{'l'} = '';
	} else {
		$FORM{'l'} =~ s/http:\/\/http:\/\//http:\/\//;
		$FORM{'v'} .= "\r\r<A href=\"$FORM{'l'}\" target=\"link\">$FORM{'l'}</A>";
	}
	if ( $FORM{'f'} ) {
		( $i, $j ) = split ( /:/, $FORM{'f'} );
		$FORM{'v'} .= "\r\r<A href=\"m=f\&s=$i\&r=$j\">参考：$j</A>";
	}
}


###############################################################################
#  メッセージチェックエラー処理
###############################################################################

sub chkerror {
	
	my $errstr = $_[0];
	$posterr = $_[1];
	
	&prterror ( $errstr ) if ( $errstr );
}


###############################################################################
#  メッセージ登録
###############################################################################

sub putmessage {
	
	my $oldlogext;
	
	open ( FLOG, "+<$logfilename" ) || &prterror ( 'メッセージ読み込みに失敗しました' );
	eval 'flock ( FLOG, 2 )';
	seek ( FLOG, 0, 0 );
	@logdata = <FLOG>;
	
	$i = 0;
	$posterr = 0;
	while ( $logdata[$i] && !$posterr ) {
		@items = split ( /\,/, $logdata[$i] );
		$items[9] =~ s/\n$//;
		$posterr = 1 if ( $i < $checkcount && $FORM{'v'} eq $items[9] );
		$posterr = 2 if ( $FORM{'pc'} eq $items[2] );
		$posterr = 2 if ( $host && ( $host eq $items[4] ) && ( $nowtime < ( $items[0] + $sptime ) ) );
		$i++;
	}
	
	if ( !$posterr ) {
		
		@items = split ( /\,/, $logdata[0] );
		$newpostid = $items[1] + 1;
		$msgdata = "$nowtime,$newpostid,$FORM{'pc'},$FORM{'h'},$host,$agent,$FORM{'u'},$FORM{'i'},$FORM{'t'},$FORM{'v'}\n";
		
		@logdata = @logdata[0 .. $logsave - 2] if ( @logdata >= $logsave );
		unshift ( @logdata, $msgdata );
		
		$oldstream = select ( FLOG );
		$| = 1;
		seek ( FLOG, 0, 0 );
		truncate ( FLOG, 0 );
		print FLOG @logdata;
		eval 'flock ( FLOG, 8 )';
		close ( FLOG );
		select ( $oldstream );
		
		&getnowdate ( $nowtime );
		
		# 過去ログ出力
		if ( $oldlogfiledir ) {
			
			if ( !$oldlogfmt ) {
				$oldlogext = 'html';
			} else {
				$oldlogext = 'dat';
			}
			
			if ( !$oldlogsavesw ) {
				$oldlogfilename = sprintf ( "%s/%d%02d%02d.$oldlogext",
				  $oldlogfiledir, $year, $mon, $mday );
			} else {
				$oldlogfilename = sprintf ( "%s%d%02d.$oldlogext",
				  $oldlogfiledir, $year, $mon );
			}
			
			open ( CLOG, ">>$oldlogfilename" ) || &prterror ( '過去ログ出力に失敗しました' );
			eval 'flock ( CLOG, 2 )';
			
			$oldstream = select ( CLOG );
			$| = 1;
			
			if ( !$oldlogfmt ) {
				if ( -z CLOG ) {
					print CLOG <<EOF;
<HTML>
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<TITLE>$bbstitle</TITLE>
</HEAD>
<BODY bgcolor="#$bgc" text="#$textc" link="#$linkc" vlink="#$vlinkc" alink="#$alinkc">
<HR>
EOF
				}
				
				&getmessage ( $msgdata );
				
				print CLOG &prtmessage ( 1, '' );
				
			} else {
				print CLOG $msgdata;
			}
			
			eval 'flock ( CLOG, 8 )';
			close ( CLOG );
			
			select ( $oldstream );
			
			chmod 0400, $logfilename if ( ( -s $oldlogfilename ) > $maxoldlogsize );
			
			&getnowdate ( time - $difftime - $oldlogsaveday * 60 * 60 * 24 );
			$oldlogfilename = sprintf (  "%s/%d%02d%02d.$oldlogext",
			  $oldlogfiledir, $year, $mon, $mday );
			unlink $oldlogfilename;
			
			&putcookie ( 0 ) if ( $cookie );
		}
		
	} else {
		eval 'flock ( FLOG, 8 )';
		close ( FLOG );
		
		if ( $posterr == 2 ) {
			&chkerror ( '', $posterr );
			if ( $FORM{'f'} ) {
				&prtfollow ( 1 );
			} else {
				&prtmain ( $FORM{'t'}, $FORM{'v'}, $FORM{'l'} );
			}
			exit;
		}
	}
}


###############################################################################
#  Cookie取得
###############################################################################

sub getcookie {
	
	if ( $ENV{'HTTP_COOKIE'} ) {
		$ENV{'HTTP_COOKIE'} =~ /^c\=u\=(.*)\&m\=(.*)&c\=(.*)$/;
		$FORM{'u'} = $1 if ( $1 && !$FORM{'u'} );
		$FORM{'i'} = $2 if ( $2 && !$FORM{'i'} );
		$FORM{'c'} = $3 if ( ( length ( $3 ) == 3 ) || ( length ( $3 ) == 33 ) );
		$FORM{'c'} =~ s/;$//;
		$FORM{'u'} =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack ( "C", hex ( $1 ) )/eg;
		$FORM{'i'} =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack ( "C", hex ( $1 ) )/eg;
	}
}


###############################################################################
#  Cookie送信
###############################################################################

sub putcookie {
	
	my ( $cuser, $cmail, @ctime, $cmday, $cmon, $cdate );
	my $cexpdif = $_[0];
	
	$cuser = &escstring ( $FORM{'u'} );
	$cmail = &escstring ( $FORM{'i'} );
	
	( @ctime ) = gmtime ( time + $S_cexp - $cexpdif );
	$cmday = ( 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' )[$ctime[6]];
	$cmon = ( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' )[$ctime[4]];
	$cdate = sprintf ( "%s, %02d\-%s\-%04d %02d:%02d:%02d GMT",
	  $cmday, $ctime[3], $cmon, $ctime[5] + 1900, $ctime[2], $ctime[1], $ctime[0] );
	print "Set-Cookie: c=u=$cuser&m=$cmail&c=$FORM{'c'}; expires=$cdate; path=/\n";
}


###############################################################################
#  プロテクトコード生成
###############################################################################

sub pcode {
	
	my ( @hostbin, @pkey, @pkeystr, @apkey );
	srand ( time | $$ );
	
	#$nowtime = time - $difftime * 60 * 60;
	@hostbin = split ( /\./, $ENV{'REMOTE_ADDR'} );
	for ( $i = 0 ; $i < 4 ; $i++ ) {
		$hostbin[$i] = vec ( pack ( 'C4', $hostbin[$i] ), 0, 8 );
	}
	$protect_c = $hostbin[0] ^ $hostbin[1] ^ $hostbin[2] ^ $hostbin[3];
	$pkey[0] = ( $nowtime + $protect_a ) * $protect_b + $protect_c;
	$pkey[1] = $pkey[0] - int ( rand ( 64 ) );
	$pkey[2] = $pkey[1] + int ( rand ( 128 ) );
	
	$pkeystr[0] = "\n  <INPUT type=\"hidden\" name=\"pc\" value=\"$pkey[0]\">\n";
	$pkeystr[1] = "  <!--\n  <INPUT type=\"hidden\" name=\"pc\" value=\"$pkey[1]\">\n  -->";
	$pkeystr[2] = "  <!--\n  <INPUT type=\"hidden\" name=\"pc\" value=\"$pkey[2]\">\n  -->";
	
	push ( @apkey, splice ( @pkeystr, rand ( @pkeystr ), 1 ) ) while @pkeystr;
	@pkeystr = @apkey;
	
	return "$pkeystr[0]$pkeystr[1]$pkeystr[2]";
}


###############################################################################
#  フォーム部分表示
###############################################################################

sub prtform {
	
	my $dtitle = $_[0];
	my $dmsg = $_[1];
	my $dlink = $_[2];
	my ( $bbslink, $gzipchk, $counter, $mbrcount );
	
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
  <P><FONT size="-1">表\示件数 <INPUT size="6" type="text" name="d" value="$FORM{'d'}">
$gzipchk
  　<FONT size="-1">URL自動リンク <INPUT type="checkbox" name="a" value="checked" $S_alchk[$autolink]></FONT>
  　<INPUT type="submit" name="setup" value="その他の設定"></FONT></P>
  <FONT size="-1">$countdate から $counter（こわれにくさレベル$countlevel）$mbrcount</FONT>
  <HR>
  <FONT size="-1">| 
  <A href="$infopage">広報室</A> | 
  <A href="$cgiurl?m=g&c=$FORM{'c'}">最近の過去ログ</A> |
  $bbslink |
  </FONT>
  <HR>
  <FONT size="-1">$txtfollow : フォロー投稿画面表\示 　 $txtauthor : 投稿者検索表\示 　 $txtthread : スレッド表\示
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
<FORM method="$formmethod" action="$cgiurl">
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
  <INPUT size="70" type="text" name="l" maxlength="255" value="$dlink">
  $ptext
  <INPUT type="hidden" name="k" value="あ">
  <INPUT type="hidden" name="c" value="$FORM{'c'}">
EOF
		
		if ( $FORM{'m'} ne 'f' && !$FORM{'f'} ) {
			print <<EOF;
  <P><FONT size="-1">表\示件数 <INPUT size="6" type="text" name="d" value="$FORM{'d'}">
  $gzipchk
  　<FONT size="-1">URL自動リンク <INPUT type="checkbox" name="a" value="checked" $S_alchk[$autolink]></FONT>
  　<INPUT type="submit" name="setup" value="その他の設定"></FONT></P>
  <FONT size="-1">$countdate から $counter（こわれにくさレベル$countlevel）$mbrcount</FONT>
  <HR>
  <FONT size="-1">| 
  <A href="$infopage">広報室</A> | 
  <A href="$cgiurl?m=g&c=$FORM{'c'}">最近の過去ログ</A> |
  $bbslink |
  </FONT>
  <HR>
  <FONT size="-1">$txtfollow : フォロー投稿画面表\示 　 $txtauthor : 投稿者検索表\示 　 $txtthread : スレッド表\示
  　　　最大登録件数 : $logsave件</FONT>
  <HR>
  <FONT size="-1"><INPUT type="submit" name="reload" value="リロード"></FONT>
  <INPUT type="hidden" name="p" value="$toppostid">
</FORM>
EOF
		}
	}
}


###############################################################################
#  画面表示
###############################################################################

sub prtmain {
	
	my ( $prtmessage, $dispcount, @pkeystr, $msgmore, $msgnext, $cntnext );
	my $dtitle = $_[0];
	my $dmsg = $_[1];
	my $dlink = $_[2];
	
	&loadmessage;
	
	$prtmessage = '';
	
	# 最新のPOSTIDを取得（０件リロード用）
	$logdata[0] =~ /^.*,(.*),.*,.*,.*,.*,.*,.*,.*,.*/;
	$toppostid = $1;
	
	# メッセージ表示件数設定
	if ( $FORM{'d'} == 0 ) {
		$dispcount = $toppostid - $FORM{'p'};
		$cntnext = $msgdisp;
	} else {
		$dispcount = $FORM{'d'};
		$cntnext = $FORM{'d'};
	}
	
	# 表示メッセージ作成
	$msgtop = $bmsg + $dispcount;
	$msgtop = @logdata if ( $msgtop > @logdata );
	$j = 0;
	
	if ( $FORM{'d'} == 0 && $reltype ) {
		for ( $i = $msgtop - 1 ; $i >= $bmsg ; $i-- ) {
			&getmessage ( $logdata[$i] );
			$prtmessage .= &prtmessage ( 0, '' );
			$j++
		}
	} else {
		for ( $i = $bmsg ; $i < $msgtop ; $i++ ) {
			&getmessage ( $logdata[$i] );
			$prtmessage .= &prtmessage ( 0, '' );
			$j++
		}
	}
	$bmsg++;
	if ( $j > 0 ) {
		$msgmore = "以上は、現在登録されている新着順$bmsg番目から$msgtop番目までの記事です。"
	} else {
		$msgmore = '未読メッセージはありません。';
	}
	if ( $logdata[$msgtop] && $j > 0 ) {
		$msgnext = <<EOF;
<TABLE>
  <TR>
    <TD>
      <FORM method="$formmethod" action="$cgiurl">
        <INPUT type="hidden" name="m" value="n">
        <INPUT type="hidden" name="b" value="$msgtop">
        <INPUT type="hidden" name="u" value="$FORM{'u'}">
        <INPUT type="hidden" name="d" value="$cntnext">
        <INPUT type="hidden" name="c" value="$FORM{'c'}">
        <INPUT type="submit" name="pnext" value="次のページ">
      </FORM>
    </TD>
    <TD>
      <FORM method="$formmethod" action="$cgiurl">
        <INPUT type="hidden" name="u" value="$FORM{'u'}">
        <INPUT type="hidden" name="p" value="$toppostid">
        <INPUT type="hidden" name="d" value="$FORM{'d'}">
        <INPUT type="hidden" name="c" value="$FORM{'c'}">
        <INPUT type="submit" name="reload" value="リロード">
      </FORM>
    </TD>
  </TR>
</TABLE>
EOF
	} else {
		$msgmore .= 'これ以下の記事はありません。';
		$msgnext = '';
	}
	
	# メイン出力
	&prthtmlhead ( "$bbstitle" );
	print <<EOF;
<P>
  <B><FONT size="+1">$bbstitle</FONT></B>
  <FONT size="-1"><A href="$infopage">広報室</A></FONT>
  <FONT size="-1"><A href="mailto:$adminmail">連絡先</A></FONT>
</P>
EOF
	
	&prtform ( $dtitle, $dmsg, $dlink );
	
	print <<EOF;
<HR>

$prtmessage

<P><I><FONT size="-1">$msgmore</FONT></I></P>

$msgnext
<HR>

<P align="right">
<FONT size="-1"><A href="http://kuzuha.tripod.co.jp/">くずはすくりぷと</A> Rev.0.1 Preview 9</FONT>
</P>

</BODY>
</HTML>
EOF
}


###############################################################################
#  個人用設定反映
###############################################################################

sub refcustom {
	
	if ( $FORM{'c'} ) {
		if ( length ( $FORM{'c'} ) == 33  ) {
			$FORM{'c'} =~ /^(\w\w\w\w\w\w)(\w\w\w\w\w\w)(\w\w\w\w\w\w)(\w\w\w\w\w\w)(\w\w\w\w\w\w)(\w)(\w)(\w)$/;
			$CC{'text'} = $1;
			$CC{'bg'} = $2;
			$CC{'link'} = $3;
			$CC{'vlink'} = $4;
			$CC{'qmsgc'} = $5;
			$CC{'subj'} = $CC{'text'};
			$i = hex ( $6 );
			$j = hex ( $7 );	# 予備
			$k = hex ( $8 );	# 予備
		} elsif ( length ( $FORM{'c'} ) == 3  ) {
			$FORM{'c'} =~ /^(\w)(\w)(\w)$/;
			$CC{'text'} = $textc;
			$CC{'bg'} = $bgc;
			$CC{'link'} = $linkc;
			$CC{'vlink'} = $vlinkc;
			$CC{'qmsgc'} = $qmsgc;
			$CC{'subj'} = $subjc;
			$i = hex ( $1 );
			$j = hex ( $2 );	# 予備
			$k = hex ( $3 );	# 予備
		}
		$gzipu = int ( $i / 8 );
		$reltype = int ( $i % 8 / 4 );
		$followwin = int ( $i % 8 % 4 / 2 );
		$autolink = ( $i % 8 % 4 % 2 );
		if ( $FORM{'m'} eq 'p' || $FORM{'m'} eq 'op' ) {
			if ( $FORM{'a'} ) { $autolink = 1; } else { $autolink = 0; }
			if ( $FORM{'g'} ) { $gzipu = 1; } else { $gzipu = 0; }
		}
	} else {
		$CC{'text'} = $textc;
		$CC{'bg'} = $bgc;
		$CC{'link'} = $linkc;
		$CC{'vlink'} = $vlinkc;
		$CC{'qmsgc'} = $qmsgc;
		$CC{'subj'} = $subjc;
		$gzipu = $FORM{'g'} if ( $FORM{'m'} eq 'g' );
	}
	$i = sprintf ( "%x", $autolink + $followwin * 2 + $reltype * 4 + $gzipu * 8 );
	$j = 0;
	$k = 0;
	
	if ( 
	  ( $CC{'text'} eq $textc ) &&
	  ( $CC{'bg'} eq $bgc ) &&
	  ( $CC{'link'} eq $linkc ) &&
	  ( $CC{'vlink'} eq $vlinkc ) &&
	  ( $CC{'qmsgc'} eq $qmsgc ) &&
	  ( $CC{'subj'} eq $subjc ) ) {
		$FORM{'c'} = "$i$j$k";
	} else {
		$FORM{'c'} = "$CC{'text'}$CC{'bg'}$CC{'link'}$CC{'vlink'}$CC{'qmsgc'}$i$j$k";
	}
}


###############################################################################
#  メイン
###############################################################################

&getformdata;
&jconv;
&getenv;
&getcookie if ( $cookie );
$nowtime = time - $difftime * 60 * 60;

if ( $FORM{'m'} eq 'c' ) {
	require './sub/bbscust.pl';
	&setcustom;
	exit;
}

# 個人用設定反映
&refcustom;
$body = qq(<BODY bgcolor="#$CC{'bg'}" text="#$CC{'text'}" link="#$CC{'link'}" vlink="#$CC{'vlink'}" alink="#$alinkc">);

# Getlog
if ( $FORM{'m'} eq 'g' ) {
	require './sub/bbslog.pl';
	&getlog;
	exit;
}

# トピック一覧
if ( $FORM{'m'} eq 'l' ) {
	require './sub/bbstopic.pl';
	&lsttopic;
	exit;
}

# 管理モード
if ( $FORM{'ad'} ) {
	require './sub/bbsadmin.pl';
	&adminmain;
	exit;
}
if ( !$adminpost ) {
	require './sub/bbsadmin.pl';
	&setpass;
	exit;
}

# 個人用設定
if ( $FORM{'setup'} ) {
	require './sub/bbscust.pl';
	&prtcustom;
	exit;
}

# 表示件数設定
if ( $FORM{'d'} ne '' ) {
	if ( $FORM{'d'} > $logsave ) {
		$FORM{'d'} = $logsave;
	}
} else {
	$FORM{'d'} = $msgdisp;
}

if ( $FORM{'m'} eq 'p' && $FORM{'v'} && !$FORM{'reload'} ) {
	$postid = 0;
	$posterr = 0;
	if ( $ENV{'CONTENT_TYPE'} eq 'application/x-www-form-urlencoded' ) {
		&chkmessage;
		&putmessage;
	} else {
		$posterr = 255;
	}
	if ( $FORM{'ac'} || ( $FORM{'f'} && !$followwin ) ) {
		&prthtmlhead ( "$bbstitle 書き込み完了" );
		print <<EOF;
<H1>書き込み完了</H1>
</BODY>
</HTML>
EOF
		exit;
	}
	undef $FORM{'f'};
} elsif ( $FORM{'m'} eq 'f' ) {
	&prtfollow ( 0 );
} elsif ( $FORM{'m'} eq 's' || $FORM{'m'} eq 't' ) {
	require './sub/bbssrc.pl';
	&srcmessage;
} else {
	if ( $FORM{'m'} eq 'n' ) {
		$bmsg = $FORM{'b'};
	} else {
		$bmsg = 0;
	}
}

&prtmain ( '', '', '' );

exit;


__END__
