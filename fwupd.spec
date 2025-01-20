%global _disable_lto 1
%global _disable_ld_no_undefined 1

%define major 3
%define plug_major 7
%define libname %mklibname %{name}
%define oldlibname %mklibname %{name} 2
%define develname %mklibname %{name} -d

Summary:	Firmware update daemon
Name:		fwupd
Version:	2.0.4
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
BuildRequires:	pkgconfig(libdrm)
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
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	pkgconfig(xmlb)
BuildRequires:	pkgconfig(tss2-esys)
BuildRequires:	hwdata
BuildRequires:	efi-srpm-macros
BuildRequires:	python%{pyver}dist(pillow)
BuildRequires:	python%{pyver}dist(python-dbusmock)
%ifarch %{efi}
BuildRequires:	pkgconfig(fwupd-efi) >= 1.6
BuildRequires:	pkgconfig(efivar)
BuildRequires:	pkgconfig(efiboot)
BuildRequires:	gnu-efi
Requires:	fwupd-efi
%endif
BuildRequires:	pkgconfig(ModemManager)
BuildRequires:	pkgconfig(qmi-glib)
BuildRequires:	pkgconfig(mbim-glib)
BuildRequires:	pkgconfig(gi-docgen)
#BuildRequires:	flashrom
BuildRequires:	python-gi
BuildRequires:	typelib(Pango)
BuildRequires:	python-gi-cairo
BuildRequires:	python-markdown
BuildRequires:	systemd-rpm-macros
BuildRequires:	git-core
BuildRequires:	pkgconfig(valgrind)
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	pesign
BuildRequires:	protobuf-compiler
BuildRequires:	protobuf-c
BuildRequires:	mingw
BuildRequires:	vala-devel
BuildRequires:	vala-tools
BuildRequires:	noto-sans-fonts
BuildRequires:	pkgconfig(flashrom)
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
%rename	%{oldlibname}

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
	-Dcbor=disabled \
	-Dbluez=enabled \
	-Dpassim=disabled \
	-Dlaunchd=disabled \
	-Dplugin_powerd=disabled \
	-Dsupported_build=enabled \
%ifarch %{x86_64} %{ix86}
	-Dplugin_msr=enabled \
	-Dplugin_synaptics_mst=enabled \
%else
	-Dplugin_msr=disabled \
	-Dplugin_synaptics_mst=disabled \
%endif
%ifarch %{efi}
	-Dplugin_uefi_pk=enabled \
	-Dplugin_uefi_capsule=enabled \
	-Dplugin_uefi_capsule_splash=true \
	-Defi_binary=true \
%else
	-Dplugin_uefi_capsule=disabled \
	-Dplugin_uefi_pk=disabled \
%endif
%ifarch %{x86_64} %{aarch64}
	-Dplugin_gpio=enabled \
	-Dplugin_flashrom=enabled \
	-Dplugin_tpm=enabled \
%else
	-Dplugin_gpio=disabled \
	-Dplugin_flashrom=disabled \
	-Dplugin_tpm=disabled \
%endif
	-Dplugin_modem_manager=enabled || cat build/meson-logs/meson-log.txt

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

%post
%systemd_post fwupd.service

%preun
%systemd_preun fwupd.service

%postun
%systemd_postun_with_restart fwupd.service

%files -f %{name}.lang
%dir %{_sysconfdir}/%{name}
#dir %{_libdir}/%{name}-plugins-%{plug_major}
%dir %{_libexecdir}/%{name}
%dir %{_datadir}/%{name}
%ifarch %{efi}
%{_sysconfdir}/grub.d/35_fwupd
%endif
%{_sysconfdir}/pki/
%{_sysusersdir}/fwupd.conf
%{_libdir}/fwupd-%{version}
%optional %{_modulesloaddir}/*
%{_sysconfdir}/%{name}/*
%{_bindir}/*
%{_libexecdir}/%{name}/*
%{_presetdir}/86-%{name}.preset
%{_unitdir}/%{name}.service
%{_unitdir}/fwupd-refresh.service
%{_unitdir}/fwupd-refresh.timer
%{_systemd_util_dir}/system-shutdown/fwupd.shutdown
#{_libdir}/%{name}-plugins-%{plug_major}/*.so
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/icons/*/*/*/org.freedesktop.fwupd.*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/polkit-1/rules.d/*.rules
%{_datadir}/fish/vendor_completions.d/fwupdmgr.fish
%{_datadir}/%{name}/*
%{_datadir}/bash-completion/completions/%{name}*
%{_datadir}/metainfo/*.xml
#{_datadir}/locale/*/LC_IMAGES/%{name}*
%dir %{_localstatedir}/lib/fwupd
%dir %{_localstatedir}/cache/fwupd
%ghost %{_localstatedir}/lib/fwupd/gnupg
%{_libdir}/girepository-1.0/*.typelib

%files -n %{libname}
%{_libdir}/lib%{name}*.so.%{major}*

%files -n %{develname}
%doc %{_docdir}/fwupd
%doc %{_docdir}/libfwupd
%doc %{_docdir}/libfwupdplugin
%{_includedir}/%{name}-3
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/%{name}.*
%{_datadir}/installed-tests/fwupd
