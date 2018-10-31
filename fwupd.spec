%global _disable_lto 1
%global _disable_ld_no_undefined 1

%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Firmware update daemon
Name:		fwupd
Version:	1.1.2
Release:	2
License:	GPLv2+
Group:	System/Boot and Init
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
BuildRequires:	pkgconfig(umockdev-1.0)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	python3egg(pygobject)
BuildRequires:	pkgconfig(py3cairo)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	python3egg(pillow)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	python-gi-cairo
BuildRequires:	systemd-macros
BuildRequires:	git-core
BuildRequires:	pkgconfig(valgrind)
BuildRequires:	meson
BuildRequires:	gnu-efi
BuildRequires:	pesign
BuildRequires:	vala-devel
BuildRequires:	vala-tools
BuildRequires:	noto-sans-fonts
ExclusiveArch:	%{x86_64} %{ix86} aarch64

%description
fwupd is a simple daemon to allow session software
to update device firmware on your local machine.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:	System/Libraries

%description -n %{libname}
System libraries for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:	Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{develname}
Development files for %{name}.

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

%find_lang %{name}

%files -f %{name}.lang
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/pki/%{name}-metadata
%dir %{_sysconfdir}/pki/%{name}
%dir %{_libdir}/%{name}-plugins-3
%dir %{_libexecdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_var}/lib/fwupd
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_sysconfdir}/%{name}/*
%{_sysconfdir}/pki/%{name}-metadata/*
%{_sysconfdir}/pki/%{name}/*
%{_bindir}/*
%{_libexecdir}/%{name}/*
%{_presetdir}/86-%{name}.preset
%{_unitdir}/%{name}-offline-update.service
%{_unitdir}/%{name}.service
%{_unitdir}/system-update.target.wants/*.service
/lib/udev/rules.d/*.rules
%{_libdir}/%{name}-plugins-3/*.so
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/polkit-1/rules.d/*.rules
%{_datadir}/%{name}/*
%{_datadir}/bash-completion/completions/%{name}*
%{_datadir}/metainfo/*.xml
%{_var}/lib/fwupd/*
%{_datadir}/locale/*/LC_IMAGES/%{name}*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{develname}
%{_includedir}/%{name}-1
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/%{name}.*
