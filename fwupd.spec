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
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gusb)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	gpgme-devel
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libgcab-1.0)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(efivar)
BuildRequires:	pkgconfig(efiboot)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(libsmbios_c)
#BuildRequires:	pkgconfig(umockdev-1.0)
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
