# Generated from protobuf-3.10.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name protobuf

Name: rubygem-%{gem_name}
Version: 3.10.3
Release: 1%{?dist}
Summary: Google Protocol Buffers serialization and RPC implementation for Ruby
License: MIT
URL: https://github.com/localshred/protobuf
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# BuildRequires: rubygem(ffi-rzmq)
BuildRequires: rubygem(rspec)
# BuildRequires: rubygem(parser) = 2.3.0.6
# BuildRequires: rubygem(timecop)
# BuildRequires: rubygem(yard)
# BuildRequires: rubygem(varint)
# BuildRequires: rubygem(ruby-prof)
BuildRequires: rubygem(middleware)
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(timecop)
BuildRequires: rubygem(thor)
BuildRequires: rubygem(thread_safe)
BuildArch: noarch

%description
Google Protocol Buffers serialization and RPC implementation for Ruby.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}

# Avoid bundler dependency
sed -i -e '/require .pry./ s/^/#/g' \
       -e '/require .bundler./ s/^/#/g' \
       -e '/^Bundler\./ s/^/#/g' \
  spec/spec_helper.rb

# ffi-rzmq is not in fedora
# Removing the require does not seem to affect the test suite anyway
# as long as we require the correct file.
sed -i -e "s/require .protobuf\/zmq./require 'protobuf\/rpc\/connectors\/ping'/g" \
  spec/lib/protobuf/rpc/connectors/ping_spec.rb

# This test fails only without access to internet.
sed -i -e '/context .when a select timeout is fired./,/^    end$/ s/^/#/' \
  spec/lib/protobuf/rpc/connectors/ping_spec.rb

# There is not currently a ffi-rzmq gem in Fedora,
# let's disable test suites testing the rzmq capability.
for file in  spec/lib/protobuf/rpc/servers/zmq/server_spec.rb \
             spec/lib/protobuf/rpc/servers/zmq/util_spec.rb \
             spec/functional/zmq_server_spec.rb \
	     spec/lib/protobuf/rpc/connectors/zmq_spec.rb ; do

  mv $file{,.bak}
done

sed -i -e "/context ..*zmq.*. do/,/^      end$/ s/^/#/g" spec/lib/protobuf/cli_spec.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/protoc-gen-ruby
%{_bindir}/rpc_server
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/bin
%{gem_libdir}
%{gem_instdir}/profile.html
%{gem_instdir}/proto
%{gem_instdir}/varint_prof.rb
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/protobuf.gemspec
%{gem_instdir}/spec
%doc %{gem_instdir}/CHANGES.md
%{gem_instdir}/install-protobuf.sh

%changelog
* Fri Oct 30 2020 Pavel Valena <pvalena@redhat.com> - 3.10.3-1
- Initial package
