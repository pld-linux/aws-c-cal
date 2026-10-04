#
# Conditional build:
%bcond_without	openssl		# system OpenSSL instead of internal ByoCrypto
%bcond_without	tests		# unit tests
#
Summary:	AWS C CAL (Crypto Abstraction Layer)
Summary(pl.UTF-8):	Biblioteka AWS C CAL (Crypto Abstraction Layer - warstwa abstrakcji kryptografii)
Name:		aws-c-cal
Version:	1.0.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/awslabs/aws-c-cal/releases
Source0:	https://github.com/awslabs/aws-c-cal/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	95ea309c67a11708a00a38643be79b30
URL:		https://github.com/awslabs/aws-c-cal
BuildRequires:	aws-c-common-devel
BuildRequires:	cmake >= 3.9
BuildRequires:	gcc >= 5:3.2
# also aws-lc possible (with -DUSE_OPENSSL=OFF)
%{?with_openssl:BuildRequires:	openssl-devel >= 1.0.2}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AWS Crypto Abstraction Layer: Cross-Platform, C99 wrapper for
cryptography primitives.

%description -l pl.UTF-8
AWS Crypto Abstraction Layer - wieloplatformowy interfejs C99 do
podstaw kryptograficznych.

%package devel
Summary:	Header files for AWS C CAL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AWS C CAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	aws-c-common-devel
%{?with_openssl:Requires:	openssl-devel >= 1.0.2}

%description devel
Header files for AWS C CAL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AWS C CAL.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	%{?with_openssl:-DBYO_CRYPTO=OFF} \
	%{?with_openssl:-DUSE_OPENSSL=ON} \

%{__make}

%if %{with tests}
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md NOTICE README.md
%{_libdir}/libaws-c-cal.so.1.0.0
%ghost %{_libdir}/libaws-c-cal.so.1.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libaws-c-cal.so
%{_includedir}/aws/cal
%{_libdir}/cmake/aws-c-cal
