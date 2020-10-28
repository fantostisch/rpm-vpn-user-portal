%global git 2660ee4f0058e7a657365472038f3566390e0d83

Name:       vpn-user-portal
Version:    2.3.5
Release:    2%{?dist}
Summary:    User and admin portal for Let's Connect! and eduVPN
Group:      Applications/Internet
License:    AGPLv3+
URL:        https://git.tuxed.net/LC/vpn-user-portal/about/
%if %{defined git}
Source0:    https://github.com/fantostisch/vpn-user-portal/archive/%{git}.tar.gz
%else
Source0:    https://src.tuxed.net/vpn-user-portal/vpn-user-portal-%{version}.tar.xz
Source1:    https://src.tuxed.net/vpn-user-portal/vpn-user-portal-%{version}.tar.xz.minisig
Source2:    minisign-8466FFE127BCDC82.pub
%endif
Source3:    vpn-user-portal-httpd.conf
Source4:    vpn-user-portal.cron
Patch0:     vpn-user-portal-autoload.patch

# patch to convert php-sodium to php-libsodium functions/constants on el7
Patch1:     vpn-user-portal-sodium-compat.patch

BuildArch:  noarch

BuildRequires:  minisign
BuildRequires:  php-fedora-autoloader-devel
BuildRequires:  %{_bindir}/phpab
#    "require-dev": {
#        "ext-json": "*",
#        "phpunit/phpunit": "^4.8.35|^5|^6|^7"
#    },
BuildRequires:  php-json
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
BuildRequires:  phpunit7
%global phpunit %{_bindir}/phpunit7
%else
BuildRequires:  phpunit
%global phpunit %{_bindir}/phpunit
%endif

#    "require": {
#        "ext-curl": "*",
#        "ext-date": "*",
#        "ext-hash": "*",
#        "ext-pcre": "*",
#        "ext-pdo": "*",
#        "ext-sqlite3": "*",
#        "ext-spl": "*",
#        "fkooman/jwt": "^1",
#        "fkooman/oauth2-server": "^6",
#        "fkooman/secookie": "^5",
#        "fkooman/sqlite-migrate": "^0",
#        "lc/common": "v2.x-dev",
#        "paragonie/constant_time_encoding": "^1.0.3|^2.2.0",
#        "paragonie/random_compat": "^1|^2",
#        "paragonie/sodium_compat": "^1",
#        "php": ">=5.4.0",
#        "psr/log": "^1.1"
#    },
BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-curl
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-spl
BuildRequires:  php-composer(fkooman/jwt)
BuildRequires:  php-composer(fkooman/oauth2-server)
BuildRequires:  php-composer(fkooman/secookie) >= 5
BuildRequires:  php-composer(fkooman/secookie) < 6
BuildRequires:  php-composer(fkooman/sqlite-migrate)
BuildRequires:  php-composer(lc/common)
BuildRequires:  php-composer(paragonie/constant_time_encoding)
BuildRequires:  php-composer(psr/log)
%if 0%{?fedora} < 28 && 0%{?rhel} < 8
BuildRequires:  php-composer(paragonie/random_compat)
%endif

%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
BuildRequires:  php-sodium
%else
BuildRequires:  php-pecl(libsodium)
%endif

%if 0%{?fedora} >= 24
Requires:   httpd-filesystem
%else
# EL7 does not have httpd-filesystem
Requires:   httpd
%endif
Requires:   /usr/bin/qrencode
Requires:   crontabs
#    "require": {
#        "ext-curl": "*",
#        "ext-date": "*",
#        "ext-hash": "*",
#        "ext-pcre": "*",
#        "ext-pdo": "*",
#        "ext-sqlite3": "*",
#        "ext-spl": "*",
#        "fkooman/jwt": "^1",
#        "fkooman/oauth2-server": "^6",
#        "fkooman/secookie": "^5",
#        "fkooman/sqlite-migrate": "^0",
#        "lc/common": "v2.x-dev",
#        "paragonie/constant_time_encoding": "^1.0.3|^2.2.0",
#        "paragonie/random_compat": "^1|^2",
#        "paragonie/sodium_compat": "^1",
#        "php": ">=5.4.0",
#        "psr/log": "^1.1"
#    },
Requires:   php(language) >= 5.4.0
Requires:   php-cli
Requires:   php-curl
Requires:   php-date
Requires:   php-hash
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-spl
Requires:   php-composer(fkooman/jwt)
Requires:   php-composer(fkooman/oauth2-server)
Requires:   php-composer(fkooman/secookie) >= 5
Requires:   php-composer(fkooman/secookie) < 6
Requires:   php-composer(fkooman/sqlite-migrate)
Requires:   php-composer(lc/common)
Requires:   php-composer(paragonie/constant_time_encoding)
Requires:   php-composer(psr/log)
%if 0%{?fedora} < 28 && 0%{?rhel} < 8
Requires:   php-composer(paragonie/random_compat)
%endif

%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
Requires:   php-sodium
%else
Requires:   php-pecl(libsodium)
%endif

Requires(post): /usr/sbin/semanage
Requires(post): /usr/bin/openssl
Requires(postun): /usr/sbin/semanage

%description
The user and admin portal and API for Let's Connect! and eduVPN allowing 
for self-management by users and administrative tasks by designated 
administrators.

%prep
%if %{defined git}
%setup -qn vpn-user-portal-%{git}
%else
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -p %{SOURCE2}
%setup -qn vpn-user-portal-%{version}
%endif
%patch0 -p1
%if 0%{?fedora} < 28 && 0%{?rhel} < 8
%patch1 -p1
%endif

%build
echo "%{version}-%{release}" > VERSION

%{_bindir}/phpab -t fedora -o src/autoload.php src
cat <<'AUTOLOAD' | tee -a src/autoload.php
require_once '%{_datadir}/php/LC/Common/autoload.php';
require_once '%{_datadir}/php/fkooman/Jwt/autoload.php';
require_once '%{_datadir}/php/fkooman/OAuth/Server/autoload.php';
require_once '%{_datadir}/php/fkooman/SeCookie/autoload.php';
require_once '%{_datadir}/php/fkooman/SqliteMigrate/autoload.php';
require_once '%{_datadir}/php/ParagonIE/ConstantTime/autoload.php';
require_once '%{_datadir}/php/Psr/Log/autoload.php';
# optional dependency
if (is_file('%{_datadir}/php/fkooman/SAML/SP/autoload.php') && is_readable('%{_datadir}/php/fkooman/SAML/SP/autoload.php')) {
    require_once '%{_datadir}/php/fkooman/SAML/SP/autoload.php';
}
AUTOLOAD
%if 0%{?fedora} < 28 && 0%{?rhel} < 8
cat <<'AUTOLOAD' | tee -a src/autoload.php
require_once '%{_datadir}/php/random_compat/autoload.php';
AUTOLOAD
%endif

%install
mkdir -p %{buildroot}%{_datadir}/vpn-user-portal
cp VERSION %{buildroot}%{_datadir}/vpn-user-portal
mkdir -p %{buildroot}%{_datadir}/php/LC/Portal
cp -pr src/* %{buildroot}%{_datadir}/php/LC/Portal

for i in add-user foreign-key-list-fetcher init generate-oauth-key show-oauth-key
do
    install -m 0755 -D -p bin/${i}.php %{buildroot}%{_bindir}/vpn-user-portal-${i}
    sed -i '1s/^/#!\/usr\/bin\/php\n/' %{buildroot}%{_bindir}/vpn-user-portal-${i}
done

cp -pr schema web views locale %{buildroot}%{_datadir}/vpn-user-portal

mkdir -p %{buildroot}%{_sysconfdir}/vpn-user-portal
cp -pr config/config.php.example %{buildroot}%{_sysconfdir}/vpn-user-portal/config.php
ln -s ../../../etc/vpn-user-portal %{buildroot}%{_datadir}/vpn-user-portal/config

mkdir -p %{buildroot}%{_localstatedir}/lib/vpn-user-portal
ln -s ../../../var/lib/vpn-user-portal %{buildroot}%{_datadir}/vpn-user-portal/data

# cron
mkdir -p %{buildroot}%{_sysconfdir}/cron.d
%{__install} -p -D -m 0640 %{SOURCE4} %{buildroot}%{_sysconfdir}/cron.d/vpn-user-portal

# httpd
install -m 0644 -D -p %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/vpn-user-portal.conf

%check
%{_bindir}/phpab -o tests/autoload.php tests
cat <<'AUTOLOAD' | tee -a tests/autoload.php
require_once 'src/autoload.php';
AUTOLOAD

%{phpunit} tests --verbose --bootstrap=tests/autoload.php

%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/lib/vpn-user-portal(/.*)?' 2>/dev/null || :
restorecon -R %{_localstatedir}/lib/vpn-user-portal || :

# generate SAML keys if they do not yet exist
if [ ! -f "%{_sysconfdir}/%{name}/sp.key" ]
then
    /usr/bin/openssl \
        req \
        -nodes \
        -subj "/CN=SAML SP" \
        -x509 \
        -sha256 \
        -newkey rsa:3072 \
        -keyout "%{_sysconfdir}/%{name}/sp.key" \
        -out "%{_sysconfdir}/%{name}/sp.crt" \
        -days 1825 \
        2>/dev/null
    # allow web server to read the private key
    /usr/bin/chmod 0644 %{_sysconfdir}/%{name}/sp.key
fi

# Generate OAuth key if it not yet exists
if [ ! -f "%{_sysconfdir}/%{name}/oauth.key" ]
then
    %{_bindir}/vpn-user-portal-generate-oauth-key
fi

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/vpn-user-portal(/.*)?' 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/vpn-user-portal.conf
%dir %attr(0750,root,apache) %{_sysconfdir}/vpn-user-portal
%config(noreplace) %{_sysconfdir}/vpn-user-portal/config.php
%config(noreplace) %{_sysconfdir}/cron.d/vpn-user-portal
%{_bindir}/*
%dir %{_datadir}/php/LC
%{_datadir}/php/LC/Portal
%{_datadir}/vpn-user-portal
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/vpn-user-portal
%doc README.md CHANGES.md composer.json config/config.php.example CONFIG_CHANGES.md locale/CREDITS.md
%license LICENSE LICENSE.spdx

%changelog
* Tue Oct 28 2020 Nick Aquina <nickaquina@gmail.com> - 2.3.5-2
- WireGuard version

* Tue Oct 20 2020 François Kooman <fkooman@tuxed.net> - 2.3.5-1
- update to 2.3.5

* Tue Sep 08 2020 François Kooman <fkooman@tuxed.net> - 2.3.4-1
- update to 2.3.4

* Thu Aug 20 2020 François Kooman <fkooman@tuxed.net> - 2.3.3-5
- convert php-sodium to php-libsodium functions/constants on el7

* Tue Aug 11 2020 François Kooman <fkooman@tuxed.net> - 2.3.3-4
- put version/release in VERSION file

* Mon Aug 10 2020 François Kooman <fkooman@tuxed.net> - 2.3.3-3
- update URL/summary/description

* Tue Aug 04 2020 François Kooman <fkooman@tuxed.net> - 2.3.3-2
- release files moved to src.tuxed.net

* Tue Jul 28 2020 François Kooman <fkooman@tuxed.net> - 2.3.3-1
- update to 2.3.3

* Mon Jul 27 2020 François Kooman <fkooman@tuxed.net> - 2.3.2-1
- update to 2.3.2

* Fri Jul 10 2020 François Kooman <fkooman@tuxed.net> - 2.3.1-1
- update to 2.3.1

* Mon Jun 29 2020 François Kooman <fkooman@tuxed.net> - 2.3.0-1
- update to 2.3.0

* Tue May 26 2020 François Kooman <fkooman@tuxed.net> - 2.2.8-1
- update to 2.2.8

* Thu May 21 2020 François Kooman <fkooman@tuxed.net> - 2.2.7-1
- update to 2.2.7

* Tue May 12 2020 François Kooman <fkooman@tuxed.net> - 2.2.6-1
- update to 2.2.6

* Sun Apr 05 2020 François Kooman <fkooman@tuxed.net> - 2.2.5-1
- update to 2.2.5

* Mon Mar 30 2020 François Kooman <fkooman@tuxed.net> - 2.2.4-1
- update to 2.2.4

* Mon Mar 23 2020 François Kooman <fkooman@tuxed.net> - 2.2.3-1
- update to 2.2.3

* Fri Mar 13 2020 François Kooman <fkooman@tuxed.net> - 2.2.2-1
- update to 2.2.2

* Fri Feb 14 2020 François Kooman <fkooman@tuxed.net> - 2.2.1-1
- update to 2.2.1

* Thu Feb 13 2020 François Kooman <fkooman@tuxed.net> - 2.2.0-1
- update to 2.2.0

* Mon Jan 20 2020 François Kooman <fkooman@tuxed.net> - 2.1.6-1
- update to 2.1.6

* Mon Jan 20 2020 François Kooman <fkooman@tuxed.net> - 2.1.5-1
- update to 2.1.5
- be explicit about fkooman/secookie version

* Tue Dec 10 2019 François Kooman <fkooman@tuxed.net> - 2.1.4-1
- update to 2.1.4

* Mon Dec 02 2019 François Kooman <fkooman@tuxed.net> - 2.1.3-1
- update to 2.1.3

* Thu Nov 21 2019 François Kooman <fkooman@tuxed.net> - 2.1.2-1
- update to 2.1.2

* Thu Nov 21 2019 François Kooman <fkooman@tuxed.net> - 2.1.1-1
- update to 2.1.1

* Mon Nov 04 2019 François Kooman <fkooman@tuxed.net> - 2.1.0-1
- update to 2.1.0

* Mon Oct 14 2019 François Kooman <fkooman@tuxed.net> - 2.0.14-1
- update to 2.0.14

* Wed Sep 25 2019 François Kooman <fkooman@tuxed.net> - 2.0.13-1
- update to 2.0.13

* Thu Aug 29 2019 François Kooman <fkooman@tuxed.net> - 2.0.12-1
- update to 2.0.12

* Mon Aug 19 2019 François Kooman <fkooman@tuxed.net> - 2.0.11-1
- update to 2.0.11

* Tue Aug 13 2019 François Kooman <fkooman@tuxed.net> - 2.0.10-1
- update to 2.0.10

* Thu Aug 08 2019 François Kooman <fkooman@tuxed.net> - 2.0.9-2
- use /usr/bin/php instead of /usr/bin/env php

* Thu Aug 08 2019 François Kooman <fkooman@tuxed.net> - 2.0.9-1
- update to 2.0.9
- switch to minisign signature verification for release builds
- add CONFIG_CHANGES to documentation

* Wed Jul 31 2019 François Kooman <fkooman@tuxed.net> - 2.0.8-1
- update to 2.0.8

* Sat Jul 20 2019 François Kooman <fkooman@tuxed.net> - 2.0.7-1
- update to 2.0.7

* Thu Jun 27 2019 François Kooman <fkooman@tuxed.net> - 2.0.6-1
- update to 2.0.6

* Fri Jun 07 2019 François Kooman <fkooman@tuxed.net> - 2.0.5-1
- update to 2.0.5

* Tue May 21 2019 François Kooman <fkooman@tuxed.net> - 2.0.4-1
- update to 2.0.4

* Tue May 14 2019 François Kooman <fkooman@tuxed.net> - 2.0.3-1
- update to 2.0.3

* Wed May 01 2019 François Kooman <fkooman@tuxed.net> - 2.0.2-1
- update to 2.0.2

* Fri Apr 26 2019 François Kooman <fkooman@tuxed.net> - 2.0.1-1
- update to 2.0.1

* Mon Apr 01 2019 François Kooman <fkooman@tuxed.net> - 2.0.0-1
- update to 2.0.0
