Summary:	Implementation of General Security Service API
Summary(pl):	Implementacja GSS API (General Security Service API)
Name:		gss
Version:	0.0.12
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://josefsson.org/gss/releases/%{name}-%{version}.tar.gz
# Source0-md5:	e3da7f9f6ee39ac108a2708934598527
Patch0:		%{name}-info.patch
URL:		http://josefsson.org/gss/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1.7
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	libtool >= 2:1.5
BuildRequires:	shishi-devel >= 0.0.7
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
Requires:	%{name} = %{version}-%{release}
Requires:	shishi-devel >= 0.0.7

%description devel
Header files for GSS library.

%description devel -l pl
Pliki nag³ówkowe biblioteki GSS.

%package static
Summary:	Static GSS library
Summary(pl):	Statyczna biblioteka GSS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GSS library.

%description static -l pl
Statyczna biblioteka GSS.

%prep
%setup -q
%patch0 -p1

# we don't have libtool 1.5a
%{__perl} -pi -e 's/AC_LIBTOOL_TAGS//' configure.ac
# incompatible with ksh
rm -f m4/libtool.m4

%build
# blegh, lt incompatible with ksh - must rebuild
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4
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
%doc AUTHORS ChangeLog NEWS README* THANKS
%attr(755,root,root) %{_bindir}/gss
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_mandir}/man1/gss.1*

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
