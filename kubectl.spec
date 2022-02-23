%define		major	1
%define		minor	23
%define		patch	4
%define		vendor_version	1.23.4

Summary:	Kubectl (Kubernetes client tools)
Name:		kubectl
Version:	%{major}.%{minor}.%{patch}
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://dl.k8s.io/v%{version}/kubernetes-src.tar.gz
# Source0-md5:	f895c16fd87ceeaa945e006f0e0e981c
URL:		http://kubernetes.io/
BuildRequires:	golang >= 1.16
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
Kubectl (Kubernetes client tool). This package contains only the
kubectl tool so it can be distributed and installed without any other
kubernetes package.

It groups containers that make up an application into logical units
for management and discovery.

%package -n bash-completion-kubectl
Summary:	Bash completion for kubectl command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-kubectl
Bash completion for kubectl command line.

%package -n fish-completion-kubectl
Summary:	fish-completion for kubectl
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-kubectl
fish-completion for kubectl.

%package -n zsh-completion-kubectl
Summary:	ZSH completion for kubectl command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-kubectl
ZSH completion for kubectl command line.

%prep
%setup -qc

%build
ldflags="-X k8s.io/component-base/version.gitMajor=%{major} \
	-X k8s.io/component-base/version.gitMinor=%{minor} \
	-X k8s.io/component-base/version.buildDate=$(date +'%Y-%m-%dT%H:%M:%SZ') \
	-X k8s.io/component-base/version.gitCommit= \
	-X k8s.io/component-base/version.gitVersion=v%{version} \
	-X k8s.io/client-go/pkg/version.gitVersion=v%{version}"
%__go build -v -ldflags="$ldflags" -o target/kubectl k8s.io/kubernetes/cmd/kubectl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{bash_compdir},%{fish_compdir},%{zsh_compdir}}
install -p target/kubectl $RPM_BUILD_ROOT%{_bindir}

./target/kubectl completion bash > $RPM_BUILD_ROOT%{bash_compdir}/kubectl
./target/kubectl completion fish > $RPM_BUILD_ROOT%{fish_compdir}/kubectl.fish
./target/kubectl completion zsh > $RPM_BUILD_ROOT%{zsh_compdir}/_kubectl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kubectl

%files -n bash-completion-kubectl
%defattr(644,root,root,755)
%{bash_compdir}/kubectl

%files -n fish-completion-kubectl
%defattr(644,root,root,755)
%{fish_compdir}/kubectl.fish

%files -n zsh-completion-kubectl
%defattr(644,root,root,755)
%{zsh_compdir}/_kubectl
