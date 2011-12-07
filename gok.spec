%define po_package gok

Summary: GNOME Onscreen Keyboard
Name: gok
Version: 2.28.1
Release: 5%{?dist}
License: LGPLv2+
Group: User Interface/Desktops
URL: http://www.gok.ca/
Source0: http://download.gnome.org/sources/gok/2.28/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: gok-0.10.2-launcher.patch
Patch1: lm.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=613632
Patch2: gok-dir-prefix.patch
# updated translations
# https://bugzilla.redhat.com/show_bug.cgi?id=589210
Patch3: gok-translations.patch

Requires(pre):    GConf2
Requires(post):   GConf2
Requires(post):   scrollkeeper >= 0.1.4
Requires(preun):   GConf2
Requires(postun): scrollkeeper >= 0.1.4

Requires:       at-spi
# for /usr/share/sounds/freedesktop/stereo
Requires:	sound-theme-freedesktop

BuildRequires:  at-spi-devel
BuildRequires:  gail-devel
BuildRequires:  intltool
BuildRequires:  scrollkeeper
BuildRequires:  libgnomeui-devel
BuildRequires:  libwnck-devel
BuildRequires:  gnome-speech-devel
BuildRequires:  gtk-doc
BuildRequires:  gettext
BuildRequires:  libXt-devel
BuildRequires:  libXevie-devel
BuildRequires:  libcanberra-devel

%description
The gok project aims to enable users to control their computer without
having to rely on a standard keyboard or mouse, leveraging GNOME's
built-in accessibility framework.

%package devel
Summary: Libraries/include files for the GNOME Onscreen Keyboard
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgnomeui-devel
Requires: atk-devel
Requires: libbonobo-devel
Requires: gtk2-devel
Requires: gail-devel
Requires: libwnck-devel
Requires: esound-devel
Requires: at-spi-devel
Requires: pkgconfig
Requires: gtk-doc

%description devel
The gok project aims to enable users to control their computer without
having to rely on a standard keyboard or mouse, leveraging GNOME's
built-in accessibility framework.

This package contains the libraries and includes files necessary to develop
applications and plugins for gok.

%prep
%setup -q
%patch0 -p1 -b .launcher
%patch1 -p1 -b .lm
%patch2 -p1 -b .dir-prefix
%patch3 -p1 -b .translations

%build
%configure

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}

iconv -f latin1 -t utf-8 NEWS > NEWSx && mv NEWSx NEWS


%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%find_lang %{po_package} --with-gnome


%clean
rm -rf $RPM_BUILD_ROOT

%post
scrollkeeper-update -q
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gok.schemas > /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gok.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gok.schemas > /dev/null || :
fi

%postun
scrollkeeper-update -q


%files -f %{po_package}.lang
%defattr(-,root,root,-)
%doc README NEWS AUTHORS COPYING
%{_sysconfdir}/gconf/schemas/*schemas
%{_bindir}/gok
%{_bindir}/create-branching-keyboard
%{_libdir}/bonobo/servers/GNOME_Gok.server
%{_datadir}/gok
%{_datadir}/icons/hicolor/48x48/apps/gok.png
%exclude %{_datadir}/applications/gok.desktop
%{_datadir}/sounds/freedesktop/stereo/goksound1.wav
%{_datadir}/sounds/freedesktop/stereo/goksound2.wav

%{_datadir}/pixmaps/*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*pc
%{_datadir}/gtk-doc/html/gok

%changelog
* Mon Jun  7 2010 Matthias Clasen <mclasen@redhat.com> 2.28.1-5
- Remove a space-saving hack that causes multlib conflicts
Resolves: #599382

* Mon May 24 2010 David Zeuthen <davidz@redhat.com> 2.28.1-4
- Don't require htmlview
Resolves: #593314

* Mon May 10 2010 Matthias Clasen <mclasen@redhat.com> 2.28.1-3
- Updated translations
Resolves: #589210

* Mon Mar 22 2010 Ray Strode <rstrode@redhat.com> 2.28.1-2
Resolves: #575933
- Support relocatable .gnome2

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-1
- Update to 2.28.1

* Tue Sep 22 2009 Matthias Clasen <mclasen@redhat.com> 2.28.0-1
- Update to 2.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> 2.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> 2.27.91-1
- Update to 2.27.91

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-1
- Update to 2.27.4

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> 2.27.3-1
- Update to 2.27.3

* Sat Jun 13 2009 Matthias Clasen <mclasen@redhat.com> 2.27.2-2
- Drop unneeded direct dependencies

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> 2.27.2-1
- Update to 2.27.2
- http://download.gnome.org/sources/gok/2.27/gok-2.27.2.news

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-2
- Don't drop schemas translations from po files

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Fri Jan 30 2009 Debarshi Ray <rishi@fedoraproject.org> - 2.25.3-4
- Removed mixed use of tabs and spaces.
- Use parallel make.

* Sat Jan 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.3-3
- Merge review feedback (#225852)

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.3-2
- Update to 2.25.3

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Thu Sep 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Tue Jul 15 2008 Matthias Clasen <mclasen@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.7-3
- Autorebuild for GCC 4.3

* Sat Feb  2 2008 Matthias Clasen <mclasen@redhat.com> - 1.3.7-2
- Fix some file permissions (#430482)

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 1.3.7-1
- Update to 1.3.7

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 1.3.4-1
- Update to 1.3.4

* Fri Sep 14 2007 Matthias Clasen <mclasen@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.3.2-1
- Update to 1.3.2

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.3.1-3
- Rebuild for selinux ppc32 issue.

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 1.3.1-2
- Update license field
- Use %%find_lang for help files

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Tue Jun  5 2007 Matthias Clasen <mclasen@redhat.com> - 1.2.2-4
- Rebuild again

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.2.2-3
- Rebuild against new libwnck

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 1.2.2-2
- Move api docs to -devel
- Some file list cleanups

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 1.2.2-1
- Update to 1.2.2

* Sat Feb 24 2007 David Zeuthen <davidz@redhat.com> - 1.2.1-3
- Make gok work under gdm (bgo #383514)

* Fri Jan 19 2007 Matthias Clasen <mclasen@redhat.com> - 1.2.1-2
- Update to 1.2.1

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 1.2.0-2
- Fix scripts according to packaging guidelines

* Fri Sep  8 2006 Matthias Clasen <mclasen@redhat.com> - 1.2.0-1
- Update to 1.2.0
- Fix directory ownership issues (#205681)

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.10-2.1
- rebuild

* Thu May 18 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.10-2
- Update to 1.0.10

* Mon May 15 2006 John (J5) Palmieri <johnp@redhat.com> - 1.0.8-2.1
- bump and rebuild

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> 1.0.8-2
- Update to 1.0.8

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.de> 1.0.7-1
- Update to 1.0.7

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 1.0.6-2
- BuildRequires: libXt-devel

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.6-1
- Update to 1.0.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Matthias Clasen <mclasen@redhat.com>
- don't crash when getting unexpected values from gconf

* Mon Nov 21 2005 Matthias Clasen <mclasen@redhat.com>
- fix memory handling errors 

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com>
- with modular X in /usr/%%{_lib}, libdir patch isn't needed - remove it

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- Rebuilt

* Wed Aug 10 2005 Matthias Clasen <mclasen@redhat.com> 1.0.5-3
- Rebuilt 

* Tue Jul 12 2005 Matthias Clasen <mclasen@redhat.com> 1.0.5-2
- Rebuilt 

* Tue Jun 28 2005 Matthias Clasen <mclasen@redhat.com> 1.0.5-1
- Update to 1.0.5

* Wed Mar 30 2005 Matthias Clasen <mclasen@redhat.com> 1.0.3-1
- Update to 1.0.3
- Add missing Requires (#152489)

* Mon Mar 14 2005 Matthias Clasen <mclasen@redhat.com> 1.0.2-1
- Update to 1.0.2

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 1.0.1-2
- Rebuild with gcc4

* Mon Feb 28 2005 Matthias Clasen <mclasen@redhat.com> 1.0.1-1
- Update to 1.0.1

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> 0.12.3-1
- Update to 0.12.3

* Fri Jan 28 2005 Matthias Clasen <mclasen@redhat.com> 0.12.1-1
- Update to 0.12.1

* Mon Sep 20 2004 Colin Walters <walters@redhat.com> 0.11.8-1
- Update to 0.11.8

* Wed Aug 31 2004 Colin Walters <walters@redhat.com> 0.11.7-1
- Update to 0.11.7

* Wed Aug 16 2004 Colin Walters <walters@redhat.com> 0.11.6-1
- Update to 0.11.6

* Wed Aug 04 2004 Colin Walters <walters@redhat.com> 0.11.5-1
- Update to 0.11.5

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Colin Walters <walters@redhat.com> 0.11.2-2
- Bust out new -devel package, make it depend on various
  other -devel packages.  Note this package is pretty much
  useless, but since upstream ships a .pc file we basically
  have to do it.
- Add BuildRequires on perl-libxml-enno
- Cut down obnoxiously long description

* Fri May 14 2004 Colin Walters <walters@redhat.com> 0.11.2-1
- New upstream version
- Use htmlview instead of mozilla directly
- BuildRequires gnome-speech-devel

* Wed Apr 21 2004 Nils Philippsen <nphilipp@redhat.com> 0.10.2-1
- version 0.10.2 fixes #118504
- use source URL
- remove desktop file as gok only works with a11y on and can be started
  from there

* Sun Apr 11 2004 Warren Togami <wtogami@redhat.com> 0.10.0-2
- BR intltool scrollkeeper libgnomeui-devel libwnck-devel gtk-doc m4 gettext

* Fri Apr  2 2004 Mark McLoughlin <markmc@redhat.com> 0.10.0-1
- Update to 0.10.0

* Wed Mar 31 2004 Mark McLoughlin <markmc@redhat.com> 0.9.11-1
- Update to 0.9.11

* Wed Mar 17 2004 Jonathan Blandford <jrb@redhat.com> 0.9.10-2
- rebuild

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 0.9.10-1
- Update to 0.9.10

* Thu Mar  4 2004 Mark McLoughlin <markmc@redhat.com> 0.9.9-1
- Update to 0.9.9

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Alexander Larsson <alexl@redhat.com> 0.9.8-1
- update to 0.9.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Sep  9 2003 Jonathan Blandford <jrb@redhat.com>
- update for GNOME 2.4

* Mon Jul 21 2003 Jonathan Blandford <jrb@redhat.com>
- new version

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May  5 2003 Jonathan Blandford <jrb@redhat.com> 
- Initial build.


