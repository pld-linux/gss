Summary:	Implementation of General Security Service API
Summary(pl.UTF-8):	Implementacja GSS API (General Security Service API)
Name:		gss
Version:	0.0.21
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://josefsson.org/gss/releases/%{name}-%{version}.tar.gz
# Source0-md5:	f89b7acbe155e36baac554550773a0ad
Patch0:		%{name}-info.patch
URL:		http://josefsson.org/gss/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	gettext-devel >= 0.16
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.98
BuildRequires:	shishi-devel >= 0.0.18
BuildRequires:	texinfo
Requires:	shishi >= 0.0.18
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GSS is an implementation of the Generic Security Service Application
Program Interface (GSS-API). GSS-API is used by network servers to
provide security services, e.g., to authenticate SMTP/IMAP clients
against SMTP/IMAP servers.

%description -l pl.UTF-8
GSS to implementacja GSS-API (Generic Security Service Application
Program Interface - ogólnego API usług bezpieczeństwa). GSS-API jest
używane przez serwery sieciowe do udostępniania usług bezpieczeństwa,
na przykład uwierzytelniania klientów SMTP/IMAP dla serwerów
SMTP/IMAP.

%package devel
Summary:	Header files for GSS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GSS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk-doc-common
Requires:	shishi-devel >= 0.0.18
# man3/gss_acquire_cred.3 file conflict
Conflicts:	heimdal-devel

%description devel
Header files for GSS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GSS.

%package static
Summary:	Static GSS library
Summary(pl.UTF-8):	Statyczna biblioteka GSS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GSS library.

%description static -l pl.UTF-8
Statyczna biblioteka GSS.

%prep
%setup -q
%patch0 -p1

rm -f m4/libtool.m4

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

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
%attr(755,root,root) %{_libdir}/libgss.so.*.*.*
%{_mandir}/man1/gss.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgss.so
%{_libdir}/libgss.la
%{_includedir}/gss.h
%{_includedir}/gss
%{_pkgconfigdir}/*.pc
%{_infodir}/gss.info*
%{_mandir}/man3/gss*.3*
%{_gtkdocdir}/gss

%files static
%defattr(644,root,root,755)
%{_libdir}/libgss.a
