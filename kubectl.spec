Summary:	Kubectl (Kubernetes client tools)
Name:		kubectl
Version:	1.13.3
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://storage.googleapis.com/kubernetes-release/release/v%{version}/bin/linux/amd64/%{name}
# Source0-md5:	205b5446cd5296827e3ac972678c74bd
URL:		http://kubernetes.io/
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# nothing to put there
%define		_enable_debug_packages	0

%description
Kubectl (Kubernetes client tool). This package contains only the
kubectl tool so it can be distributed and installed without any other
kubernetes package.

It groups containers that make up an application into logical units
for management and discovery.

%prep
%setup -qcT
install -p %{SOURCE0} .

%build
./kubectl version --client --short

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -p kubectl $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kubectl
