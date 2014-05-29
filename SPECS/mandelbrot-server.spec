Name:		    mandelbrot-server
Version:	    0.0.4
Release:	    1%{?dist}
Summary:	    Mandelbrot network monitoring system - server
Group:		    System Environment/Daemons
License:	    GPL
URL:		    http://www.mandelbrot.io
Source:         mandelbrot-server-%{version}-bin.tar.gz
Source1:        supervisor-3.0.tar.gz
BuildRoot:	    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	mandelbrot-common, python-setuptools
Requires:	    mandelbrot-common, python-setuptools

%description
Mandelbrot network monitoring system - server


%prep
%setup -c
%setup -T -D -a 1


%build


%install
rm -rf %{buildroot}

PYTHON=/usr/libexec/mandelbrot/python-bootstrap

JAVALIB_DIR=$RPM_BUILD_ROOT/usr/lib/mandelbrot/java
PYLIB_DIR=$RPM_BUILD_ROOT/usr/lib/mandelbrot/python2.6
LIBEXEC_DIR=$RPM_BUILD_ROOT/usr/libexec/mandelbrot
INITD_DIR=$RPM_BUILD_ROOT/etc/rc.d/init.d
SYSCONFIG_DIR=$RPM_BUILD_ROOT/etc/sysconfig

mkdir -p $JAVALIB_DIR
mkdir -p $PYLIB_DIR
mkdir -p $LIBEXEC_DIR

# install supervisord
pushd supervisor-3.0
export PYTHONPATH=$PYLIB_DIR
$PYTHON ./setup.py \
        build_scripts --executable $PYTHON \
        install --install-lib $PYLIB_DIR --install-scripts $LIBEXEC_DIR \
        install_scripts
rm -f $PYLIB_DIR/*.pth $PYLIB_DIR/site.py*
rm -f $LIBEXEC_DIR/easy_install*
popd

# copy the server jars
pushd mandelbrot-server-%{version}-bin
cp target/scala-2.10/*.jar $JAVALIB_DIR


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/usr/lib/mandelbrot/java
/usr/lib/mandelbrot/python2.6
/usr/libexec/mandelbrot


%changelog

* Thu May 29 2014 Michael Frank <syntaxjockey@gmail.com> 0.0.4-1
- Initial RPM release
