%define modname apm
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B10_%{modname}.ini

%define pre_rel %{nil}

Summary:	Alternative PHP Monitor
Name:		php-%{modname}
Version:	1.0.0
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/APM/
Source0:	http://pecl.php.net/get/APM-%{version}%{pre_rel}.tgz
Source1:	B10_apm.ini
Patch0:		APM-1.0.0-default_path.diff
BuildRequires:	sqlite3-devel
BuildRequires:	mysql-devel
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Monitoring extension for PHP, collects error events and store them in a local
SQLite database.

%prep

%setup -q -n APM-%{version}%{pre_rel}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

cp %{SOURCE1} %{inifile}

%build
%serverbuild

export APM_SHARED_LIBADD="-lmysqlclient -lz -lsqlite3"
phpize
%configure2_5x \
    --with-libdir=%{_lib} \
    --with-sqlite3=%{_prefix} \
    --with-mysql=%{_prefix} \
    --with-zlib-dir=%{_prefix} \
    --with-%{modname}=shared,%{_prefix}

# use the correct version
echo "#define APM_VERSION \"%{version}%{pre_rel}\"" >> config.h

%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}/var/lib/php-apm

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc web AUTHORS LICENSE NEWS apm.sql apm.ini package*.xml
%config(noreplace) %attr(0640,apache,apache) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
%attr(0750,apache,apache) /var/lib/php-apm
