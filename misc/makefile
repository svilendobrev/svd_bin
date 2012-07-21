now:
	@echo targets: kmail_pass_decrypt unwand

unwand: unwand.cpp
	$(CXX) $+ -o $@ -lcrypto
kmail_pass_decrypt: kmail_pass_decrypt.c utf8.c
	$(CC) $+ -o $@

#libvte: misc/vte-fix-ctrl-home-end-tab.diff (vte-fix-ctrl-keys.diff is fixed)
# 	needs libgtk-dev; m install -> /usr/local/lib + ldconfig
#vfu + rx*: filedir/rx4vfu/* vfu-20110128-patch64-utf8-rx_auto-wifnewer-svd.tbz
#	needs libncursesw5-dev
#dellfand: dellfand0.9 qini/tun/etc/default/dellfand
#misc/ax*term*
#misc/ooffice

# vim:ts=4:sw=4:noexpandtab
