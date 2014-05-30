Name:		        mandelbrot-server
Version:	        0.0.4
Release:	        1%{?dist}
Summary:	        Mandelbrot network monitoring system - server
Group:		        System Environment/Daemons
License:	        GPL
URL:		        http://www.mandelbrot.io
Source:             mandelbrot-server-%{version}-bin.tar.gz
Source1:            supervisor-3.0.tar.gz
Source2:            mandelbrot.sysvinit
Source3:            mandelbrot.sysconfig
Source4:            mandelbrot-server.conf
Source5:            notification.rules
Source6:            supervisord.conf
BuildRoot:	        %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	    mandelbrot-common, python-setuptools
Requires:	        mandelbrot-common, python-setuptools
Requires(post):     chkconfig
Requires(preun):    chkconfig, initscripts
Requires(postun):   initscripts

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
ETC_DIR=$RPM_BUILD_ROOT/etc/mandelbrot
INITD_DIR=$RPM_BUILD_ROOT/etc/rc.d/init.d
SYSCONFIG_DIR=$RPM_BUILD_ROOT/etc/sysconfig

mkdir -p $JAVALIB_DIR
mkdir -p $PYLIB_DIR
mkdir -p $LIBEXEC_DIR
mkdir -p $ETC_DIR
mkdir -p $INITD_DIR
mkdir -p $SYSCONFIG_DIR

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
cp $RPM_SOURCE_DIR/mandelbrot-server-start $LIBEXEC_DIR

# copy default server config
cp $RPM_SOURCE_DIR/mandelbrot-server.conf $ETC_DIR
cp $RPM_SOURCE_DIR/notification.rules $ETC_DIR

# install sysvinit script
cp $RPM_SOURCE_DIR/mandelbrot.sysvinit $INITD_DIR/mandelbrot
cp $RPM_SOURCE_DIR/mandelbrot.sysconfig $SYSCONFIG_DIR/mandelbrot
cp $RPM_SOURCE_DIR/supervisord.conf $ETC_DIR/supervisord.conf


%clean
rm -rf %{buildroot}


%post
ln -s /usr/lib/mandelbrot/java/mandelbrot-server_2.10-%{version}-one-jar.jar /usr/lib/mandelbrot/java/mandelbrot-server-one-jar.jar
/sbin/chkconfig --add mandelbrot


%preun
if [ $1 -eq 0 ] ; then
    /sbin/service mandelbrot stop >/dev/null 2>&1
    /sbin/chkconfig --del mandelbrot
fi
rm -f /usr/lib/mandelbrot/java/mandelbrot-server-one-jar.jar


%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service mandelbrot condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
/usr/lib/mandelbrot/java
/usr/lib/mandelbrot/python2.6
/usr/libexec/mandelbrot
/etc/rc.d/init.d/mandelbrot
%config /etc/sysconfig/mandelbrot
%config /etc/mandelbrot/mandelbrot-server.conf
%config /etc/mandelbrot/notification.rules
%config /etc/mandelbrot/supervisord.conf


%changelog

* Thu May 29 2014 Michael Frank <syntaxjockey@gmail.com> 0.0.4-1
- Initial RPM release
