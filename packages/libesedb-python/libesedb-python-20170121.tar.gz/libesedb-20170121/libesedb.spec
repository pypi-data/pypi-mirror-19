Name: libesedb
Version: 20170121
Release: 1
Summary: Library to access the Extensible Storage Engine (ESE) Database File (EDB) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libesedb/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
                
                

%description
libesedb is a library to access the Extensible Storage Engine (ESE) Database File (EDB) format

%package devel
Summary: Header files and libraries for developing applications for libesedb
Group: Development/Libraries
Requires: libesedb = %{version}-%{release}

%description devel
Header files and libraries for developing applications for libesedb.

%package tools
Summary: Several tools for reading Extensible Storage Engine (ESE) Database Files (EDB)
Group: Applications/System
Requires: libesedb = %{version}-%{release}   
   

%description tools
Several tools for reading Extensible Storage Engine (ESE) Database Files (EDB)

%package python
Summary: Python 2 bindings for libesedb
Group: System Environment/Libraries
Requires: libesedb = %{version}-%{release} python
BuildRequires: python-devel

%description python
Python 2 bindings for libesedb

%package python3
Summary: Python 3 bindings for libesedb
Group: System Environment/Libraries
Requires: libesedb = %{version}-%{release} python3
BuildRequires: python3-devel

%description python3
Python 3 bindings for libesedb

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libesedb.pc
%{_includedir}/*
%{_mandir}/man3/*

%files tools
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_bindir}/esedbexport
%attr(755,root,root) %{_bindir}/esedbinfo
%{_mandir}/man1/*

%files python
%defattr(644,root,root,755)
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files python3
%defattr(644,root,root,755)
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%changelog
* Sat Jan 21 2017 Joachim Metz <joachim.metz@gmail.com> 20170121-1
- Auto-generated

