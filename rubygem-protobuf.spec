# Generated from protobuf-3.10.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name protobuf

Name: rubygem-%{gem_name}
Version: 3.10.3
Release: 1.8%{?dist}
Summary: Google Protocol Buffers serialization and RPC implementation for Ruby
License: MIT
URL: https://github.com/localshred/protobuf
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# We need patch from the cucumber fork to make protobuf compatible with cucumber-messages
# Gemspec rename and version bumps were omitted from the diff by hand.
# curl -L https://github.com/cucumber/protobuf/compare/v3.10.3...v3.10.8.diff -o rubygem-protobuf-3.10.3-cucumber-messages-compatibility.patch
Patch0: %{name}-%{version}-cucumber-messages-compatibility.patch
# For some reason spec/encoding/extreme_values_spec.rb does not appear in the previous patch properly
# even though it should appear in previous diff creation, so when applying the file is unchanged and test fails.
# Let's add the patch explicitly, it just enforces encoding in test case.
Patch1: %{name}-%{version}-spec-extreme-values-force-ascii-utf8-encoding.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(middleware)
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(timecop)
BuildRequires: rubygem(thor)
BuildRequires: rubygem(thread_safe)
# rubygem-ffi-rzmq is currently not in fedora.
# BuildRequires: rubygem(ffi-rzmq)
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

%patch0 -p1
%patch1 -p1

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

# rubygem-ffi-rzmq is not in fedora
# Removing the require does not seem to affect this test anyway
# as long as we require the correct file instead.
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

  mv $file{,.disabled}
done
# Another ffi-zmq test that needs disabling.
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
