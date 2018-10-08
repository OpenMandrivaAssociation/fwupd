Summary:	Firmware update daemon
Name:		fwupd
Version:	1.1.2
Release:	1
License:	GPLv2+
URL:		https://github.com/hughsie/fwupd
Source0:	https://github.com/hughsie/fwupd/archive/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(fwup)
BuildRequires:	systemd-macros
BuildRequires:	meson
BuildRequires:	gnu-efi
BuildRequires:	pesign
ExclusiveArch:	%{x86_64} %{ix86} aarch64

%description
fwupd is a simple daemon to allow session software
to update device firmware on your local machine.

%prep
%autosetup -p1

%build
%meson -Dman=false -Dtests=false -Dgtkdoc=false
%meson_build

%install
%meson_install

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable %{name}.service
EOF

%files
%{_presetdir}/86-%{name}.preset
