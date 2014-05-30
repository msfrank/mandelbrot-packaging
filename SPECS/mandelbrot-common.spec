Name:		    mandelbrot-common
Version:	    0.0.4
Release:	    1%{?dist}
Summary:	    Mandelbrot network monitoring system - common tools
Group:		    System Environment/Daemons
License:	    GPL
URL:		    http://www.mandelbrot.io
Source0:	    python-bootstrap
BuildRoot:	    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	python-setuptools
Requires:	    python-setuptools
Requires(pre):  shadow-utils

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
mkdir -p %{buildroot}/var/log/mandelbrot


%clean
rm -rf %{buildroot}


%pre
getent group mandelbrot >/dev/null || groupadd -r mandelbrot
getent passwd mandelbrot >/dev/null || \
    useradd -r -g mandelbrot -d /var/lib/mandelbrot -s /sbin/nologin \
    -c "Mandelbrot network monitoring system" mandelbrot
exit 0  # don't fail the install if user/group creation fails


%files
%defattr(0755,root,root,-)
/usr/lib/mandelbrot
/usr/libexec/mandelbrot
/etc/mandelbrot
%attr(0755,mandelbrot,mandelbrot)     /var/lib/mandelbrot
%attr(0755,mandelbrot,mandelbrot)     /var/run/mandelbrot
%attr(0755,mandelbrot,mandelbrot)     /var/log/mandelbrot


%changelog

* Fri May 30 2014 Michael Frank <syntaxjockey@gmail.com> 0.0.4-1
- Initial RPM release
