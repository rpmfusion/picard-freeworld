%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:             picard-freeworld
Version:          0.16
Release:          3%{?dist}
Summary:          MusicBrainz-based audio tagger
Group:            Applications/Multimedia

Source0:          http://ftp.musicbrainz.org/pub/musicbrainz/picard/picard-%{version}.tar.gz

License:          GPLv2+
Url:              http://musicbrainz.org/doc/PicardTagger
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    python-devel
BuildRequires:    gettext
BuildRequires:    desktop-file-utils
BuildRequires:    PyQt4 >= 4.3
BuildRequires:    python-mutagen > 1.9
BuildRequires:    libofa-devel
Requires:         PyQt4 >= 4.3
Requires:         python-mutagen > 1.9
Requires:         libdiscid
BuildRequires:    libofa-devel
BuildRequires:    ffmpeg-devel
# Require matching main package picard from Fedora
Requires:         picard = %{version}

%description
Picard is an audio tagging application using data from the MusicBrainz
database. This add-on package supplies the library necessary for
acoustic fingerprinting.

%prep
%setup -q -n picard-%{version}

%build
env %{__python} setup.py config
env CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT

# remove everything except for {python_sitearch}/picard/musicdns/avcodec.so
cp -p $RPM_BUILD_ROOT%{python_sitearch}/picard/musicdns/avcodec.so avcodec.so
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{python_sitearch}/picard/musicdns/
install -pm 0755 avcodec.so $RPM_BUILD_ROOT%{python_sitearch}/picard/musicdns/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{python_sitearch}/picard/musicdns/avcodec.so

%changelog
* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.16-2
- Bump version to enable F-16 build.

* Tue Nov 15 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.16-1
- Sync with new 0.16 in Fedora

* Mon Sep 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.15.1-2
- Rebuilt for FFmpeg-0.8

* Sun Aug 21 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.15.1-1
- Drop 0.11-avsetup patch 
- Update to 0.15.1, sync with main package
- Add more plugins

* Mon May 30 2011 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.15-0.1.beta1
- Update to 0.15beta1 (#683055)
- Convert plugin files to files in git, easier to manage
- Only use plugins certified to be API compatible with 0.15 from
  http://users.musicbrainz.org/~luks/picard-plugins/

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Nov  3 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.12.1-1
- Update to upstream 0.12.1 (brown bag fix release)

* Tue Oct 27 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.12-1
- Update to 0.12 (#531224)
- Icons now in icons/hicolor directory

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec  9 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.11-2
- Fixed sources.

* Tue Dec  9 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.11-1
- Update to latest upstream (0.11)
- Drop upstreamed patch
- Remove sed-ing of .desktop file

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.10-3
- Rebuild for Python 2.6

* Tue Sep  2 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.10-2
- Update plugin versions to 0.10 where possible.  
- Temporarily disable the search plugins until they are ported to new API.

* Sun Aug 31 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.10-1
- Update to latest upstream (0.10).
- Add patch to work around broken setup.py.
- Fixed some spec file errors: duplicate sources.

* Sat Feb  9 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.9.0-6
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering

* Wed Dec 19 2007 Alex Lancaster <alexlan@fedoraproject.org> 0.9.0-5
- Add support for python eggs for F9+

* Wed Dec 19 2007 Alex Lancaster <alexlan@fedoraproject.org> 0.9.0-4
- Update to proper release: 0.9.0
- Drop plugins directory patch, applied upstream

* Tue Dec 04 2007 Alex Lancaster <alexlan@fedoraproject.org> 0.9.0-0.6.beta1
- strip out png extension from .desktop file

* Tue Dec 04 2007 Alex Lancaster <alexlan@fedoraproject.org> 0.9.0-0.5.beta1
- Add plugins from http://musicbrainz.org/doc/PicardQt/Plugins
- Patch to find proper plugins directory (filed upstream:
  http://bugs.musicbrainz.org/ticket/3430)
- Does not depend on python-musicbrainz2 any longer, uses libdiscid directly 

* Wed Nov 15 2007 Alex Lancaster <alexlan@fedoraproject.org> 0.9.0-0.4.beta1
- Various minor spec file cleanups to make sure timestamps stay correct

* Wed Nov 14 2007 Alex Lancaster <alexlan@fedoraproject.org> 0.9.0-0.3.beta1
- Create pixmaps directory

* Wed Nov 14 2007 Alex Lancaster <alexlan@fedoraproject.org> 0.9.0-0.2.beta1
- Missing BR: python-devel
- Use sitearch to make sure x86_64 builds work
- Install icons share/pixmaps/, rather than share/icons/

* Wed Nov 14 2007 Alex Lancaster <alexlan@fedoraproject.org> 0.9.0-0.1.beta1
- Initial packaging
