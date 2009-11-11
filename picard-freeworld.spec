%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:             picard-freeworld
Version:          0.12.1
Release:          2%{?dist}
Summary:          Acoustic fingerprinting for Picard tagger
Group:            Applications/Multimedia

Source0:          http://ftp.musicbrainz.org/pub/musicbrainz/picard/picard-%{version}.tar.gz
Patch0:           %{name}-0.11-avsetup.patch

License:          GPLv2+
Url:              http://musicbrainz.org/doc/PicardTagger
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    python-devel
BuildRequires:    gettext
BuildRequires:    desktop-file-utils
BuildRequires:    PyQt4 >= 4.3
BuildRequires:    python-mutagen > 1.9
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
%patch0 -p0

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
* Wed Nov 11 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.12.1-2
- Rebuild again for F-12 (bump release tag)

* Wed Nov  4 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.12.1-1
- Update to upstream 0.12.1 (brown bag fix release)

* Wed Oct 28 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.12-1
- Update to 0.12
- Drop SSE2 patch, now applied upstream, hopefully fixes #678:
  http://bugs.musicbrainz.org/ticket/5263

* Tue Jun 23 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.11-6
- Patch to fix segfaults using SSE2 (#678)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.11-5
- rebuild for new F11 features

* Wed Jan 14 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.11-4
- Remove check target, only useful in the base picard package.

* Fri Jan  2 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.11-3
- Rename to picard-freeworld as per review
- Fix cp/install commands
- Modified patch by Bob Arendt to skip test for <avcodec.h>

* Mon Dec 29 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.11-2
- Initial RPM Fusion package for providing acoustic fingerprinting.
