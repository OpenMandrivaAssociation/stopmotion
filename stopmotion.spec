%define	version 0.6.2
%define rel	3
%define	release	%mkrel %rel
%define Summary An application for creating stopmotion animations

Name:		stopmotion
Summary:	%{Summary}
Version:	%{version} 
Release:	%{release} 
Source0:	http://developer.skolelinux.no/info/studentgrupper/2005-hig-stopmotion/project_management/webpage/releases/%{name}-%{version}.tar.gz
URL:		http://stopmotion.bjoernen.com/
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
BuildRequires:	SDL_image-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libxml2-devel
BuildRequires:  libtar-devel
BuildRequires:	inotifytools-devel
BuildRequires:  qt4-devel
BuildRequires:  qt4-linguist
BuildRequires:  imagemagick
BuildRequires:  gamin-devel
Requires:	vgrabbj

%description
Stopmotion is a free application for creating stop-motion animation movies.
The users will be able to create stop-motions from pictures imported from
a camera or from the harddrive, add sound effects and export the animation
to different video formats such as mpeg or avi.

%prep
%setup -q

%build
# Wrong permissions
chmod -R a+r *
for a in `find ./manual/`; do if [ ! -d $a ]; then chmod 644 $a;else chmod 755 $a;fi;done
%configure2_5x --with-html-dir=%{_datadir}/doc/%{name}/manual
rm -f Makefile
%qmake_qt4
%make
# Generate icons. The 48x48 one might be a bit ugly, but it'll have to do
convert graphics/stopmotion.png -resize 16x16 graphics/stopmotion-16.png
convert graphics/stopmotion.png -resize 48x48 graphics/stopmotion-48.png

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%buildroot
install -m755 stopmotion -D %{buildroot}%{_bindir}/%{name}

install -m644 graphics/stopmotion.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 graphics/stopmotion-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 graphics/stopmotion-48.png -D %{buildroot}%{_liconsdir}/%{name}.png
install -m644 graphics/stopmotion.png -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 graphics/stopmotion-16.png -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png


desktop-file-install	--vendor="" \
			--remove-category="Application" \
			--add-category="Qt" \
			--add-category="Video" \
			--add-category="AudioVideoEditing" \
			--add-category="X-MandrivaLinux-Multimedia-Video" \
			--dir %{buildroot}%{_datadir}/applications %name.desktop

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean 
rm -rf $%{buildroot}

%files
%defattr(-,root,root)
%doc README AUTHORS manual/
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
