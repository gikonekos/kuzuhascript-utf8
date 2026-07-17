#! /usr/local/bin/perl

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (管理ツール)
#

###############################################################################
#  メッセージ削除モードメイン画面表示
###############################################################################

sub msglist {
	
	my @msgline;
	
	&prthtmlhead ( 'くずはすくりぷと メッセージ削除モード' );
	print <<EOF;
<CENTER>
<FORM method="post" action="$cgiurl">
<INPUT type="hidden" name="m" value="ad">
<INPUT type="hidden" name="u" value="$FORM{'u'}">
<INPUT type="hidden" name="ad" value="kx">
<H3 align="center">くずはすくりぷと メッセージ削除モード</H3>
<TABLE border="1">
  <TR>
    <TH nowrap>削除</TH>
    <TH nowrap>投稿日</TH>
    <TH nowrap>題名</TH>
    <TH nowrap>投稿者</TH>
    <TH nowrap>内容（一部）</TH>
  </TR>
EOF
	
	&loadmessage;
	for ( $i = 0 ; $i < @logdata ; $i++ ) {
		&getmessage ( $logdata[$i] );
		@msgline = split ( /\r/, $msg );
		$msg = $msgline[0];
		print <<EOF;
  <TR>
    <TD align="center" nowrap><INPUT type="checkbox" name="id$postid" value="checked"></TD>
    <TD nowrap>$wdate</TD>
    <TD nowrap>$title 　</TD>
    <TD nowrap>$user</TD>
    <TD nowrap>$msg</TD>
  </TR>
EOF
	}
	
	print <<EOF;
</TABLE>
<INPUT type="submit" value="削除実行">
</FORM>
<FORM method="post" action="$cgiurl">
<INPUT type="hidden" name="m" value="ad">
<INPUT type="hidden" name="u" value="$FORM{'u'}">
<INPUT type="hidden" name="ad" value="tp">
<INPUT type="submit" value="終了">
</FORM>
</CENTER>
</BODY>
</HTML>
EOF
}


###############################################################################
#  メッセージ削除
###############################################################################

sub msgdel {
	
	my ( @newlog, @newoldlog, $logitems, $oldlogitems );
	
	open ( FLOG, "+<$logfilename" ) || &prterror ( 'メッセージ読み込みに失敗しました' );
	eval 'flock ( FLOG, 2 )';
	seek ( FLOG, 0, 0 );
	@logdata = <FLOG>;
	
	for ( $i = 0 ; $i < $logsave ; $i++ ) {
		@logitems = split ( /\,/, $logdata[$i] );
		if ( $FORM{"id$logitems[1]"} eq 'checked' ) {
			
			if ( $oldlogfiledir && $oldlogfmt ) {
				&getnowdate ( $logitems[0] );
				if ( !$oldlogsavesw ) {
					$oldlogfilename = sprintf ( "%s/%d%02d%02d.dat",
					  $oldlogfiledir, $year, $mon, $mday );
				} else {
					$oldlogfilename = sprintf ( "%s%d%02d.dat",
					  $oldlogfiledir, $year, $mon );
				}
				open ( CLOG, "+<$oldlogfilename" ) || &prterror ( '過去ログ読み込みに失敗しました' );
				eval 'flock ( CLOG, 2 )';
				seek ( CLOG, 0, 0 );
				@oldlogdata = <CLOG>;
				
				undef @newoldlog;
				for ( $j = 0 ; $j < $logsave ; $j++ ) {
					@oldlogitems = split ( /\,/, $oldlogdata[$j] );
					if ( $logitems[1] ne $oldlogitems[1] ) {
						$newoldlog[$j] = $oldlogdata[$j];
					}
				}
				
				$oldstream = select ( CLOG );
				$| = 1;
				seek ( CLOG, 0, 0 );
				truncate ( CLOG, 0 );
				print CLOG @newoldlog;
				eval 'flock ( CLOG, 8 )';
				close ( CLOG );
				select ( $oldstream );
			}
			
		} else {
			$newlog[$i] = $logdata[$i];
		}
	}
	
	$oldstream = select ( FLOG );
	$| = 1;
	seek ( FLOG, 0, 0 );
	truncate ( FLOG, 0 );
	print FLOG @newlog;
	eval 'flock ( FLOG, 8 )';
	close ( FLOG );
	select ( $oldstream );
}


###############################################################################
#  パスワード設定画面表示
###############################################################################

sub setpass {
	
	&prthtmlhead ( 'くずはすくりぷと パスワード設定画面' );
	print <<EOF;
<FORM method="post" action="$cgiurl">
<INPUT type="hidden" name="m" value="ad">
<INPUT type="hidden" name="ad" value="ps">
<H2 align="center">くずはすくりぷと パスワード設定画面</H2>
<HR>
<CENTER>
<TABLE>
  <TR>
    <TD>
      <FONT size="+1">パスワード設定を行います。</FONT><BR>
      これから掲示板の管理で使用する「管理用パスワード」を入力してください。
    </TD>
  </TR>
</TABLE>
<BR>
<TABLE border="2" cellspacing="4">
  <TR>
    <TD>管理用パスワード</TD>
    <TD><INPUT size="30" type="text" name="ps" maxlength="127"></TD>
  </TR>
  <TR>
    <TD colspan="2"><FONT size="-1">
      ここで入力するパスワードは、管理人名での投稿、管理モードの認証の際に使用します。
      </FONT>
    </TD>
  </TR>
</TABLE>
<BR>
<INPUT type="submit" value="設定">　<INPUT type="reset" value="リセット">
</CENTER>
</FORM>
</BODY>
</HTML>
EOF
}


###############################################################################
#  暗号化テスト
###############################################################################

sub MD5test {
	
	my $tpass = 'ABCDE';
	my $tsalt = 'r7';
	my ( $cpass, $rpass, $slen );
	
	$MD5salt = '$1$';
	$cpass = crypt ( $tpass, "$MD5salt$tsalt" );
	if ( $cpass =~ /^\$1\$/ ) {
		$slen = 5;
	} else {
		$slen = 2;
	}
	$rpass = crypt ( $tpass, substr ( $cpass, 0, $slen ) );
	if ( ( $slen == 5 ) && ( $cpass eq $rpass ) && $cpass ) {
		return 2;
	} else {
		$cpass = crypt ( $tpass, "$tsalt" );
		$rpass = crypt ( $tpass, substr ( $cpass, 0, 2 ) );
		if ( ( $cpass eq $rpass ) && $cpass ) {
			return 1;
		} else {
			return 0;
		}
	}
}


###############################################################################
#  パスワード生成
###############################################################################

sub makepass {
	
	my $pass = $_[0];
	my ( $salt, $ctype, $cpass );
	my @saltlist = ( '0'..'9', 'A'..'Z', 'a'..'z' );
	
	if ( length ( $pass ) > 5 ) {
		$ctype = &MD5test;
		if ( $ctype > 0 ) {
			srand ( time ^ ( $$ + ( $$ << 15 ) ) );
			$salt = splice ( @saltlist, int ( rand ( @saltlist ) ), 1 ) . 
			  splice ( @saltlist, int ( rand ( @saltlist ) ), 1 );
			
			if ( $ctype == 2 ) {
				$cpass = crypt ( $pass, "\$1\$$salt" );
			} else {
				$cpass = crypt ( $pass, "$salt" );
			}
		} else {
			$cpass = $pass;
		}
		return $cpass;
	} else {
		&prterror ( 'パスワードが短すぎます。６桁以上の文字列を入力してください。' );
	}
}


###############################################################################
#  パスワード表示
###############################################################################

sub prtpass {
	
	my $cpass = &makepass ( $FORM{'ps'} );
	&prthtmlhead ( 'パスワード' );
	print <<EOF;
<H2 align="center">くずはすくりぷと パスワード設定画面</H2>
<HR>
<FORM>
<CENTER>
<TABLE>
  <TR>
    <TD>
      <FONT size="+1">暗号化パスワードを生成しました。</FONT><BR>
      掲示板スクリプト本体の所定の位置に、下記の暗号化パスワード文字列をコピーしてください。
    </TD>
  </TR>
</TABLE>
<BR>
<TABLE border="2" cellspacing="4">
  <TR>
    <TD>管理用パスワード</TD>
    <TD><INPUT type="text" name="dummy" value="$cpass" readonly></TD>
  </TR>
</TABLE>
</FORM>
</BODY>
</HTML>
EOF
}


###############################################################################
#  ログ表示
###############################################################################

sub logprint {
	
	&loadmessage;
	print "Content-Type: text/plain\n\n";
	
	print @logdata;
}


###############################################################################
#  管理メニュー画面表示
###############################################################################

sub adminmenu {
	
	&prthtmlhead ( 'くずはすくりぷと 管理メニュー' );
	print <<EOF;
<H2 align="center">くずはすくりぷと 管理メニュー</H2>
<HR>
<CENTER>
<FORM method="post" action="$cgiurl">
<INPUT type="hidden" name="m" value="ad">
<INPUT type="hidden" name="ad" value="kl">
<INPUT type="hidden" name="u" value="$FORM{'u'}">
<INPUT type="submit" value="メッセージ削除">
</FORM>
<FORM method="post" action="$cgiurl">
<INPUT type="hidden" name="m" value="ad">
<INPUT type="hidden" name="ad" value="rp">
<INPUT type="hidden" name="u" value="$FORM{'u'}">
<INPUT type="submit" value="暗号化パスワード再生成">
</FORM>
<FORM method="post" action="$cgiurl">
<INPUT type="hidden" name="m" value="ad">
<INPUT type="hidden" name="ad" value="lv">
<INPUT type="hidden" name="u" value="$FORM{'u'}">
<INPUT type="submit" value="ログ閲覧">
</FORM>
<FORM method="post" action="$cgiurl">
<INPUT type="submit" value="終了">
</FORM>
</CENTER>
</BODY>
</HTML>
EOF
}


###############################################################################
#  管理モードメイン処理
###############################################################################

sub adminmain {
	
	if ( !$FORM{'ad'} || $FORM{'ad'} eq 'tp' ) {
		&adminmenu;
	} elsif ( $FORM{'ad'} eq 'ps' ) {
		if ( $FORM{'ps'} ) {
			&prtpass;
		} else {
			&prterror ( 'パスワードが入力されていません。' );
		}
	} else {
		if ( &chkpasswd ) {
			if ( $FORM{'ad'} eq 'rp' ) {
				&setpass;
			} elsif ( $FORM{'ad'} eq 'kl' ) {
				&msglist;
			} elsif ( $FORM{'ad'} eq 'kx' ) {
				&msgdel;
				&msglist;
			} elsif ( $FORM{'ad'} eq 'lv' ) {
				&logprint;
			}
		} else {
			&prterror ( '認証に失敗しました。' );
		}
	}
}


1;
