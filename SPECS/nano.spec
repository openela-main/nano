Summary:         A small text editor
Name:            nano
Version:         2.9.8
Release:         1%{?dist}
License:         GPLv3+
URL:             https://www.nano-editor.org
Source:          https://www.nano-editor.org/dist/v2.9/%{name}-%{version}.tar.gz
Source2:         nanorc

BuildRequires:   file-devel
BuildRequires:   gettext-devel
BuildRequires:   gcc
BuildRequires:   git
BuildRequires:   groff
BuildRequires:   ncurses-devel
BuildRequires:   sed
BuildRequires:   texinfo
Conflicts:       filesystem < 3
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

%description
GNU nano is a small and friendly text editor.

%prep
%autosetup -S git

%build
mkdir build
cd build
%global _configure ../configure
%configure
make %{?_smp_mflags}

# generate default /etc/nanorc
# - disable line wrapping by default
# - set hunspell as the default spell-checker
# - enable syntax highlighting by default (#1270712)
sed -e 's/# set nowrap/set nowrap/' \
    -e 's/^#.*set speller.*$/set speller "hunspell"/' \
    -e 's|^# \(include "/usr/share/nano/\*.nanorc"\)|\1|' \
    %{SOURCE2} doc/sample.nanorc > ./nanorc

%install
cd build
%make_install
rm -f %{buildroot}%{_infodir}/dir

# remove installed HTML documentation
rm -f %{buildroot}%{_docdir}/nano/{nano,nano.1,nanorc.5,rnano.1}.html

# install default /etc/nanorc
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 ./nanorc %{buildroot}%{_sysconfdir}/nanorc

%find_lang %{name}

%post
if [ -f %{_infodir}/%{name}.info.gz ]; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir
fi
exit 0

%preun
if [ $1 -eq 0 ]; then
  if [ -f %{_infodir}/%{name}.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir
  fi
fi
exit 0

%files -f build/%{name}.lang
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%doc build/doc/sample.nanorc
%doc doc/{faq,nano}.html
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/nanorc
%{_mandir}/man*/*
%{_infodir}/nano.info*
%{_datadir}/nano

%changelog
* Mon Jun 04 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.8-1
- new upstream release

* Tue May 15 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.7-1
- new upstream release

* Fri Apr 27 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.6-1
- new upstream release

* Wed Apr 25 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.5-2
- fix crash when using word completion

* Thu Mar 29 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.5-1
- new upstream release

* Wed Mar 21 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.4-2
- fix crash of 'nano --restrict' when <Insert> is pressed (#1558532)

* Thu Mar 08 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.4-1
- new upstream release

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.3-3
- add explicit BR for the gcc compiler

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.3-1
- new upstream release

* Tue Jan 02 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.2-1
- new upstream release

* Tue Nov 28 2017 Kamil Dudka <kdudka@redhat.com> - 2.9.1-1
- new upstream release

* Mon Nov 20 2017 Kamil Dudka <kdudka@redhat.com> - 2.9.0-1
- new upstream release

* Mon Aug 28 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.7-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.6-1
- new upstream release

* Sun Jun 25 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.5-1
- new upstream release

* Mon May 22 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.4-1
- new upstream release

* Thu May 18 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.3-1
- new upstream release

* Thu May 04 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.2-1
- new upstream release

* Wed Apr 12 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.1-1
- new upstream release

* Tue Apr 04 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.0-2
- use upstream patch to prevent symlink attack while creating a backup

* Fri Mar 31 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.0-1
- new upstream release

* Thu Feb 23 2017 Kamil Dudka <kdudka@redhat.com> - 2.7.5-1
- new upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Kamil Dudka <kdudka@redhat.com> - 2.7.4-1
- new upstream release (removes French man pages)

* Fri Dec 30 2016 Kamil Dudka <kdudka@redhat.com> - 2.7.3-1
- new upstream release

* Mon Dec 12 2016 Kamil Dudka <kdudka@redhat.com> - 2.7.2-1
- new upstream release

* Mon Oct 31 2016 Kamil Dudka <kdudka@redhat.com> - 2.7.1-1
- new upstream release

* Thu Sep 01 2016 Kamil Dudka <kdudka@redhat.com> - 2.7.0-1
- new upstream release

* Thu Aug 11 2016 Kamil Dudka <kdudka@redhat.com> - 2.6.3-1
- use %%autosetup in %%prep
- build out of source tree
- do not recode man pages, they are UTF-8 encoded since v2.3.6
- new upstream release

* Thu Jul 28 2016 Kamil Dudka <kdudka@redhat.com> - 2.6.2-1
- drop BuildRoot and Group tags, which are no longer necessary
- new upstream release

* Mon Jun 27 2016 Kamil Dudka <kdudka@redhat.com> - 2.6.1-1
- new upstream release

* Mon Jun 20 2016 Kamil Dudka <kdudka@redhat.com> - 2.6.0-1
- new upstream release

* Fri Feb 26 2016 Kamil Dudka <kdudka@redhat.com> - 2.5.3-1
- new upstream release

* Fri Feb 12 2016 Kamil Dudka <kdudka@redhat.com> - 2.5.2-2
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Kamil Dudka <kdudka@redhat.com> - 2.5.1-1
- new upstream release

* Sun Dec 06 2015 Kamil Dudka <kdudka@redhat.com> - 2.5.0-1
- new upstream release

* Wed Nov 18 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.3-1
- new upstream release

* Mon Oct 12 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.2-2
- enable syntax highlighting by default (#1270712)
- remove installed HTML documentation (to prevent a build failure in rawhide)

* Tue Jul 07 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.2-1
- new upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.1-1
- new upstream release

* Mon Mar 23 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.0-1
- new upstream release

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.3.6-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Jan 27 2015 Kamil Dudka <kdudka@redhat.com> - 2.3.6-6
- additional fixes to the file locking feature of nano (#1186384)

* Mon Jan 26 2015 Kamil Dudka <kdudka@redhat.com> - 2.3.6-5
- fix the file locking feature of nano (#1183320)

* Mon Jan 05 2015 Kamil Dudka <kdudka@redhat.com> - 2.3.6-4
- drop BR for autoconf, which is no longer needed

* Mon Jan 05 2015 Kamil Dudka <kdudka@redhat.com> - 2.3.6-3
- do not use closed file descriptor when setting backup's timestamp (#1177155)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Kamil Dudka <kdudka@redhat.com> - 2.3.6-1
- new upstream release

* Wed Jul 16 2014 Kamil Dudka <kdudka@redhat.com> - 2.3.5-1
- new upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Kamil Dudka <kdudka@redhat.com> - 2.3.4-1
- new upstream release

* Thu May 29 2014 Kamil Dudka <kdudka@redhat.com> - 2.3.3-1
- new upstream release

* Fri Aug 09 2013 Kamil Dudka <kdudka@redhat.com> - 2.3.2-4
- document the --poslog (-P) option in nano.1 man page

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Kamil Dudka <kdudka@redhat.com> - 2.3.2-2
- add "BuildRequires: file-devel" to build libmagic support (#927994)

* Tue Mar 26 2013 Kamil Dudka <kdudka@redhat.com> - 2.3.2-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 2.3.1-5
- fix specfile issues reported by the fedora-review script

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.3.1-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 11 2011 Kamil Dudka <kdudka@redhat.com> - 2.3.1-1
- new upstream release

* Thu Mar 03 2011 Kamil Dudka <kdudka@redhat.com> - 2.3.0-1
- new upstream release (#680736)
- use hunspell as default spell-checker (#681000)
- fix for http://thread.gmane.org/gmane.editors.nano.devel/2911

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 28 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.6-2
- fix bugs introduced by patches added in 2.2.6-1 (#657875)

* Mon Nov 22 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.6-1
- new upstream release (#655978)
- increase code robustness (patches related to CVE-2010-1160, CVE-2010-1161)

* Sat Aug 07 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.5-1
- new upstream release (#621857)

* Thu Apr 15 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.4-1
- new upstream release
- CVE-2010-1160, CVE-2010-1161 (#582739)

* Wed Mar 03 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.3-1
- new upstream release

* Fri Jan 29 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.2-1
- new upstream release

* Sun Dec 27 2009 Kamil Dudka <kdudka@redhat.com> - 2.2.1-1
- new upstream release

* Tue Dec 01 2009 Kamil Dudka <kdudka@redhat.com> - 2.2.0-1
- new upstream release

* Wed Nov 25 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-7
- sanitize specfile according to Fedora Packaging Guidelines 

* Thu Oct 15 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-6
- use nanorc.sample as base of /etc/nanorc

* Tue Oct 13 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-5
- fix build failure of the last build

* Tue Oct 13 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-4
- ship a system-wide configuration file along with the nano package
- disable line wrapping by default (#528359)

* Mon Sep 21 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-3
- suppress warnings for __attribute__((warn_unused_result)) (#523951)

* Fri Sep 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-2
- install binaries to /bin (#168340)

* Fri Sep 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-1
- new upstream release
- dropped patch no longer needed (possible change in behavior though negligible)
- fixed broken HTML doc in FR locales (#523951)

* Thu Sep 17 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.6-8
- do process install-info only without --excludedocs(#515943)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr  4 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.0.6-5
- Mark localized man pages with %%lang, fix French nanorc(5) (#322271).

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.6-4
- Autorebuild for GCC 4.3

* Fri Dec 07 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.0.6-3
- Pass rnano.1 through iconv to silence the final rpmlint complaint
  and finish up the merge review.

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 2.0.6-2
- Update licence
- Fix open(O_CREAT) calls without mode

* Sun Jun 03 2007 Florian La Roche <laroche@redhat.com> - 2.0.6-1
- update to 2.0.6

* Mon Feb 05 2007 Florian La Roche <laroche@redhat.com> - 2.0.3-1
- update to 2.0.3
- update spec file syntax, fix scripts rh#220527

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.12-1.1
- rebuild

* Mon Jul 10 2006 David Woodhouse <dwmw2@redhat.com> - 1.3.12-1
- Update to 1.3.12

* Tue May 16 2006 David Woodhouse <dwmw2@redhat.com> - 1.3.11-1
- Update to 1.3.11
- BuildRequires: groff (#191946)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.8-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.8-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 5 2005 David Woodhouse <dwmw2@redhat.com> 1.3.8-1
- 1.3.8

* Wed Mar 2 2005 David Woodhouse <dwmw2@redhat.com> 1.3.5-0.20050302
- Update to post-1.3.5 CVS tree to get UTF-8 support.

* Wed Aug 04 2004 David Woodhouse <dwmw2@redhat.com> 1.2.4-1
- 1.2.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 02 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.2.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Aug 11 2003 Bill Nottingham <notting@redhat.com> 1.2.1-4
- build in different environment

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  6 2003 Bill Nottingham <notting@redhat.com> 1.2.1-2
- description tweaks

* Mon May  5 2003 Bill Nottingham <notting@redhat.com> 1.2.1-1
- initial build, tweak upstream spec file
