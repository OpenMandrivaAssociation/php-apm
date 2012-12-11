%define modname apm
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B10_%{modname}.ini

%define pre_rel beta4

Summary:	Alternative PHP Monitor
Name:		php-%{modname}
Version:	1.1.0
Release:	%mkrel 0.0.%{pre_rel}.1
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
%doc web AUTHORS LICENSE NEWS sql apm.ini package*.xml
%config(noreplace) %attr(0640,apache,apache) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
%attr(0750,apache,apache) /var/lib/php-apm


%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-0.0.beta4.1mdv2012.0
+ Revision: 806362
- 1.1.0beta4

* Fri Jun 01 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-0.0.beta3.1
+ Revision: 801811
- 1.1.0beta3

* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.0-0.0.beta2.1
+ Revision: 797205
- 1.1.0beta2
- rebuild for php-5.4.x
- rebuild

* Tue Nov 15 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1
+ Revision: 730707
- 1.0.1

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3
+ Revision: 696390
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2
+ Revision: 695347
- rebuilt for php-5.3.7

* Wed Jun 15 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1
+ Revision: 685385
- 1.0.0

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta3.5
+ Revision: 646609
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta3.4mdv2011.0
+ Revision: 629762
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta3.3mdv2011.0
+ Revision: 628061
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta3.2mdv2011.0
+ Revision: 600458
- rebuild

* Thu Nov 11 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta3.1mdv2011.0
+ Revision: 595938
- 1.0.0beta3

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta2.3mdv2011.0
+ Revision: 588740
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta2.2mdv2010.1
+ Revision: 514514
- rebuilt for php-5.3.2

* Sun Jan 31 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta2.1mdv2010.1
+ Revision: 498793
- import php-apm


* Sun Jan 31 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-0.0.beta2.1mdv2010.0
- initial Mandriva package
