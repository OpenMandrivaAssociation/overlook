%define	name	overlook
%define	version	3.2
%define	release %mkrel 7
%define summary Overlook is a webmail system derived from squirrelmail
%define group	System/Servers
%define basedir %{_var}/www/html/overlook

Name:		%{name} 
Summary:	%{summary}
Version:	%{version} 
Release:	%{release} 
Source0:	%{name}-%{version}.tar.bz2
# A fixed Norwegian Bokmål translation
Source1:	%{name}-nb.po.bz2
# Patch to make i18n actually work (bug inherited from squirrelmail.
#  I have reported it upstream).
Patch0:		%{name}-i18n.patch.bz2
URL:		http://gforge.openit.it/projects/overlook/
Group:		%{group}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
Requires:	sendmail-command
Requires:	apache >= 1.3.19
Requires:	mod_php >= 4.0.4
Conflicts:	apache2-mod_php <= 2.0.44_4.3.1-1mdk
BuildRequires:	file
BuildArch:	noarch

%description
Overlook is a webmail system derived from squirrelmail.
It acts more like a normal mail client than a webmail client.

Remember to configure it by editing /etc/overlook/config.php
after installation.

%prep
%setup -q
%patch0 -p0

%build
# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%install
cat > README.install.urpmi << EOF
Remember to configure Overlook by editing /etc/overlook/config.php after installation.
EOF
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{basedir}
INSTALL="class config credits css data database FCKeditor functions images include js locale plugins po src themes index.php"
for a in $INSTALL; do
	cp -r $a $RPM_BUILD_ROOT%{basedir}/
done
mkdir -p $RPM_BUILD_ROOT%{_var}/cache/overlook/data/
# Put the config.php into /etc/
mkdir $RPM_BUILD_ROOT/etc/
mv $RPM_BUILD_ROOT%{basedir}/config/ $RPM_BUILD_ROOT/etc/overlook/
ln -s /etc/overlook/ $RPM_BUILD_ROOT%{basedir}/config
# Fix no_NO directories
ln -s %{basedir}/locale/no_NO $RPM_BUILD_ROOT%{basedir}/locale/nb_NO
# Remove non-functional nb_NO translation
rm -f $RPM_BUILD_ROOT%{basedir}/locale/nb_NO/*
install -m664 %{SOURCE1} $RPM_BUILD_ROOT%{basedir}/locale/no_NO/squirrelmail.po.bz2
bunzip2 $RPM_BUILD_ROOT%{basedir}/locale/no_NO/squirrelmail.po.bz2
msgfmt -v $RPM_BUILD_ROOT%{basedir}/locale/no_NO/squirrelmail.po -o $RPM_BUILD_ROOT%{basedir}/locale/no_NO/squirrelmail.mo
# Force spec helper not to relativize symlinks
export DONT_RELINK=1

%clean 
rm -rf $RPM_BUILD_ROOT 

%files 
%defattr(-,root,root)
%doc ChangeLog.txt History.it INSTALL OVERLOOK_AUTHORS README SQ_ChangeLog SQUIRRELMAIL_AUTHORS README.install.urpmi
%dir %{basedir}
%{basedir}/class/
%{basedir}/credits/
%{basedir}/css/
%{basedir}/data/
%{basedir}/database/
%{basedir}/FCKeditor/
%{basedir}/functions/
%{basedir}/images/
%{basedir}/include/
%{basedir}/js/
%{basedir}/locale/
%{basedir}/plugins/
%{basedir}/po/
%{basedir}/src/
%{basedir}/themes/
%{basedir}/config/
%{basedir}/index.php
%config(noreplace) /etc/overlook
%defattr(-,apache,apache)
%{_var}/cache/overlook/



%changelog
* Fri Sep 04 2009 Thierry Vignaud <tvignaud@mandriva.com> 3.2-7mdv2010.0
+ Revision: 430224
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tvignaud@mandriva.com> 3.2-6mdv2009.0
+ Revision: 254941
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tvignaud@mandriva.com> 3.2-4mdv2008.1
+ Revision: 130979
- kill re-definition of %%buildroot on Pixel's request
- import overlook


* Mon Nov 07 2005 Eskild Hustvedt <eskild@mandriva.org> 3.2-4mdk
- Rebuild (I messed up the 10.2 update)

* Mon Nov 07 2005 Eskild Hustvedt <eskild@mandriva.org> 3.2-3mdk
- Cleanup and hopefully fix upgrade to 2006.0

* Mon May 23 2005 Eskild Hustvedt <eskild@mandriva.org> 3.2-2mdk
- Fix wrong-script-end-of-line-encoding

* Wed Apr 27 2005 Eskild Hustvedt <eskild@mandriva.org> 3.2-1mdk
- New version 3.2
- Rediff patch 0
- Don't relativize symlinks

* Mon Mar 28 2005 Eskild Hustvedt <eskild@mandrake.org> 3.0-4mdk
- %%mkrel

* Thu Mar 17 2005 Eskild Hustvedt <eskild@mandrake.org> 3.0-3mdk
- Rebuild

* Thu Mar 10 2005 Eskild Hustvedt <eskild@mandrake.org> 3.0-2mdk
- Fixes to the Norwegian bokmål language directories
- Include more sane (but very incomplete) Norwegian bokmål translation
- Patch0: Quick (but ugly) fix making i18n work

* Mon Mar 07 2005  Eskild Hustvedt <eskild@mandrake.com> 3.0-1mdk
- Initial Mandrakelinux package
