#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	C library for reading DICOM files
Summary(pl.UTF-8):	Biblioteka C do odczytu plików DICOM
Name:		libdicom
Version:	1.1.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ImagingDataCommons/libdicom/releases
Source0:	https://github.com/ImagingDataCommons/libdicom/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	319057e80915050c008ba6b7ac1abb2c
URL:		https://github.com/ImagingDataCommons/libdicom
BuildRequires:	meson >= 0.50
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	uthash-devel
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdicom is a C library and a set of command-line tools for reading
DICOM WSI files. It is free (MIT licensed), fast, cross-platform, uses
little memory, has no dependencies, includes API documentation and is
easy to use from languages like Python.

%description -l pl.UTF-8
libdicom to biblioteka C i zestaw narzędzi linii poleceń do odczytu
plików DICOM WSI. Jest wolnodostępna (na licencji MIT), szybka,
wieloplatformowa, zużywa mało pamięci, nie ma zależności, zawiera
dokumentację API i jest łatwa w użyciu z języków takich jak Python.

%package devel
Summary:	Header files for libdicom library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libdicom
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libdicom library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libdicom.

%package static
Summary:	Static libdicom library
Summary(pl.UTF-8):	Statyczna biblioteka libdicom
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libdicom library.

%description static -l pl.UTF-8
Statyczna biblioteka libdicom.

%package apidocs
Summary:	API documentation for libdicom library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libdicom
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libdicom library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libdicom.

%prep
%setup -q

%build
%meson \
	%{!?with_static_libs:--default-library=shared}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/dcm-dump
%attr(755,root,root) %{_bindir}/dcm-getframe
%attr(755,root,root) %{_libdir}/libdicom.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdicom.so.1
%{_mandir}/man1/dcm-dump.1*
%{_mandir}/man1/dcm-getframe.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdicom.so
%{_includedir}/dicom
%{_pkgconfigdir}/libdicom.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdicom.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{_static,*.html,*.js}
