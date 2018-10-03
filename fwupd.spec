Summary:	Firmware update daemon
Name:		fwupdate
Version:	1.0.9
Release:	1
License:	GPLv2+
URL:		https://github.com/rhinstaller/fwupdate
Source0:	https://github.com/hughsie/fwupd/archive/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	fwupdate-devel
BuildRequires:	systemd-macros
ExclusiveArch:	%{x86_64} %{ix86} aarch64

%description
fwupd is a simple daemon to allow session software
to update device firmware on your local machine.

%prep
%autsetup -p1

%build
%configure
%make_build

%install
%make_install

%files
