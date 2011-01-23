%define pkgname linecache
Summary:	Extracts common modeling concerns from ActiveRecord
Name:		ruby-%{pkgname}
Version:	0.43
Release:	1
License:	Ruby-alike
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	3ebb8276bff3e68b16e13be5e1a8677f
Group:		Development/Languages
URL:		http://rubyforge.org/projects/ruby-linecache/
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-modules
BuildRequires:	setup.rb >= 3.4.1
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LineCache is a module for reading and caching lines. This may be
useful for example in a debugger where the same lines are shown many
times.

%package rdoc
Summary:	Documentation files for %{name}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
Documentation files for %{name}.

%package ri
Summary:	ri documentation for %{name}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{name}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{name}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{name}.

%prep
%setup -q -c
%{__tar} xf %{SOURCE0} -O data.tar.gz | %{__tar} xz
find -newer README  -o -print | xargs touch --reference %{SOURCE0}
cp %{_datadir}/setup.rb .

%build
ruby setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

ruby setup.rb setup

rdoc --ri --op ri lib
rdoc --op rdoc lib
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README AUTHORS
%{ruby_rubylibdir}/linecache.rb
%{ruby_rubylibdir}/tracelines.rb
%attr(755,root,root) %{ruby_archdir}/trace_nums.so

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/LineCache
%{ruby_ridir}/TraceLineNumbers
