Name:		    mandelbrot
Version:	    0.0.4
Release:	    1%{?dist}
Summary:	    Mandelbrot network monitoring system - client and agent utilities
Group:		    System Environment/Daemons
License:	    GPL
URL:		    http://www.mandelbrot.io
Source:	        mandelbrot-%{version}.tar.gz
Source1:        mandelbrot.conf
BuildRoot:	    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	mandelbrot-common, python-setuptools
Requires:	    mandelbrot-common, python-setuptools

%description
Mandelbrot network monitoring system - client and agent utilities


%prep
%setup


%build


%install
rm -rf %{buildroot}

PYTHON=/usr/libexec/mandelbrot/python-bootstrap

PYLIB_DIR=$RPM_BUILD_ROOT/usr/lib/mandelbrot/python2.6
LIBEXEC_DIR=$RPM_BUILD_ROOT/usr/libexec/mandelbrot
BIN_DIR=$RPM_BUILD_ROOT/usr/bin
SBIN_DIR=$RPM_BUILD_ROOT/usr/sbin
ETC_DIR=$RPM_BUILD_ROOT/etc/mandelbrot

mkdir -p $PYLIB_DIR
mkdir -p $LIBEXEC_DIR
mkdir -p $BIN_DIR
mkdir -p $SBIN_DIR
mkdir -p $ETC_DIR

export PYTHONPATH=$PYLIB_DIR
$PYTHON ./setup.py pesky_default --command flush
$PYTHON ./setup.py pesky_default --command set --key SYSCONF_DIR --value /etc/mandelbrot
$PYTHON ./setup.py pesky_default --command set --key LOCALSTATE_DIR --value /var/lib/mandelbrot
$PYTHON ./setup.py pesky_default --command set --key RUN_DIR --value /var/run/mandelbrot
$PYTHON ./setup.py \
        build_scripts --executable $PYTHON \
        install --install-lib $PYLIB_DIR --install-scripts $LIBEXEC_DIR \
        install_scripts
rm -f $PYLIB_DIR/*.pth $PYLIB_DIR/site.py*
rm -f $LIBEXEC_DIR/easy_install*


mv $LIBEXEC_DIR/mandelbrot $BIN_DIR
mv $LIBEXEC_DIR/mandelbrot-agent $SBIN_DIR

cp $RPM_SOURCE_DIR/mandelbrot.conf $ETC_DIR


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/usr/lib/mandelbrot/python2.6
/usr/libexec/mandelbrot
/usr/bin/mandelbrot
/usr/sbin/mandelbrot-agent
%config /etc/mandelbrot/mandelbrot.conf


%changelog

* Thu May 29 2014 Michael Frank <syntaxjockey@gmail.com> 0.0.4-1
- Initial RPM release
