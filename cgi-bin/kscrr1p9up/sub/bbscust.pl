#! /usr/local/bin/perl

#
#	くずはすくりぷと Rev.0.1 Preview 9 (2000.9.3)
#	 (個人用環境設定画面用関数群)
#


###############################################################################
#  環境設定画面表示
###############################################################################

sub prtcustom {
	
	my ( @follow, @reload );
	$follow[$followwin] = 'checked';
	$reload[$reltype] = 'checked';
	
	&prthtmlhead ( "$bbstitle 個人用環境設定" );
	print <<EOF;
<H3>$bbstitle 個人用環境設定</H3><BR>
<FORM method="post" action="$cgiurl">
  <INPUT type="hidden" name="m" value="c">
  <INPUT type="hidden" name="nm" value="$FORM{'m'}">
  <UL>
    <LI><STRONG>表示設定</STRONG><BR> <BR>
    <TABLE border="0" cellspacing="0" cellpadding="0">
      <TR>
        <TD>文字色　　　</TD>
        <TD><INPUT type="text" name="tc" size="7" value="$CC{'text'}"></TD>
        <TD>　背景色</TD>
        <TD><INPUT type="text" name="bc" size="7" value="$CC{'bg'}"></TD>
      </TR>
      <TR>
        <TD>リンク色</TD>
        <TD><INPUT type="text" name="lc" size="7" value="$CC{'link'}"></TD>
        <TD>　訪問済リンク色 </TD>
        <TD><INPUT type="text" name="vc" size="7" value="$CC{'vlink'}"></TD>
      </TR>
      <TR>
        <TD>引用色</TD>
        <TD><INPUT type="text" name="qc" size="7" value="$CC{'qmsgc'}"></TD>
        <TD>　</TD>
        <TD>　</TD>
      </TR>
    </TABLE>
  </UL>
  <UL>
    <LI><STRONG>付加機能設定</STRONG><BR> <BR>
    gzip圧縮転送 <INPUT type="checkbox" name="g" value="checked" $S_gzchk[$gzipu]><BR>
    URL自動リンク <INPUT type="checkbox" name="a" value="checked" $S_alchk[$autolink]><BR>
  </UL>
  <UL>
    <LI><STRONG>フォロー画面の表示方法</STRONG><BR> <BR>
    <INPUT type="radio" name="fw" value="0" $follow[0]>新規ウィンドウを開いて表示<BR>
    <INPUT type="radio" name="fw" value="1" $follow[1]>新規ウィンドウを開かずに表示<BR>
  </UL>
  <UL>
    <LI><STRONG>０件リロード時のメッセージの表示方法</STRONG><BR> <BR>
    <INPUT type="radio" name="rt" value="0" $reload[0]>標準（投稿時刻降順表示）<BR>
    <INPUT type="radio" name="rt" value="1" $reload[1]>反転（投稿時刻昇順表示）<BR>
  </UL>
  <BR>
  「登録」を押した後に表示されるURLをブックマークに登録しましょう。<BR>
  上記の設定で掲示板を訪問することができます。<BR> <BR>
  <INPUT type="submit" value="登録">
  <INPUT type="reset" value="元に戻す">
  <INPUT type="submit" name="cr" value="規定値に戻す">
  <INPUT type="submit" name="cdc" value="Cookie消去">
</FORM>
</BODY>
</HTML>
EOF
}


###############################################################################
#  環境設定結果画面表示
###############################################################################

sub setcustom {
	
	my ( $p1, $p2, $p3, $nm, %alchk, %gzchk );
	
	if ( !$FORM{'cr'} ) {
		$alchk{'checked'} = 1;
		$gzchk{'checked'} = 1;
		$p1 = sprintf ( "%x", $alchk{"$FORM{'a'}"} + $FORM{'fw'} * 2 + $FORM{'rt'} * 4 + $gzchk{"$FORM{'g'}"} * 8 );
		$p2 = 0;
		$p3 = 0;
		if ( $FORM{'nm'} eq 'op' ) {
			$nm = 'm=o&';
		} else {
			$nm = '';
		}
		$FORM{'c'} = "$FORM{'tc'}$FORM{'bc'}$FORM{'lc'}$FORM{'vc'}$FORM{'qc'}$p1$p2$p3";
	} else {
		$FORM{'c'} = '';
	}
	
	if ( $FORM{'cdc'} ) {
		&putcookie ( $S_cexp - 2 );
	} else {
		&putcookie ( 0 ) if ( $cookie );
	}
	print "Location: $cgiurl?${nm}c=$FORM{'c'}\n\n";
}


1;


__END__
