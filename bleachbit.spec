Name:		bleachbit
Version:	6.0.2
Release:	1
Summary:	A tool to remove unnecessary files, free disk space and maintain privacy
Group:		System/Configuration/Other
License:	GPLv3
URL:		https://bleachbit.sourceforge.net/
Source0:	https://download.bleachbit.org/%{name}-%{version}.tar.lzma
Source1:	%{name}.1
BuildArch:	noarch
BuildRequires:	make
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	python3dist(setuptools)
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
Requires:	python
Requires:	python3dist(scandir)
Requires:	python3dist(pygobject)
Requires:	gtk+3

%description
BleachBit deletes unnecessary files to free valuable disk space
and maintain privacy. Rid your system of old junk including cache,
temporary files, and cookies. Designed for Linux systems, it
wipes clean Bash, Beagle, Epiphany, Firefox, Adobe Flash, Java,
KDE, OpenOffice.org, Opera, rpm-build, XChat and more.

%prep
%setup -q

%build
make -C po local
%py_build

#sed -i -e 's|/usr/bin/env python|/usr/bin/python2|g' bleachbit/GUI.py bleachbit.py

%install
%make_install prefix=%{_prefix}

# create root desktop-file
cp org.bleachbit.BleachBit.desktop %{name}-root.desktop
sed -i -e 's/Name=BleachBit$/Name=BleachBit as Administrator/g' %{name}-root.desktop
sed -i -e 's/Exec=bleachbit$/Exec=pkexec bleachbit/g' %{name}-root.desktop

desktop-file-install \
	--add-category="Utility"\
        --dir=%{buildroot}%{_datadir}/applications/ \
        --vendor="" org.bleachbit.BleachBit.desktop

desktop-file-install \
	--add-category="Utility"\
        --dir=%{buildroot}%{_datadir}/applications/ \
        --vendor="" %{name}-root.desktop

mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1

chmod 644 %{buildroot}%{_datadir}/%{name}/Worker.py
chmod 755 %{buildroot}%{_datadir}/%{name}/CLI.py
chmod 755 %{buildroot}%{_datadir}/%{name}/GUI.py

#rm %{buildroot}%{_datadir}/%{name}/*.pyo

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/*.png
#{_datadir}/pixmaps/bleachbit-indicator.svg
%{_datadir}/applications/*.desktop
%{_mandir}/man1/%{name}.1.*
%{_datadir}/metainfo/org.bleachbit.BleachBit.metainfo.xml
%{_datadir}/polkit-1/actions/org.bleachbit.policy
