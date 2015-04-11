
Summary:	Firmware update daemon
Name:		fwupdate
Version:	0.1.1
Release:	1
License:	GPLv2+
URL:		https://github.com/rhinstaller/fwupdate
Source0:	https://github.com/hughsie/fwupd/archive/%{name}_%(echo %{version} | tr . _).tar.gz
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(polkit-gobject-1)
#Buildrequires:	fwupdate-devel
ExclusiveArch:	x86_64 %{ix86} aarch64

%description
fwupd is a simple daemon to allow session software
to update device firmware on your local machine.

%prep
%setup -q

%build
%configure
%make

%install
%makeinstall_std

%files
