Name:		mandelbrot-common
Version:	0.0.4
Release:	1%{?dist}
Summary:	Mandelbrot network monitoring system - common tools
Group:		System Environment/Daemons
License:	GPL
URL:		http://www.mandelbrot.io
Source0:	python-bootstrap
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	python-setuptools
Requires:	python-setuptools

%description
Mandelbrot network monitoring system - common tools


%prep


%build


%install
rm -rf %{buildroot}

LIB_DIR=%{buildroot}/usr/lib/mandelbrot
mkdir -p $LIB_DIR
mkdir -p $LIB_DIR/python2.6/site-packages
mkdir -p $LIB_DIR/java

LIBEXEC_DIR=%{buildroot}/usr/libexec/mandelbrot
mkdir -p $LIBEXEC_DIR
cp $RPM_SOURCE_DIR/python-bootstrap $LIBEXEC_DIR

mkdir -p %{buildroot}/etc/mandelbrot
mkdir -p %{buildroot}/var/lib/mandelbrot
mkdir -p %{buildroot}/var/run/mandelbrot


%clean
rm -rf %{buildroot}


%files
%defattr(0755,root,root,-)
/usr/lib/mandelbrot
/usr/libexec/mandelbrot
/usr/libexec/mandelbrot/python-bootstrap
/etc/mandelbrot
/var/lib/mandelbrot
/var/run/mandelbrot


%changelog

