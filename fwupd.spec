%global __requires_exclude ^%{python}$

%global _disable_lto 1
%global _disable_ld_no_undefined 1

%define major 2
%define plug_major 4
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Firmware update daemon
Name:		fwupd
Version:	1.7.2
Release:	1
License:	GPLv2+
Group:		System/Boot and Init
URL:		https://github.com/fwupd/fwupd
Source0:	https://github.com/fwupd/fwupd/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gusb)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(libprotobuf-c)
BuildRequires:	pkgconfig(jcat)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	gpgme-devel
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libgcab-1.0)
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(umockdev-1.0)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(py3cairo)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	python3dist(pillow)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(xmlb)
BuildRequires:	pkgconfig(tss2-esys)
BuildRequires:	efi-srpm-macros
%ifarch %{efi}
BuildRequires:	pkgconfig(fwupd-efi)
BuildRequires:	pkgconfig(efivar)
BuildRequires:	pkgconfig(efiboot)
BuildRequires:	gnu-efi
%endif
BuildRequires:	pkgconfig(ModemManager)
BuildRequires:	pkgconfig(qmi-glib)
BuildRequires:	pkgconfig(mbim-glib)
BuildRequires:	pkgconfig(gi-docgen)
BuildRequires:	python-gi
BuildRequires:	typelib(Pango)
BuildRequires:	python-gi-cairo
BuildRequires:	python-markdown
BuildRequires:	systemd-macros
BuildRequires:	git-core
BuildRequires:	pkgconfig(valgrind)
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	pesign
BuildRequires:	protobuf-c
BuildRequires:	mingw
BuildRequires:	vala-devel
BuildRequires:	vala-tools
BuildRequires:	noto-sans-fonts
Requires:	gsettings-desktop-schemas
Requires:	bubblewrap
Requires:	shared-mime-info
ExclusiveArch:	%{x86_64} %{ix86} %{aarch64}
%ifarch %{ix86} %{x86_64}
BuildRequires:	pkgconfig(libsmbios_c)
%endif

%description
fwupd is a simple daemon to allow session software
to update device firmware on your local machine.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
System libraries for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{develname}
Development files for %{name}.

%prep
%autosetup -p1

%build
%meson \
	-Dman=false \
	-Dtests=false \
%ifnarch %{x86_64} %{ix86}
	-Dplugin_dell=false \
	-Defi-ld=ld.bfd \
	-Dplugin_msr=false \
	-Defi_binary=false \
%endif
	-Dplugin_modem_manager=true || cat build/meson-logs/meson-log.txt

%meson_build

%install
%meson_install

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable %{name}.service
EOF

mkdir -p --mode=0700 %{buildroot}%{_localstatedir}/lib/fwupd/gnupg
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1757948
mkdir -p %{buildroot}%{_localstatedir}/cache/fwupd

%find_lang %{name}

%files -f %{name}.lang
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/pki/%{name}-metadata
%dir %{_sysconfdir}/pki/%{name}
%dir %{_libdir}/%{name}-plugins-%{plug_major}
%dir %{_libexecdir}/%{name}
%dir %{_datadir}/%{name}
%doc %{_docdir}/fwupd
%{_sysconfdir}/grub.d/35_fwupd
# modules-load.d is created on x86 for msr bits
# but not on aarch64
%ifarch %{ix86} %{x86_64}
/lib/modules-load.d/*
%endif
%{_sysconfdir}/%{name}/*
%{_sysconfdir}/pki/%{name}-metadata/*
%{_sysconfdir}/pki/%{name}/*
%{_bindir}/*
%{_libexecdir}/%{name}/*
%{_presetdir}/86-%{name}.preset
%{_unitdir}/%{name}-offline-update.service
%{_unitdir}/%{name}.service
%{_unitdir}/system-update.target.wants/*.service
%{_unitdir}/fwupd-refresh.service
%{_unitdir}/fwupd-refresh.timer
%{_presetdir}/fwupd-refresh.preset
%{_systemd_util_dir}/system-shutdown/fwupd.shutdown
%{_udevrulesdir}/*.rules
%{_libdir}/%{name}-plugins-%{plug_major}/*.so
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/polkit-1/rules.d/*.rules
%{_datadir}/fish/vendor_completions.d/fwupdmgr.fish
%{_datadir}/%{name}/*
%{_datadir}/bash-completion/completions/%{name}*
%{_datadir}/metainfo/*.xml
%{_iconsdir}/hicolor/scalable/apps/*.svg
%{_var}/lib/fwupd/*
#{_datadir}/locale/*/LC_IMAGES/%{name}*
%ifarch aarch64
/lib/modules-load.d/fwupd-redfish.conf
%endif
%dir %{_localstatedir}/lib/fwupd
%dir %{_localstatedir}/cache/fwupd
%ghost %{_localstatedir}/lib/fwupd/gnupg

%files -n %{libname}
%{_libdir}/lib%{name}*.so.%{major}*
%{_libdir}/libfwupdplugin.so.%{plug_major}*

%files -n %{develname}
%{_includedir}/%{name}-1
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/fwupdplugin.pc
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/%{name}.*
