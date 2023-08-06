%global pypi_name horizon-bsn
%global pypi_name_underscore horizon_bsn
%global rpm_name horizon-bsn
%global docpath doc/build/html
%global lib_dir %{buildroot}%{python2_sitelib}/%{pypi_name}/plugins/bigswitch

Name:           python-%{rpm_name}
Version:        20153.37.4
Release:        1%{?dist}
Summary:        Big Switch Networks horizon plugin for OpenStack
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

Requires:   pytz
Requires:   python-lockfile
Requires:   python-six
Requires:   python-pbr
Requires:   python-django
Requires:   python-django-horizon

BuildRequires: python-django
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-d2to1
BuildRequires: python-pbr
BuildRequires: python-lockfile
BuildRequires: python-eventlet
BuildRequires: python-six
BuildRequires: gettext
BuildRequires: python-oslo-sphinx >= 2.3.0
BuildRequires: python-netaddr
BuildRequires: python-kombu
BuildRequires: python-anyjson
BuildRequires: python-iso8601

%description
This package contains Big Switch
Networks horizon plugin

%prep
%setup -q -n %{pypi_name}-%{version}

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build
%{__python2} setup.py build_sphinx
rm %{docpath}/.buildinfo

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p %{lib_dir}/tests
for lib in %{lib_dir}/version.py %{lib_dir}/tests/test_server.py; do
    sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
    touch -r $lib $lib.new &&
    mv $lib.new $lib
done


%files
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name_underscore}
%{python2_sitelib}/%{pypi_name_underscore}-%{version}-py?.?.egg-info

%post

%preun

%postun

%changelog
* Fri Feb 3 2017 Aditya Vaja <wolverine.av@gmail.com> - 20153.37.4
- OSP-26 check for presence of routers
* Thu Jan 26 2017 Aditya Vaja <wolverine.av@gmail.com> - 20153.37.3
- OSP-19 ensure policy is deleted in MLR case
* Thu Jan 19 2017 Aditya Vaja <wolverine.av@gmail.com> - 20153.37.2
- OSP-6 handle MLR in horizon
* Fri Sep 2 2016 Aditya Vaja <wolverine.av@gmail.com> - 20153.37.1
- remove offending history from changelog
* Fri Sep 2 2016 Aditya Vaja <wolverine.av@gmail.com> - 20153.37.0
- tag branch for bcf 3.7 release
- merge master branch to stable/liberty, changes listed below
- move angular enabled files to future_enabled
- BVS-6759: move horizon dashboard to use the new AngularJS framework
- BVS-6497: present a warning when policy change doesn't affect existing policy set
- BVS-6323 limit testpath visiblity to tenants
- ensure quick testpath names are unique
