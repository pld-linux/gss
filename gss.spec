Summary:	Implementation of General Security Service API
Summary(pl):	Implementacja GSS API (General Security Service API)
Name:		gss
Version:	0.0.3
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://savannah.nongnu.org/download/gss/unstable.pkg/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c23953bbdcddd108cc38d425abfbbd2b
Patch0:		%{name}-info.patch
Patch1:		%{name}-amfix.patch
URL:		http://josefsson.org/gss/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1.5
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	shishi-devel >= 0.0.0
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GSS is an implementation of the Generic Security Service Application
Program Interface (GSS-API). GSS-API is used by network servers to
provide security services, e.g., to authenticate SMTP/IMAP clients
against SMTP/IMAP servers.

%description -l pl
GSS to implementacja GSS-API (Generic Security Service Application
Program Interface - ogólnego API us³ug bezpieczeñstwa). GSS-API jest
u¿ywane przez serwery sieciowe do udostêpniania us³ug bezpieczeñstwa,
na przyk³ad uwierzytelniania klientów SMTP/IMAP dla serwerów
SMTP/IMAP.

%package devel
Summary:	Header files for GSS library
Summary(pl):	Pliki nag³ówkowe biblioteki GSS
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for GSS library.

%description devel -l pl
Pliki nag³ówkowe biblioteki GSS.

%package static
Summary:	Static GSS library
Summary(pl):	Statyczna biblioteka GSS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static GSS library.

%description static -l pl
Statyczna biblioteka GSS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

tail +6524 aclocal.m4 > acinclude.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ANNOUNCE AUTHORS ChangeLog NEWS README* THANKS TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/gss.h
%{_includedir}/gss
%{_pkgconfigdir}/*.pc
%{_infodir}/*.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
